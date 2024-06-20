
from datetime import datetime
from pandas import Timestamp
from datetime import timedelta

class Time:

    def __init__(self, time):
        self.time = time

    @staticmethod
    def now():
        return datetime.now().strftime('%H:%M') + ':00'
    
    @property
    def decrement(self):
        return str(Timestamp(self.time) - timedelta(minutes=3))[11:]

    


        
     
