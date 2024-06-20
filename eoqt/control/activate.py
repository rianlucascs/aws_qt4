
from control.data import Data
from control.market_time import Time
from control.launch import Launch
from control.log import LogQt
from control.transation_log import TransationLog
from control.pdf_builder import PDFBuilder
from control.after_strategies import AfterStrategies
from control.risk import Risk
from control.email import Email

class Activate:

    def __init__(self):
        self.time = Time.now()
        data = Data.read()
        self.update = data[0]
        self.open = data[1]
        self.close = data[2]
        self.after = data[3]

    @property
    def protocol(self):

        if self.time == self.update:
            Launch("update").batch()
            Risk().protocol1()
            LogQt('StartLoop UPDATE').startup

        if self.time == Time(self.open).decrement:
            Launch("open").batch()
            LogQt("StartLoop OPEN").startup

        if self.time == self.close:
            Launch("close").batch()
            LogQt("StartLoop CLOSE").startup

        if self.time == self.after:
            Launch("after").batch()
            TransationLog().save()
            PDFBuilder().create()
            AfterStrategies().main()
            Email().send()
            LogQt("StartLoop AFTER").startup
