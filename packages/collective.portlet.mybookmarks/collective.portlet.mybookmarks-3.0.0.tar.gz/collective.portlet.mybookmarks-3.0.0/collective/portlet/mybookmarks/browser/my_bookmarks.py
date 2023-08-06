# -*- coding: utf-8 -*-
from collective.portlet.mybookmarks import _
from collective.portlet.mybookmarks.controlpanel.interfaces import IMyBookmarksSettings
from plone import api
from plone.memoize import view
from plone.protect import PostOnly
from plone.protect.authenticator import createToken
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zExceptions import Forbidden
from zope.i18n import translate
from zope.i18n import translate
from zope.interface import alsoProvides

import json
import logging

logger = logging.getLogger(__name__)


class BaseBookmarksView(BrowserView):

    """
    Base view with common methods
    """

    @view.memoize
    def extract_user_bookmarks(self):
        """
        return stored bookmarks.
        They are a json list in an user property
        """
        user = api.user.get_current()
        bookmarks = user.getProperty("personal_bookmarks")
        if not bookmarks:
            return []
        try:
            return json.loads(bookmarks)
        except ValueError as e:
            logger.error("Unable to retrieve %s bookmarks for user: " % (user.getId()))
            logger.exception(e)
            return []

    def update_user_bookmarks(self, bookmarks):
        """
        set user bookmarks
        """
        user = api.user.get_current()
        user.setMemberProperties({"personal_bookmarks": json.dumps(bookmarks)})

    def update_bookmark(self, index, name, value):
        """
        update a selected bookmark with given infos
        """
        bookmarks = self.extract_user_bookmarks()
        try:
            bookmark = bookmarks[index]
        except IndexError:
            logger.error('Invalid index "%s" for personal bookmarks.' % index)
            return False
        if name not in bookmark:
            logger.error('"%s": invalid key.' % name)
            return False
        bookmark[name] = value
        self.update_user_bookmarks(bookmarks)
        return True

    def remove_bookmark(self, index):
        """delete a bookmark"""
        bookmarks = self.extract_user_bookmarks()
        bookmarks.pop(index)
        self.update_user_bookmarks(bookmarks)
        return True

    def add_bookmark(self, data):
        """add a bookmark"""
        bookmarks = self.extract_user_bookmarks()
        bookmarks.append(data)
        self.update_user_bookmarks(bookmarks)
        return True

    def already_bookmarked(self):
        """check if the current context is already in bookmarks"""
        uid = api.content.get_uuid(obj=self.context)
        filtered_bookmarks = [
            x for x in self.extract_user_bookmarks() if x.get("uid") == uid
        ]
        return len(filtered_bookmarks) > 0

    def format_bookmarks(self, type="internal", data=None):
        if not data:
            # internal bookmark
            return {
                "title": self.context.Title(),
                "uid": api.content.get_uuid(obj=self.context),
                "type": type,
            }
        else:
            return {"title": data.get("title"), "url": data.get("url"), "type": type}


class MyBookmarksView(BaseBookmarksView):

    """
    View that shows a list of personal bookmarks
    """

    def authenticator(self):
        """generate a csrf token"""
        return createToken()

    def get_bookmarks(self):
        """
        Return a list of saved bookmarks and default bookmarks
        """
        return self.parse_default_bookmarks() + self.parse_user_bookmarks()

    def parse_default_bookmarks(self):
        default_bookmarks = api.portal.get_registry_record(
            "default_bookmarks", interface=IMyBookmarksSettings
        )
        results = []
        for bookmark in default_bookmarks:
            try:
                title, path = bookmark.split("|")
            except ValueError:
                # malformed bookmark
                pass
            test_dict = {"uid": path, "title": title, "type": "default"}
            parsed_bookmark = self.parse_internal_bookmark(test_dict)
            if parsed_bookmark:
                results.append(parsed_bookmark)
            else:
                test_dict["url"] = path
                parsed_bookmark = self.parse_external_bookmark(test_dict)
                if parsed_bookmark:
                    results.append(parsed_bookmark)
        return results

    def parse_user_bookmarks(self):
        bookmarks = self.extract_user_bookmarks()
        if not bookmarks:
            return []
        formatted_bookmarks = []
        for bookmark in bookmarks:
            bookmark_dict = self.parse_bookmark(bookmark)
            if bookmark_dict:
                formatted_bookmarks.append(bookmark_dict)
        return formatted_bookmarks

    def parse_bookmark(self, bookmark):
        """return a formatted bookmark"""
        if bookmark.get("type") == "internal":
            return self.parse_internal_bookmark(bookmark)
        elif bookmark.get("type") == "external":
            return self.parse_external_bookmark(bookmark)
        return {}

    def parse_external_bookmark(self, bookmark):
        """ """
        url = bookmark.get("url")
        if not url:
            return {}
        return {
            "title": bookmark.get("title", url),
            "url": url,
            "type": bookmark.get("type"),
        }

    def parse_internal_bookmark(self, bookmark):
        """ """
        uid = bookmark.get("uid")
        item = api.content.get(UID=uid)
        if not item:
            return False
        return {
            "title": bookmark.get("title", item.Title()),
            "id": item.getId(),
            "url": item.absolute_url(),
            "description": item.Description(),
            "type": bookmark.get("type"),
        }


