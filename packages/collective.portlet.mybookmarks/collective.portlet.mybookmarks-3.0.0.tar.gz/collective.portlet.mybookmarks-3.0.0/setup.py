from setuptools import setup, find_packages
import os

version = "3.0.0"

setup(
    name="collective.portlet.mybookmarks",
    version=version,
    description="A portlet that allows to store some internal and external bookmarks for users",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="bookmark portlet user",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="https://github.com/RedTurtle/collective.portlet.mybookmarks",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.portlet.mybookmarks",
        "Source": "https://github.com/RedTurtle/collective.portlet.mybookmarks",
        "Tracker": "https://github.com/RedTurtle/collective.portlet.mybookmarks/issues",
    },
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective", "collective.portlet"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
    ],
    entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
