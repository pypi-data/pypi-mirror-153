Changelog
=========

3.0.0 (2022-06-06)
------------------

- Drop python 2 and Plone < 5.2 support.
  [cekk, axaroth]
- Python 3 compatibility.
  [cekk, axaroth]


2.0.4 (2018-04-06)
------------------

- Always show edit bookmarks link in bookmarks list, also if the user doesn't
  have any bookmark.
  [cekk]

2.0.3 (2018-04-04)
------------------

- Don't show bookmark action on site root
  [cekk]
- Use standard slots in edit template
  [cekk]

2.0.2 (2017-11-20)
------------------

- Fix Italian translations.
  [cekk]


2.0.1 (2017-10-24)
------------------

- remove userschema.xml. Now additional field is added in the install script.
  In this way, we don't override existing ones.
  [cekk]

2.0.0 (11/10/2017)
------------------

- Removed plone_logs and used a proper logger [cekk]
- Plone 5 compatibility
  [cekk]

1.3.4 (2014-01-13)
------------------

- Fix accessibility stuffs [cekk]
- Refactored js that hide the form [cekk]


1.3.3 (2013-08-01)
------------------

- Now portlet title are correctly shown in the template [cekk]


1.3.2 (2013-07-17)
------------------

* Added separated permission to add the portlet [cekk]

1.3.1 (2013-07-08)
------------------

* Fixed portlet footer [cekk]

1.3.0 (2012-08-23)
------------------

* fix external bookmarks deletion [cekk]
* fix Plone 4 compatibility [cekk]
* initial release on pypi [cekk]

1.2.0 (2012-04-02)
------------------

* added default bookmarks configuration [cekk]

1.1.3 (2012-01-09)
------------------

* added "/view" to object bookmarks, to avoid automatic download of files [cekk]

1.1.2 (2011-07-08)
------------------

* added confirm delete view [cekk]

1.1.1 (2010-12-17)
------------------

* include package "plone.app.portlets" into zcml before registration of portlet [mirco]

1.1.0 (2010-12-03)
------------------

* fixed translation [cekk]
* deleting method [cekk]

1.0.0 (2010-11-22)
------------------

* Initial release
