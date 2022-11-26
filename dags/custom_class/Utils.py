class Utils:
    def __init__(self, file_path: str, args):
        self.file_path = file_path
        self.args = args

    def get_file_path(self):
        return self.file_path

    def get_args(self):
        return self.args
