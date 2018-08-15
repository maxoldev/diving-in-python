class FileReader:
    def __init__(self, path):
        assert isinstance(path, str)
        self.path = path

    def read(self):
        try:
            with open(self.path, "r") as f:
                content = f.read()
                return content
        except IOError:
            return ""

