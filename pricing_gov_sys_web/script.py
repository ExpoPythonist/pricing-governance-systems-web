import os


class FolderScript(object):

    def __init__(self, dirpath):
        """init."""
        self.dirpath = dirpath
        self.init_or_create_folder()

    def __call__(self):
        """call."""
        pass

    def init_or_create_folder(self):
        """Initialize."""
        if not os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)
        return
