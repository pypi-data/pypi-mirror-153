##
# File: TaskParameter
# Date: 2-May-2015
#
# #
class TaskParameter(object):
    """Container of task parameter details"""

    def __init__(self):

        self.title = ""
        self.format = ""
        self.comment = ""
        self.question = ""
        self.options = []
        self.objects = []

    def addFormat(self, string):

        self.format = string

    def addComment(self, string):

        self.comment = string

    def addQuestion(self, string):

        self.question = string

    def addTitle(self, string):

        self.title = string

    def addOption(self, n, string):

        self.options.append([str(n), string])

    def addObject(self, string):

        self.objects.append(string)
