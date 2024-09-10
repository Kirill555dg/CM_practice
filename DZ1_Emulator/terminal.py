import tarfile

class Terminal:



    def __init__(self, archive: tarfile.TarFile, log_file, start_script):
        self.archive = archive