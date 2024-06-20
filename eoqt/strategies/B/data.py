from utils import read_file
class Data:
    @staticmethod
    def read(path):
        return read_file(path).split(', ')
        