class MyBookmarksEditView(MyBookmarksView):

    """View for edit bookmarks"""

    def get_bookmarks(self):
        """
        Return a list of personal bookmarks and not default ones
        """
        return self.parse_user_bookmarks()


class ReorderView(BaseBookmarksView):

    """View for reorder bookmarks"""

    def __call__(self):
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            return json.dumps({"error": e.message})
        try:
            delta = int(self.request.form.get("delta", 0))
            original = int(self.request.form.get("original", 0))
        except ValueError:
            msg = translate(
                _(
                    "unable_sort_msg",
                    default=u"Unable to sort bookmarks. Invalid values.",
                ),
                context=self.request,
            )
            logger.error(msg)
            return json.dumps({"error": msg})
        if not delta:
            return
        if delta == original:
            return
        bookmarks = self.extract_user_bookmarks()
        newIndex = original + delta
        bookmarks.insert(newIndex, bookmarks.pop(original))
        self.update_user_bookmarks(bookmarks)


class EditBookmarkView(BaseBookmarksView):

    """ """

    def __call__(self):
        res_dict = {"field": self.request.form.get("fieldName")}
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            res_dict["success"] = False
            res_dict["message"] = e.message
            return json.dumps(res_dict)
        index_str, name = self.request.form.get("fieldName").split("-")
        if not index_str or not name:
            logger.error("Unable to edit bookmark. index or name not provided.")
            res_dict["success"] = False
            res_dict["message"] = translate(_("Error on saving"), context=self.request)
            return json.dumps(res_dict)
        try:
            index = int(index_str)
        except ValueError:
            msg = translate(
                _("Unable to edit bookmark. index is not a valid number."),
                context=self.request,
            )
            logger.error(msg)
            res_dict["success"] = False
            res_dict["message"] = msg
            return json.dumps(res_dict)
        res_dict["success"] = self.update_bookmark(
            index=index, name=name, value=self.request.form.get("value")
        )
        return json.dumps(res_dict)


class RemoveBookmarkView(BaseBookmarksView):

    """ """

    def __call__(self):
        res_dict = {"field": self.request.form.get("fieldName")}
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            res_dict["success"] = False
            res_dict["message"] = e.message
            return json.dumps(res_dict)
        index_str = self.request.form.get("index")
        try:
            index = int(index_str)
        except ValueError:
            msg = translate(
                _("Unable to edit bookmark. index is not a valid number."),
                context=self.request,
            )
            logger.error(msg)
            res_dict["success"] = False
            res_dict["message"] = msg
            return json.dumps(res_dict)
        res_dict["success"] = self.remove_bookmark(index=index)
        return json.dumps(res_dict)


class AddExternalBookmarkView(BaseBookmarksView):

    """ """

    def __call__(self):
        res_dict = {}
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            res_dict["success"] = False
            res_dict["message"] = e.message
            return json.dumps(res_dict)
        url = self.request.form.get("url")

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://{}".format(url)
        data = {
            "title": self.request.form.get("title"),
            "url": url,
            "type": self.request.form.get("type"),
        }

        res_dict["success"] = self.add_bookmark(data=data)
        return json.dumps(res_dict)


class AddBookmarkView(BaseBookmarksView):

    """ """

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        if self.already_bookmarked():
            message = translate(
                _(
                    "already_bookmarked_label",
                    default=u"This content is already bookmarked!",
                ),
                context=self.request,
            )
            api.portal.show_message(
                message=message, type="warning", request=self.request
            )
            return self.request.response.redirect(self.context.absolute_url())
        result = self.add_bookmark(data=self.format_bookmarks())
        message = ""
        msg_type = "info"
        if result:
            message = translate(
                _("bookmark_addedd_label", default=u"Bookmark added!"),
                context=self.request,
            )
        else:
            message = translate(
                _("bookmark_unable_add_label", default=u"Unable to add this bookmark."),
                context=self.request,
            )
            message = "error"
        api.portal.show_message(message=message, type=msg_type, request=self.request)
        return self.request.response.redirect(self.context.absolute_url())
