import tarfile
import xml.etree.ElementTree

class Terminal:
    def __init__(self, archive_path, log_file_path, start_script_path):
        self.archive_path = archive_path
        self.log_file_path = log_file_path
        self.start_script_path = start_script_path
        self.current_directory = ''
        self.running = False

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
        params = command.split()
        if params[0] == 'exit':
            self.running = False
            return

    def ls(self):
        pass

    def cd(self):
        pass

    def rev(self):
        pass

    def find(self):
        pass

    def date(self):
        pass
