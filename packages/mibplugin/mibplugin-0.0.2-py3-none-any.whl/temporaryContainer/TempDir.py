import tempfile
class TempDir:

    def __init__(self):

        self.temp_dir = tempfile.TemporaryDirectory(suffix='mibfilepath')
        self._tempDir = self.temp_dir.name

    def get_full_path(self):

        return self._tempDir

    def cleanupDir(self):
        self.temp_dir.cleanup()


