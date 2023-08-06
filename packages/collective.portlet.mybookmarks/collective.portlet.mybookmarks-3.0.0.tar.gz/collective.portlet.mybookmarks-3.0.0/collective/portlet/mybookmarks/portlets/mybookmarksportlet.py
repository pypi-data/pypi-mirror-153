from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.mybookmarks import _
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.interface import implementer
from plone import api
import json

import logging
logger = logging.getLogger(__name__)


class IMyBookmarksPortlet(IPortletDataProvider):
    """
    A portlet for user bookmarks
    """
    portletTitle = schema.TextLine(
        title=_("mybookmarks_portlet_title",
                default=u"Title of the portlet"),
        description=_("mybookmarks_portlet_title_help",
                      default=u"Insert the title of the portlet."),
        default=u'Bookmarks',
        required=True)


@implementer(IMyBookmarksPortlet)
class Assignment(base.Assignment):
    """
    Portlet assignment
    """

    def __init__(self, portletTitle=''):
        self.portletTitle = portletTitle

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self.portletTitle:
            return self.portletTitle
        return _("mybookmarks_portlet_title_default",
                 default="Personal bookmark")


class Renderer(base.Renderer):
    """
    Portlet renderer
    """

    _template = ViewPageTemplateFile('mybookmarksportlet.pt')
    render = _template

    @property
    def available(self):
        return not api.user.is_anonymous()


class AddForm(base.AddForm):
    """
    Portlet add form.
    """
    schema = IMyBookmarksPortlet

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """
    Portlet edit form.
    """
    schema = IMyBookmarksPortlet
