"""
>>> Esse arquivo deve ser executado em um terminal
>>> A referência para construção sera os arquivos da estrategia A 
>>> 

"""

from control.straton import StratOn

from os import mkdir, listdir
from os.path import exists
from control.utils import read_file, writing_file
from time import sleep

from sys import path
from control.log import LogQt

STRATS = [
    ['A', 1], 
    ['B', 2], 
    ['C', 3], 
    ['D', 4], 
    ['E', 5], 
    ['F', 6], 
    ['G', 7], 
    ['H', 8], 
    ['I', 9], 
    ['J', 10]
    ]

COPY = [
    'acess.py', 
    'after.py', 
    'close.py',    
    'build_info.py',
    'create_average_return.py',
    'create_drawdown.py',
    'create_sign.py',
    'create_images.py', 
    'data.py', 
    'log.py', 
    'model.py',
    'mt5_operations.py',
    'open.py',
    'pdf_builder.py',
    'update.py', 
    'utils.py',
    ] 

COPY_AND_EDIT = [
    'acess.py', 
    'model.py', 
    'utils.py'
    ]

NOT_COPY = [
    'features.py', 
    'settings.txt', 
    'after.bat', 
    'close.bat', 
    'open.bat', 
    'pdf_builder.bat', 
    'update.bat'
    ]

class InsertCode:
    """
    Escreve linhas de codigo especificas para cada arquivo
    """
    def __init__(self, file_ref, path_new_strat, name_new_strat=None):
        self.file_ref = file_ref
        self.path_new_strat = path_new_strat
        self.name_new_strat = name_new_strat

    @property
    def transformer(self):
        return self.file_ref.split('\n')

    def find_features_names(self):
        file = read_file(f'{self.path_new_strat}\\features.py')
        features = []
        for row in file.split('\n'):
            if 'def' in row:
                features.append(row.split(' ')[1].split('(')[0].replace('feature', ''))
        return features

    def model(self):
        file = ''
        key = False
        for row in self.transformer:
            row += '\n'
            if '{% builder start insert_features %}' in row:
                key = True
                function_names = self.find_features_names()
                for feature in function_names:
                    file += f'        data["{feature}"] = ft.feature{feature}(data["retorno"])\n'
                file += f'        return data\n'
            if '{% builder end insert_features %}' in row:
                key = False
            if key:
                row = ''
            file += row
        return file 
    
    def acess(self):
        file = ''
        for row in self.transformer:
            row += '\n'
            if '{% builder %}' in row:
                row = row.replace('A', self.name_new_strat)
            file += row
        return file
    
    def utils(self):
        # A função acess resolve a criação do utils.py
        return self.acess()

class FileBuilder:

    def __init__(self):
        self.stratname = StratOn().names_strategies()
        self.path_new_strat = f'{path[0]}\\strategies\\{self.name_new_strat}'
        self.path_strat_ref = f'{path[0]}\\strategies\\A'
        LogQt(f'FileBuilder create ({self.path_new_strat[-1]})').startup
        
    @property
    def name_new_strat(self): 
        name_last_strat = [ls for ls in STRATS if self.stratname[-1] in ls][0][1]
        name_new_strat = [ls for ls in STRATS if name_last_strat + 1 in ls][0][0]
        return name_new_strat

    def create_directory_and_files(self):
        if not exists(self.path_new_strat):
            mkdir(self.path_new_strat)
            print(20*'\n', f'\nDiretório cirado: {self.path_new_strat}')
        
        if not exists(path_settings:= f'{self.path_new_strat}\\settings.txt'):
            writing_file(path_settings, '')
            print('\nArquivo settings.txt criado\nAdicione as configurações da estratégia separadas por virguala e space ", "')
        
        if not exists(path_features:= f'{self.path_new_strat}\\features.py'):
            writing_file(path_features, '# Adicione aqui as features.')
            print(f'\nArquivo features.py criado\nAdicione as features...')
        return True
    
    def create_files(self):
        print(f'\nSTRAT: {self.name_new_strat}')
        for filename_ref in listdir(self.path_strat_ref):
            sleep(0.33)
            if filename_ref in COPY:
                path_file_ref = f'{self.path_strat_ref}\\{filename_ref}'
                file_ref = read_file(path_file_ref)

                if filename_ref in COPY_AND_EDIT:

                    match filename_ref:
                        case 'model.py':
                            file_ref = InsertCode(file_ref, self.path_new_strat).model()
                            writing_file(f'{self.path_new_strat}\\model.py', file_ref)
                            print('Create model.py')
                            LogQt(f'FileBuilder create ({self.path_new_strat[-1]})\\model.py').startup
    
                        case 'acess.py':
                            file_ref = InsertCode(file_ref, self.path_new_strat, self.name_new_strat).acess()
                            writing_file(f'{self.path_new_strat}\\acess.py', file_ref)
                            print('Create acess.py')
                            LogQt(f'FileBuilder create ({self.path_new_strat[-1]})\\acess.py').startup

                        case 'utils.py':
                            file_ref = InsertCode(file_ref, self.path_new_strat, self.name_new_strat).utils() 
                            writing_file(f'{self.path_new_strat}\\utils.py', file_ref)
                            print('Create utils.py')
                            LogQt(f'FileBuilder create ({self.path_new_strat[-1]})\\utils.py').startup

                else:
                    writing_file(f'{self.path_new_strat}\\{filename_ref}', file_ref)
                    print(f'Create {filename_ref}')
                    LogQt(f'FileBuilder create ({self.path_new_strat[-1]})\\{filename_ref}').startup

        print('Complet!')
        return True 
    
    # def update_all_files(self):
    #     for strat_on in StratOn().paths_strategies():
    #         print(strat_on)
    
    def check_cmd_bool(self, text, bool):
        if bool != None:
            while True:
                if input(text) == bool:
                    return True
        
    def check_cmd_question(self, text, quastions):
        while True:
            check = input(text)
            if check in quastions:
                return check

    def process(self):
        print(20*'\n')
        question = self.check_cmd_question('[ 1 ] Builder: ', ['1'])
        sleep(1)
        match question:
            case '1':
                if self.create_directory_and_files():
                    sleep(1)
                    if self.check_cmd_bool('\n\nDigitar "features.py" para continuar: ', 'features.py'):
                        sleep(1)
                        self.create_files()
            case '2':
                self.update_all_files()

