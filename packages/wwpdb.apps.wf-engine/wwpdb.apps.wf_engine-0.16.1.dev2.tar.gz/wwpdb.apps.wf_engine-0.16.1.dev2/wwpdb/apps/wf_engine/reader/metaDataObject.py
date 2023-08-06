##
# File:    metaDataobject.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#
##

"""
holds the data information of basic workflow class
"""

__docformat__ = "restructuredtext en"
__author__ = "Tom Oldfield"
__email__ = "oldfield@ebi.ac.uk"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.24"


class metaDataObject:
    def __init__(self):

        self.ID = None
        self.versionMajor = None
        self.versionMinor = None
        self.versionAuthor = None
        self.name = None
        self.date = None
        self.description = None
        self.author = None

    def setID(self, did):
        self.ID = did

    def setVersionMajor(self, version):
        self.versionMajor = version

    def setVersionMinor(self, version):
        self.versionMinor = version

    def setDate(self, name):
        self.date = name

    def setAuthor(self, name):
        self.author = name

    def setName(self, name):
        self.name = name

    def setDescription(self, name):
        self.description = name

    def getID(self):
        return self.ID

    def getVersionMajor(self):
        return self.versionMajor

    def getVersionMinor(self):
        return self.versionMinor

    def getAuthor(self):
        return self.author

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description
