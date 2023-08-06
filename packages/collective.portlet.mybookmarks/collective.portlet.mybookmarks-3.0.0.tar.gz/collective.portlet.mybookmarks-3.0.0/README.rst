Introduction
============

A portlet that allows users to manage some personal bookmarks that can be site objects or external links.
The bookmarks are stored in two member properties.

Settings
========

Managers can set some default bookmarks that all users should view by default.

These bookmarks can be set in a portal_property called "*mybookmarks_properties*" and should be putted in a list field one per line, with the following sintax: *Title|url_or_path*.

For example:

``Common Page|/common_documents/common_page``

``google.com|http://www.google.com``

Usage
=====

If you want to add a site content to bookmarks list, just click on the "*bookmark*" link in document_actions.

To add a new external link, you need to fill the related form in the portlet.

To remove a bookmark, just click on delete icon.

Default bookmarks can't be removed by users.

Dependencies
============

This product has been tested on Plone 5.2 and Python 3.

For Plone 5 on python2, use 2.x versions and "python2" branch on github.

For Plone < 5, use 1.x versions and "plone4" branch on github.


Credits
=======

Developed with the support of `Regione Emilia Romagna`__; Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/
