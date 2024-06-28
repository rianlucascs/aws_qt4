from control.market_time import Time
time = Time.now()

from control.data import Data
from control.launch import Launch
from control.log import LogQt
from control.transation_log import TransationLog
from control.pdf_builder import PDFBuilder
from control.after_strategies import AfterStrategies
from control.risk import Risk
from control.email import Email
from control.utils import day_week, date_today
from time import sleep


class Activate:

    def __init__(self):
        data = Data.read()
        self.update = data[0]
        self.open = data[1]
        self.close = data[2]
        self.after = data[3]

    @property
    def protocol(self):
        
        if not day_week(date_today()) in ['Sábado', 'Domingo']:
            
            if time == self.update:
                Risk().protocol1()
                Launch("update").batch()
                LogQt('StartLoop UPDATE').startup

            if time == Time(self.open).decrement:
                Launch("open").batch()
                LogQt("StartLoop OPEN").startup

            if time == self.close:
                Launch("close").batch()
                LogQt("StartLoop CLOSE").startup

            if time == self.after:
                Launch("after").batch()
                TransationLog().save()
                PDFBuilder().create()
                AfterStrategies().main()
                sleep(120)
                Email().send()
                LogQt("StartLoop AFTER").startup

