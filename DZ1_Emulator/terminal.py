import os
import tarfile
import xml.etree.ElementTree

import getpass

from datetime import datetime



#def make_tar_archive():
#    with tarfile.open(archive_name, 'w') as tar:
#        tar.add("root", os.path.basename("root"))
#
#
#def add_files_tar_archive():
#    with tarfile.open(archive_name, 'a') as f:
#        # f.makedir(f.tarinfo(), 'text/')
#        f.add('text.txt', 'text/supertext/text.txt')
#        # t = tarfile.TarInfo('mydir')
#        # t.type = tarfile.DIRTYPE
#        # f.addfile(t)
#        # f.add('newdir', 'newdir')
#
#
#def read_tar_archive():
#    if tarfile.is_tarfile(archive_name):
#        print('Архив найден')
#        with tarfile.open(archive_name, 'r') as f:
#            print('Файлы в архиве:')
#            f.list()
#            print("Members:")
#            f.getmembers()
#            print("Names:")
#            f.getnames()




class Terminal:
    def __init__(self, archive_path, log_file_path, start_script_path):
        self.archive_path = archive_path
        self.log_file_path = log_file_path
        self.start_script_path = start_script_path
        self.current_directory = ''
        self.running = False
        self.user = getpass.getuser()
        self.system_date = datetime.now()
        self.past_time = datetime.now()

    def run(self):
        self.running = True
        while self.running:
            return

    def execute_start_script(self):
        with open(self.start_script_path, 'r') as start_script:
            for command in start_script.readlines():
                if len(command) > 0:
                    self.parse_cmd(command.strip())

    def parse_cmd(self, command):
        prmtrs = command.split()
        if prmtrs[0] == 'exit':
            self.running = False
            return
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

    def ls(self, prmtrs):
        pass

    def cd(self, prmtrs):
        pass

    def rev(self, prmtrs):
        pass

    def find(self, prmtrs):
        pass

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

        if len(prmtrs[0]) < 8:
            print(f"date: invalid date ‘{prmtrs[0]}’")
            return

        MM,DD,hh,mm = prmtrs[0][:2],prmtrs[0][2:4],prmtrs[0][4:6],prmtrs[0][6:8]
        ss = prmtrs[0][-2:] if prmtrs[0][-3] == '.' else '00'
        CCYY = prmtrs[0][8:-3] if prmtrs[0][-3] == '.' else prmtrs[0][8:]
        CC = CCYY[:2] if len(CCYY) == 4 else str(self.system_date.year)[:2]
        YY = CCYY[2:] if len(CCYY) == 4 else str(self.system_date.year)[2:] if len(CCYY) == 0 else CCYY

        try:
            self.system_date = datetime.strptime(f'{DD}.{MM}.{CC}{YY} {hh}:{mm}:{ss}', '%d.%m.%Y %H:%M:%S')
            self.past_time = datetime.now()
            print(self.system_date.ctime())
        except:
            print(f"date: invalid date ‘{prmtrs[0]}’")
