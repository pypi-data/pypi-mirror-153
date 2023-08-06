import os
import shutil

class Remover:

    def __init__(self):
        self.removed = []


    def remove(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    def find_and_remove(self, path):
        if path.is_file():
            size = os.path.getsize(path)
            if size == 0:
                self.removed.append(str(path))
                self.remove(path)
                print(f"# {len(self.removed)}: {str(path)}")
        elif path.is_dir():
            try:
                for item in path.iterdir():
                    self.find_and_remove(item)
            except PermissionError:
                print(f"Access denied: {str(path)}")
