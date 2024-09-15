import tarfile
import xml.etree.ElementTree
import getpass
import platform

from datetime import datetime


class Terminal:
    def __init__(self, archive_path, log_file_path, start_script_path):
        self.running = False

        self.archive_path = archive_path
        self.log_file_path = log_file_path
        self.start_script_path = start_script_path

        self.working_directory = ''
        self.user = getpass.getuser()
        self.hostname = platform.node()

        self.system_date = datetime.now()
        self.past_time = datetime.now()

    def run(self):
        self.running = True
        while self.running:
            dir = '/' + self.working_directory if self.working_directory else ''
            info = f'{self.user}@{self.hostname}:~{dir}$ '
            try:
                command = input(info).strip()
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
            print("Не удалось прочесть стартовый скрипт")
            exit(1)

    def parse_cmd(self, command):
        prmtrs = command.split()
        if prmtrs[0] == 'exit':
            self.running = False
        elif prmtrs[0] == 'ls':
            self.ls(prmtrs[1:])
        elif prmtrs[0] == 'cd':
            self.cd(prmtrs[1:])
        elif prmtrs[0] == 'rev':
            self.rev(prmtrs[1:])
        elif prmtrs[0] == 'find':
            self.find(prmtrs[1:])
        elif prmtrs[0] == 'date':
            self.date(prmtrs[1:])
        else:
            print(f"Command '{prmtrs[0]}' not found.")

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
                    print(f"ls: cannot access '{name}': No such file or directory")
                    continue

                print(f'{name}:')
                names = ls_names(directory)
                if names: print(*names)
                if prmtrs: print()

            return

        directory = self.working_directory
        if len(prmtrs) == 1:
            directory = self.find_path(prmtrs[0])
            if directory is None:
                print(f"ls: cannot access '{prmtrs[0]}': No such file or directory")
                return

        names = ls_names(directory)
        if names: print(*names)



    def cd(self, prmtrs):
        if not prmtrs:
            self.working_directory = ''
            return

        if len(prmtrs) > 1:
            print("cd: too many arguments")
            return

        new_directory = self.find_path(prmtrs[0])
        if new_directory is None:
            print(f"cd: {prmtrs[0]}: No such file or directory")
            return
        if new_directory == '':
            self.working_directory = new_directory
            return

        with tarfile.open(self.archive_path, 'r') as tar:
            for member in tar:
                if member.name == new_directory:
                    if member.type != tarfile.DIRTYPE:
                        print(f"cd: {prmtrs[0]}: Not a directory")
                        return
                    self.working_directory = new_directory
                    return


    def rev(self, prmtrs):
        if not prmtrs:
            print(input()[::-1])

        while prmtrs:
            name = prmtrs.pop(0)
            path = self.find_path(name)
            if path is None:
                print(f"rev: cannot open {name}: No such file or directory")
                continue
            with tarfile.open(self.archive_path, 'r') as tar:
                for member in tar:
                    if member.name == path:
                        if member.type == tarfile.DIRTYPE:
                            print(f"rev: {name}: 0: Is a directory")
                            continue
                        file = tar.extractfile(member)
                        try:
                            for line in file.readlines():
                                print(line.decode(encoding='utf-8')[::-1])
                        except:
                            print(f"rev: {name}: the file cannot be read")


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
                    print(f"find: '{name}': No such file or directory")
                    continue

                names = find_names(directory)
                print(name)
                if name[-1] == '/':
                    name = name[:-1]
                for path in names:
                    print(name + path)

            return

        name = prmtrs[0] if prmtrs else '.'
        directory = self.find_path(name)
        if directory is None:
            print(f"find: '{prmtrs[0]}': No such file or directory")
            return

        names = find_names(directory)
        print(name)
        if name[-1] == '/':
            name = name[:-1]
        for path in names:
            print(name + path)


    def date(self, prmtrs):
        if not prmtrs:
            delta = datetime.now() - self.past_time
            self.system_date += delta
            self.past_time = datetime.now()
            print(self.system_date.ctime())
            return

        if len(prmtrs) > 1:
            print(f"date: extra operand ‘{prmtrs[1]}’")
            return

        try:
            MM,DD,hh,mm = prmtrs[0][:2],prmtrs[0][2:4],prmtrs[0][4:6],prmtrs[0][6:8]
            ss = prmtrs[0][-2:] if prmtrs[0][-3] == '.' else '00'
            CCYY = prmtrs[0][8:-3] if prmtrs[0][-3] == '.' else prmtrs[0][8:]
            CC = CCYY[:2] if len(CCYY) == 4 else str(self.system_date.year)[:2]
            YY = CCYY[2:] if len(CCYY) == 4 else str(self.system_date.year)[2:] if len(CCYY) == 0 else CCYY

            self.system_date = datetime.strptime(f'{DD}.{MM}.{CC}{YY} {hh}:{mm}:{ss}', '%d.%m.%Y %H:%M:%S')
            self.past_time = datetime.now()
            print(self.system_date.ctime())
        except:
            print(f"date: invalid date ‘{prmtrs[0]}’")
