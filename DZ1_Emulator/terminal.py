import tarfile
import xml.etree.ElementTree as ET
import getpass
import platform
import gui

from datetime import datetime


class Terminal:
    def __init__(self, archive_path, log_file_path, start_script_path):
        self.running = False

        try:
            self.log_file = ET.parse(log_file_path)
            self.xml = ET.SubElement(self.log_file.getroot(), "log_info_" + datetime.now().isoformat(timespec='minutes').replace(':','.'))
        except:
            print("Лог-файл формата xml открыть не удалось. Проверьте корректность содержания файла.")
            exit(1)

        self.log_file_path = log_file_path
        self.archive_path = archive_path
        self.start_script_path = start_script_path

        self.working_directory = ''
        self.user = getpass.getuser()
        self.hostname = platform.node()

        self.system_date = datetime.now()
        self.past_time = datetime.now()

        self.gui = None

    def write(self, message):
        if self.gui is None:
            print(message)
        else:
            self.gui.write(message + "\n")

    def enableGUI(self, gui):
        self.gui = gui
        dir = '/' + self.working_directory if self.working_directory else ''
        info = f'{self.user}@{self.hostname}:~{dir}$ '
        self.gui.write(info)

    def run(self):
        self.running = True
        self.execute_start_script()
        while self.running:
            dir = '/' + self.working_directory if self.working_directory else ''
            info = f'{self.user}@{self.hostname}:~{dir}$ '
            print(info)
            try:
                command = input().strip()
            except:
                exit(1)
            if len(command) > 0:
                self.parse_cmd(command)
        print("Stop running...")

    def execute_start_script(self):
        try:
            with open(self.start_script_path, 'r') as start_script:
                for command in start_script.readlines():
                    command = command.strip()
                    if len(command) > 0:
                        self.parse_cmd(command)
        except:
            self.write("Не удалось прочесть стартовый скрипт")
            exit(1)

    def parse_cmd(self, command):
        prmtrs = command.split()
        self.gui.write(' '.join(prmtrs) + '\n')
        if prmtrs:
            if prmtrs[0] == 'exit':
                self.running = False
                log = ET.SubElement(self.xml, 'command')
                log.text = prmtrs[0]
                self.log_file.write(self.log_file_path)
                if gui: self.gui.disable()
            elif prmtrs[0] == 'ls':
                self.ls(prmtrs[1:])
                log = ET.SubElement(self.xml, 'command')
                log.text = prmtrs[0]
                log.attrib['parameters'] = ' '.join(prmtrs[1:])
            elif prmtrs[0] == 'cd':
                self.cd(prmtrs[1:])
                log = ET.SubElement(self.xml, 'command')
                log.text = prmtrs[0]
                log.attrib['parameters'] = ' '.join(prmtrs[1:])
            elif prmtrs[0] == 'rev':
                self.rev(prmtrs[1:])
                log = ET.SubElement(self.xml, 'command')
                log.text = prmtrs[0]
                log.attrib['parameters'] = ' '.join(prmtrs[1:])
            elif prmtrs[0] == 'find':
                self.find(prmtrs[1:])
                log = ET.SubElement(self.xml, 'command')
                log.text = prmtrs[0]
                log.attrib['parameters'] = ' '.join(prmtrs[1:])
            elif prmtrs[0] == 'date':
                self.date(prmtrs[1:])
                log = ET.SubElement(self.xml, 'command')
                log.text = prmtrs[0]
                log.attrib['parameters'] = ' '.join(prmtrs[1:])
            else:
                log = ET.SubElement(self.xml, 'command')
                log.text = prmtrs[0]
                log.attrib['success'] = 'false'
                self.write(f"Command '{prmtrs[0]}' not found.")
        if (prmtrs[0] != 'rev') or (prmtrs[1:]):
            dir = '/' + self.working_directory if self.working_directory else ''
            info = f'{self.user}@{self.hostname}:~{dir}$ '
            self.gui.write(info)

    def find_path(self, path):
        current_path = self.working_directory

        while '//' in path:
            path = path.replace('//', '/')
        if path[-1] == '/':
            path = path[:-1]

        path = path.split('/')
        if path[0] == '/':
            current_path = ''
            path.pop(0)

        while path:
            name = path.pop(0)
            if name == '.':
                current_path = self.working_directory
            elif name == '..':
                index = current_path.rfind('/')
                if index > -1:
                    current_path = current_path[:index]
                else:
                    current_path = ''
            else:
                if current_path:
                    current_path += '/' + name
                else:
                    current_path += name
                with tarfile.open(self.archive_path, 'r') as tar:
                    paths = [member.name for member in tar]
                    if current_path not in paths:
                        return None
        return current_path

    def ls(self, prmtrs):
        def ls_names(directory):
            names = set()
            with tarfile.open(self.archive_path, 'r') as tar:
                for member in tar:
                    name = member.name
                    if name.find(directory) > -1:
                        if name == directory:
                            if member.type == tarfile.DIRTYPE:
                                continue
                            return (directory[directory.rfind('/') + 1:],)

                        name = name[len(directory):]
                        if name[0] == '/':
                            name = name[1:]
                        erase = name.find('/')
                        if erase > -1:
                            name = name[:name.find('/')]
                        names.add(name)
            return names

        if len(prmtrs) > 1:
            prmtrs.sort()
            while prmtrs:
                directory = self.find_path(prmtrs[0])
                name = prmtrs.pop(0)
                if directory is None:
                    self.write(f"ls: cannot access '{name}': No such file or directory")
                    continue

                self.write(f'{name}:')
                names = ls_names(directory)
                if names: self.write(' '.join(names))
                if prmtrs: self.write('')

            return

        directory = self.working_directory
        if len(prmtrs) == 1:
            directory = self.find_path(prmtrs[0])
            if directory is None:
                self.write(f"ls: cannot access '{prmtrs[0]}': No such file or directory")
                return

        names = ls_names(directory)
        if names: self.write(' '.join(names))



    def cd(self, prmtrs):
        if not prmtrs:
            self.working_directory = ''
            return

        if len(prmtrs) > 1:
            self.write("cd: too many arguments")
            return

        new_directory = self.find_path(prmtrs[0])
        if new_directory is None:
            self.write(f"cd: {prmtrs[0]}: No such file or directory")
            return
        if new_directory == '':
            self.working_directory = new_directory
            return

        with tarfile.open(self.archive_path, 'r') as tar:
            for member in tar:
                if member.name == new_directory:
                    if member.type != tarfile.DIRTYPE:
                        self.write(f"cd: {prmtrs[0]}: Not a directory")
                        return
                    self.working_directory = new_directory
                    return

    def rev_gui(self, text):
        self.write(text)
        self.write(text[::-1])
        dir = '/' + self.working_directory if self.working_directory else ''
        info = f'{self.user}@{self.hostname}:~{dir}$ '
        self.gui.write(info)

    def rev(self, prmtrs):
        if not prmtrs:
            if gui:
                self.gui.get_text()
            else:
                self.write(input()[::-1])

        while prmtrs:
            name = prmtrs.pop(0)
            path = self.find_path(name)
            if path is None:
                self.write(f"rev: cannot open {name}: No such file or directory")
                continue
            with tarfile.open(self.archive_path, 'r') as tar:
                for member in tar:
                    if member.name == path:
                        if member.type == tarfile.DIRTYPE:
                            self.write(f"rev: {name}: 0: Is a directory")
                            continue
                        file = tar.extractfile(member)
                        try:
                            for line in file.readlines():
                                self.write(line.decode(encoding='utf-8')[::-1])
                        except:
                            self.write(f"rev: {name}: the file cannot be read")


    def find(self, prmtrs):
        def find_names(directory):
            names = []
            with tarfile.open(self.archive_path, 'r') as tar:
                for member in tar:
                    name = member.name
                    if name == directory:
                        continue
                    if name.find(directory) > -1:
                        name = name[len(directory):]
                        if name[0] != '/':
                            name = '/' + name
                        names.append(name)
            return names

        if len(prmtrs) > 1:
            while prmtrs:
                name = prmtrs.pop(0)
                directory = self.find_path(name)
                if directory is None:
                    self.write(f"find: '{name}': No such file or directory")
                    continue

                names = find_names(directory)
                self.write(name)
                if name[-1] == '/':
                    name = name[:-1]
                for path in names:
                    self.write(name + path)

            return

        name = prmtrs[0] if prmtrs else '.'
        directory = self.find_path(name)
        if directory is None:
            self.write(f"find: '{prmtrs[0]}': No such file or directory")
            return

        names = find_names(directory)
        self.write(name)
        if name[-1] == '/':
            name = name[:-1]
        for path in names:
            self.write(name + path)


    def date(self, prmtrs):
        if not prmtrs:
            delta = datetime.now() - self.past_time
            self.system_date += delta
            self.past_time = datetime.now()
            self.write(self.system_date.ctime())
            return

        if len(prmtrs) > 1:
            self.write(f"date: extra operand ‘{prmtrs[1]}’")
            return

        try:
            MM,DD,hh,mm = prmtrs[0][:2],prmtrs[0][2:4],prmtrs[0][4:6],prmtrs[0][6:8]
            ss = prmtrs[0][-2:] if prmtrs[0][-3] == '.' else '00'
            CCYY = prmtrs[0][8:-3] if prmtrs[0][-3] == '.' else prmtrs[0][8:]
            CC = CCYY[:2] if len(CCYY) == 4 else str(self.system_date.year)[:2]
            YY = CCYY[2:] if len(CCYY) == 4 else str(self.system_date.year)[2:] if len(CCYY) == 0 else CCYY

            self.system_date = datetime.strptime(f'{DD}.{MM}.{CC}{YY} {hh}:{mm}:{ss}', '%d.%m.%Y %H:%M:%S')
            self.past_time = datetime.now()
            self.write(self.system_date.ctime())
        except:
            self.write(f"date: invalid date ‘{prmtrs[0]}’")
