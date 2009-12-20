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

import os.path
import sys
from xml.etree.ElementTree import ElementTree

DEBUG = False

class MergeFinder(object):
    '''DOCSTRING'''
    def __init__(self, data_file, branch_str):
        '''DOCSTRING'''
        self.data_file = data_file
        self.mi_dict = {}
        self.branch_str = os.path.normpath(branch_str)

    def mergeinfo_dict(self):
        '''return all URLs with properties containing PATH text'''
        tree = ElementTree(file=self.data_file)
        parent_map = dict((c, p) for p in tree.getiterator() for c in p)
        for target in parent_map:   # URL
            for property in target: # paths
                _list = []
                # CAREFUL: this matches on whitespace, so it's affected by
                # the formatting of the file
                if property.text:
                    for line in property.text.splitlines():
                        ln = line.strip()
                        if ln == "":
                            if DEBUG:
                                print "[DEBUG] skipping empty string"
                        else:
                            _list.append(os.path.normpath(ln))
                    if len(_list) > 0:
                        self.mi_dict[target.attrib['path']] = _list
        return self.mi_dict

    # branch_str is the string to match against the values of mergeinfo_dict;
    # if a match is found, the key that contains the matching value is saved;
    # when the whole list is processed, the matching keys are returned.
    #def mergefinder(self, branch_str):
    def mergefinder(self):
        '''DOCSTRING'''
        path_list = []
        for url, paths in self.mi_dict.items():
            for path in paths:
                # NB: there is only one possible matching path per branch, so
                # this is sort of broken; TODO (in what way?); it needs to ...
                if self.branch_str in path:
                    path_list.append(url)
                    print "URL:", url
                    print "  PATH:", path
                    print
#        for path in path_list:
#            print path
        #return path_list

    def ugly_print(self, dict):
        '''DOCSTRING'''
        # key is a string, values is a list of strings
        for key, values in dict.items():
            print "URL:", key
            for value in values:
                print "  PATH:", value
            print

#            /branches/9.7/SP1/EB/DMCC/src/server:6683-7744
#mf = MergeFinder('mini.xml', r"branches/9.7/SP1/EB/DMCC")
#            /branches/9.10/maintenance/PRN22180/docs:9424
#mf = MergeFinder('mini.xml', r"branches/9.10/maintenance/PRN22180")
#mf = MergeFinder('mini.xml', r"branches\9.10\maintenance\PRN22180")
#mf = MergeFinder('mergeinfo_chinook_eps_branches.xml', r"branches\9.10\maintenance\PRN22180")
#mf = MergeFinder('mergeinfo_chinook_eps_branches.xml', r"branches")
#mf = MergeFinder('mini.xml', r"branches/9.10/maintenance/9.10.0001")
mf = MergeFinder('mini.xml', r"branches/9.10/maintenance/9.10.0112")
mf.mergeinfo_dict()
mf.mergefinder()

