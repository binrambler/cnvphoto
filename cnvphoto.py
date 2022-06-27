import pathlib
from PIL import Image
import sys

CURR_DIR = pathlib.Path.cwd()
FILE_LOG = pathlib.Path(CURR_DIR, 'cnvphoto.log')
WORK_DIR = pathlib.Path('//z2/base/ftp/foto')
# макисмальная длина самой длинной стороны
MAX_LENGTH_OR_WIDTH = 640


def drawProgressBar(n_file, n_files, n_resize):
    sys.stdout.write(f'\rПросмотрено файлов: {n_file}/{n_files}, изменено файлов: {n_resize}')
    sys.stdout.flush()


def resize_file(dir):
    file_err = []
    n_files = len(list(pathlib.Path(dir).glob('*.jpg')))
    n_resize = 0
    n_file = 0
    for f in pathlib.Path(dir).glob('*.jpg'):
        n_file += 1
        try:
            image = Image.open(f)
            ratio = max(image.size) / MAX_LENGTH_OR_WIDTH
            # qq
            if ratio != 1:
                n_resize += 1
                size_new = tuple(map(lambda x: int(x / ratio), image.size))
                image_resize = image.resize(size_new)
                image_resize.save(f)
        except:
            file_err.append(f.name)
        drawProgressBar(n_file, n_files, n_resize)
    return n_files, n_resize, file_err


def log_write(n_files, n_resize, file_err):
    with open(FILE_LOG, 'w', encoding='cp1251') as f:
        f.write(f'Кол-во просмотренных файлов: {n_files}')
        f.write(f'\nКол-во измененных файлов: {n_resize}')
        f.write(f'\n\nФайлы, которые не удалось обработать:')
        for i in file_err:
            f.write(f'\n{i}')


if __name__ == "__main__":
    # удаляем лог-файл
    FILE_LOG.unlink(missing_ok=True)
    # изменяем разрешение файлов
    n_files, n_resize, file_err = resize_file(WORK_DIR)
    # файлы, которые не удалось обработать записываем в лог-файл
    log_write(n_files, n_resize, file_err)