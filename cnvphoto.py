from pathlib import Path
from configparser import ConfigParser
from PIL import Image

CURR_DIR = Path.cwd()
FILE_INI = Path(CURR_DIR, 'cnvphoto.ini')

WORK_DIR = CURR_DIR
MAX_LENGTH_OR_WIDTH = 0

def create_ini(file_ini):
    config = ConfigParser()
    config.add_section('Main')
    config.set('Main', 'work_dir', str(CURR_DIR))
    config.set('Main', 'max_length_or_width', '800')
    with open(file_ini, 'w') as f:
        config.write(f)

def read_ini():
    if not FILE_INI.exists():
        print('Нет файла с настройками программы:', FILE_INI)
        create_ini(FILE_INI)
        return
    config = ConfigParser()
    config.read(FILE_INI)
    global WORK_DIR, MAX_LENGTH_OR_WIDTH
    WORK_DIR = config.get('Main', 'work_dir')
    MAX_LENGTH_OR_WIDTH = int(config.get('Main', 'max_length_or_width'))

def resize_file(dir):
    for f in Path(dir).glob('*.jpg'):
        image = Image.open(f)
        ratio = max(image.size) / MAX_LENGTH_OR_WIDTH
        if ratio != 1:
            size_new = tuple(map(lambda x: int(x / ratio), image.size))
            print(f'Меняем разрешение файла {f.name}: {image.size} --> {size_new}')
            image_resize = image.resize(size_new)
            image_resize.save(f)

read_ini()
resize_file(WORK_DIR)
