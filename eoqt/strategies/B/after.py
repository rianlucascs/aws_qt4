
from acess import Acess
from pdf_builder import PDFBuilder
from log import LogQT

class After(Acess):

    def main(self):
        PDFBuilder().main()

if __name__ == '__main__':
    LogQT('After start').startup
    After().main()
    LogQT('After end').startup