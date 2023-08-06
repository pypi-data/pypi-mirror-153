# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from collective.portlet.mybookmarks import _
from collective.portlet.mybookmarks.controlpanel.interfaces import IMyBookmarksSettings


class MyBookmarksSettingsEditForm(controlpanel.RegistryEditForm):
    """settings form."""
    schema = IMyBookmarksSettings
    id = "MyBookmarksSettingsEditForm"
    label = _(
        "mybookmarks_controlpanel_title",
        default=u"My Bookmarks settings")
    description = u""


class MyBookmarksSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel.
    """
    form = MyBookmarksSettingsEditForm
