#!python
#
# svn_mergefinder.py
#
# Description: given a specific branch, find all other branches which contain
#   a merge reference to the given branch.

# The inputs to the program will be the XML file generated by Subversion
# (e.g., "svn propget svn:mergeinfo svn://Chinook/EPS") and the URL of the
# branch in question, with or without the trailing slash (e.g.,
# svn://Chinook/EPS/branches/9.10/maintenance/base/).
#
# Originally I was planning to parse the logs for the given branch back to the
# copy operation, but there's no reason to bother with that.  Just look for
# where the branch has been merged *to*.
#
# The hard part is deciding how much of the branch URL to use.  Maybe I should
# define the preamble as svn://Chinook/EPS/branches, and use whatever follows
# as the pattern to match.

import sys
from xml.etree.ElementTree import ElementTree

DEBUG = False

class MergeFinder(object):
    def __init__(self, dat):
        self.datafile = dat

    def ugly_print(self, dict):
        # key is a string, values is a list of strings
        for key, values in dict.items():
            print "URL:", key
            for value in values:
                print "  PATH:", value
            print

    # Generates a dictionary with (key = target URL) and (value = list of
    # paths with their transactions).  It looks like this.  Note the empty
    # list at the end.
    #
    # {
    # 'svn://chinook/eps/branches/projects/merlin10/docs': [
    #    '/branches/9.10/maintenance/9.10.0112/docs:9636',
    #    '/branches/9.10/maintenance/PRN22180/docs:9424' ],
    #
    # 'svn://chinook/eps/branches/developers/danf/RadUpdate/src/server': [
    #    '/branches/9.7/Initial/base/src/server:6330-6336',
    #    '/branches/9.7/SP1/EB/DMCC/src/server:6683-7744',
    #    '/branches/9.7/SP1/base/src/server:6337-6682',
    #    '/branches/projects/DMCC09/src/server:7540-7863',
    #    '/branches/projects/July09/src/server:7600-8120',
    #    '/trunk/src/server:6542-7602' ],
    #
    # 'svn://chinook/eps/branches/projects/Dartboard09/setup/installs/Server': [],
    # }
    #
    def mergeinfo_dict(self):
#        tree = ElementTree(file=sys.argv[1])
        tree = ElementTree(file=self.datafile)
        parent_map = dict((c, p) for p in tree.getiterator() for c in p)
        self.mergeinfo_dict = {}
        for target in parent_map:   # parent (URL)
            for property in target: # child (paths and txns)
                _list = []
                for line in property.text.splitlines():
                    ln = line.strip()
                    if ln == "":
                        if DEBUG:
                            print "[DEBUG] skipping empty string"
                        pass
                    else:
                        _list.append(ln)
                # don't add URLs without PATHs
                if len(_list) > 0:
                    self.mergeinfo_dict[target.attrib['path']] = _list
        return self.mergeinfo_dict

    def mergefinder(self, path_str):
        # what does this look like?
        pass

mf = MergeFinder('mini.xml')
mf.ugly_print(mf.mergeinfo_dict())
#mergeinfo_dict()

