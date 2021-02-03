import os


class FS:
    @staticmethod
    def create_dir(directory: str):
        try:
            os.mkdir(directory)
        except:
            return
