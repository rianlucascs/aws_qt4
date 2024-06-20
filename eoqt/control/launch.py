from control.batch_file_management import BatchFileManagement
from control.straton import StratOn
from control.log import LogQt
from dataclasses import dataclass
from control.key_strat_on import keys

@dataclass
class Launch:

    filename: str

    def batch(self):
        for path_strat in StratOn().paths_strategies():
            if path_strat[-1] in keys:
                LogQt(f"Launch {self.filename} {path_strat[-1]}").startup
                batch = BatchFileManagement(path_strat, self.filename)
                batch.start()
                
        return None