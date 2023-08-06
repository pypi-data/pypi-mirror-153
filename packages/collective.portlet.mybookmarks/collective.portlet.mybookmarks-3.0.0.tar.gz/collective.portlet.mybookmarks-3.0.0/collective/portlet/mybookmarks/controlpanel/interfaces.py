# -*- coding: utf-8 -*-

from collective.portlet.mybookmarks import _
from zope import schema
from zope.interface import Interface


class IMyBookmarksSettings(Interface):
    """Single entry for the editable menu configuration
    """

    default_bookmarks = schema.Tuple(
        title=_(
            'default_bookmarks_label',
            default=u'Default bookmarks'),
        description=_(
            'default_bookmarks_help',
            default=u"Insert a list of default bookmarks visible to all users "
                    "in the following format: \"title|path_to_resource_or_url\"."
                    " One per line."),
        value_type=schema.TextLine(),
        required=True,
        default=(),
        missing_value=(),
    )
