# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)
default_profile = 'profile-collective.portlet.mybookmarks:default'


def to_3100(context):
    """
    Upgrades to version 3100
    """
    logger.info('Upgrading collective.portlet.mybookmarks to version 1')
    context.runImportStepFromProfile(default_profile, 'actions')
    logger.info('Fix add bookmark condition')
