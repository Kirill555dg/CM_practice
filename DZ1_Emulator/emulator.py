import tarfile
import csv

from os.path import exists
from sys import argv
from terminal import Terminal
from gui import GUI


def read_config_file():
    if len(argv) < 2:
        print("Для корректного запуска эмулятора необходимо ввести: " 
              "\"py emulator.py <путь к конфигурационному файлу>\""
              "\n\nКонфигурационный файл должен иметь формат csv. Формат данных следующий:"
              "\narchive_path,<путь к архиву>"
              "\nlog_file_path,<путь к лог-файлу>"
              "\nstart_script_path,<путь к стартовому скрипту>")
        exit(1)

    config_file_path = argv[1]
    if not exists(config_file_path):
        print("Конфигурационный файл по заданному пути не найден.")
        exit(1)
    if not config_file_path.endswith(".csv"):
        print("Указанный конфигурационный файл задан в неверном формате.")
        exit(1)

    with open(config_file_path, newline='') as config_file:
        config_reader = csv.reader(config_file, delimiter=",", quotechar="|")
        names = ['archive_path', 'log_file_path', 'start_script_path']
        archive_path, log_file_path, start_script_path = None, None, None
        for row in config_reader:
            name = row[0]
            path = row[1]
            if not exists(path):
                print(f"Файл для {name} не найден.")
                exit(1)
            if name == "archive_path":
                if not tarfile.is_tarfile(path):
                    print("Для archive_path указан файл, не являющийся tar-архивом.")
                    exit(1)
                archive_path = path
            if name == "log_file_path":
                if not path.endswith(".xml"):
                    print("Для log_file_path указан неверный формат файла. Файл должен быть формата xml.")
                    exit(1)
                log_file_path = path
            if name == "start_script_path":
                start_script_path = path
            if name not in names:
                print("В конфигурационном файле присутствует неопознанный ключ: " + name)

        is_exit = False
        if archive_path is None:
            print("В конфигурационном файле не указан путь для tar-архива")
            is_exit = True
        if log_file_path is None:
            print("В конфигурационном файле не указан путь для лог-файла")
            is_exit = True
        if start_script_path is None:
            print("В конфигурационном файле не указан путь для стартового скрипта")
            is_exit = True

        if is_exit:
            exit(1)

        return archive_path,log_file_path,start_script_path

def execute_terminal(archive_path, log_file_path, start_script_path):
    terminal = Terminal(archive_path, log_file_path, start_script_path)
    gui = GUI(terminal)
    gui.run()
    return terminal

if __name__ == "__main__":
    paths = read_config_file()
    execute_terminal(*paths)

