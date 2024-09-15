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
        prmts = command.split()
        if prmts[0] == 'exit':
            self.running = False
            return
        elif prmts[0] == 'ls':
            self.ls(prmts[1:])
        elif prmts[0] == 'cd':
            self.cd(prmts[1:])
        elif prmts[0] == 'rev':
            self.rev(prmts[1:])
        elif prmts[0] == 'find':
            self.find(prmts[1:])
        elif prmts[0] == 'date':
            self.date(prmts[1:])

    def ls(self, prmts):
        pass

    def cd(self, prmts):
        pass

    def rev(self, prmts):
        pass

    def find(self, prmts):
        pass

    def date(self, prmts):
        if not prmts:
            delta = datetime.now() - self.past_time
            self.system_date += delta
            self.past_time = datetime.now()
            print(self.system_date.ctime())
            return

        if len(prmts) > 1:
            print(f"date: extra operand ‘{prmts[1]}’")
            return

        if len(prmts[0]) < 8:
            print(f"date: invalid date ‘{prmts[0]}’")
            return

        MM,DD,hh,mm = prmts[0][:2],prmts[0][2:4],prmts[0][4:6],prmts[0][6:8]
        ss = prmts[0][-2:] if prmts[0][-3] == '.' else '00'
        CCYY = prmts[0][8:-3] if prmts[0][-3] == '.' else prmts[0][8:]
        CC = CCYY[:2] if len(CCYY) == 4 else str(self.system_date.year)[:2]
        YY = CCYY[2:] if len(CCYY) == 4 else str(self.system_date.year)[2:] if len(CCYY) == 0 else CCYY

        try:
            self.system_date = datetime.strptime(f'{DD}.{MM}.{CC}{YY} {hh}:{mm}:{ss}', '%d.%m.%Y %H:%M:%S')
            self.past_time = datetime.now()
            print(self.system_date.ctime())
        except:
            print(f"date: invalid date ‘{prmts[0]}’")
