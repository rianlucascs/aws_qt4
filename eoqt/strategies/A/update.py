

from create_images import CreateImages
from create_sign import CreateSign
from create_drawdown import DrawDownMin
from create_average_return import AverageReturn
from log import LogQT
    
if __name__ == '__main__':
    LogQT('Update start').startup
    [CreateImages().writing_images_returns_line(i) for i in [1, 2]]
    CreateSign().writing_file_sign()
    DrawDownMin.create()
    AverageReturn.create()
    LogQT('Update end').startup