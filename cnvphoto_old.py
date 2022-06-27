from pathlib import Path
from configparser import ConfigParser
from PIL import Image
import sys

CURR_DIR = Path.cwd()
FILE_INI = Path(CURR_DIR, 'cnvphoto.ini')
FILE_LOG = Path(CURR_DIR, 'cnvphoto.log')

WORK_DIR = CURR_DIR
MAX_LENGTH_OR_WIDTH = 0

def create_ini(file_ini):
    config = ConfigParser()
    config.add_section('Main')
    config.set('Main', 'work_dir', str(CURR_DIR))
    config.set('Main', 'max_length_or_width', '768')
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

def drawProgressBar(n_file, n_files, n_resize):
    sys.stdout.write(f'\rПросмотрено файлов: {n_file}/{n_files}, изменено файлов: {n_resize}')
    sys.stdout.flush()

def resize_file(dir):
    file_err = []
    n_files = len(list(Path(dir).glob('*.jpg')))
    n_resize = 0
    n_file = 0
    for f in Path(dir).glob('*.jpg'):
        n_file += 1
        try:
            image = Image.open(f)
            ratio = max(image.size) / MAX_LENGTH_OR_WIDTH
            if ratio != 1:
                n_resize += 1
                size_new = tuple(map(lambda x: int(x / ratio), image.size))
                image_resize = image.resize(size_new)
                image_resize.save(f)
        except:
            file_err.append(f.name)
        drawProgressBar(n_file, n_files, n_resize)
    return n_resize, file_err

def log_write(n_resize, file_err):
    with open(FILE_LOG, 'w', encoding='cp1251') as f:
        f.write(f'Кол-во измененных файлов: {n_resize}')
        f.write(f'\n\nФайлы, которые не удалось обработать:')
        for i in file_err:
            f.write(f'\n{i}')

read_ini()
n_resize, file_err = resize_file(WORK_DIR)
log_write(n_resize, file_err)
