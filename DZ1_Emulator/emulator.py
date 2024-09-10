import os.path
import tarfile
import os.path
import csv
import xml
from os.path import exists

from sys import argv

archive_name = 'archive.tar'


def make_tar_archive():
    with tarfile.open(archive_name, 'w') as tar:
        tar.add("root", os.path.basename("root"))


def add_files_tar_archive():
    with tarfile.open(archive_name, 'a') as f:
        # f.makedir(f.tarinfo(), 'text/')
        f.add('text.txt', 'text/supertext/text.txt')
        # t = tarfile.TarInfo('mydir')
        # t.type = tarfile.DIRTYPE
        # f.addfile(t)
        # f.add('newdir', 'newdir')


def read_tar_archive():
    if tarfile.is_tarfile(archive_name):
        print('Архив найден')
        with tarfile.open(archive_name, 'r') as f:
            print('Файлы в архиве:')
            f.list()
            print("Members:")
            f.getmembers()
            print("Names:")
            f.getnames()


def execute():
    if len(argv) < 2:
        print("Для корректного запуска эмулятора необходимо ввести: " 
              "\"py emulator.py <путь к конфигурационному файлу>\""
              "\n\nКонфигурационный файл должен иметь формат csv. Формат данных следующий:"
              "\narchive_path,<путь к архиву>"
              "\nlog_file_path,<путь к лог-файлу>"
              "\nstart_script_path,<путь к стартовому скрипту>")
        return

    config_file_path = argv[1]
    if not exists(config_file_path):
        print("Конфигурационный файл по заданному пути не найден.")
        return
    if not config_file_path.endswith(".csv"):
        print("Указанный конфигурационный файл задан в неверном формате.")
        return

    with open(config_file_path, newline='') as config_file:
        config_reader = csv.reader(config_file, delimiter=",", quotechar="|")
        for row in config_reader:
            print(row)


if __name__ == "__main__":
    execute()
