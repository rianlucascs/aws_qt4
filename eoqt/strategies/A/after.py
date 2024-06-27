
from pdf_builder import PDFBuilder
from log import LogQT

if __name__ == '__main__':
    LogQT('After start').startup
    PDFBuilder().main()
    LogQT('After end').startup