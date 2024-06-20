from control.batch_file_management import BatchFileManagement
from control.straton import StratOn

class AfterStrategies:
   
    def __init__(self):
      self.paths_strats = StratOn().paths_strategies()
   
    def main(self):

        # Atualizando "Strategy?_Report.pdf" de cada estrategia
        for path in self.paths_strats:
            BatchFileManagement(path, 'after').start()
        
        return None
    
