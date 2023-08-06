from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "collective.portlet.mybookmarks"

addUserBookmark = PROJECTNAME + ": Add User Bookmark"
delUserBookmark = PROJECTNAME + ": Remove User Bookmark"

setDefaultRoles(addUserBookmark, ('Manager',))
setDefaultRoles(delUserBookmark, ('Manager',))
