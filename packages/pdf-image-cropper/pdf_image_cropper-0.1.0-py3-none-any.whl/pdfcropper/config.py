import yaml

from pdfcropper.utils.error import ErrorHandler

class LoadConfig:
    def __init__(self, cfname):
        self.default_error = 'all'
        self.default_dpi = 300
        self.default_logfile = 'pdfcropper.log'
        self.default_replace = False
        self.default_root_path = ''
        self.default_same_root = True

        self.cfname = cfname
        self.load_config()
        self.check_config()

    def load_config(self):
        with open(self.cfname, 'r') as f:
            self.config_dict = yaml.safe_load(f)
        

    def check_config(self):
        self.error = self.config_dict.get('error', self.default_error)
        self.dpi = self.config_dict.get('dpi', self.default_dpi)
        self.logfile = self.config_dict.get('logfile', self.default_logfile)
        self.replace = self.config_dict.get('replace', self.default_replace)
        self.root_path = self.config_dict.get('root_path', self.default_root_path)
        self.same_root = self.config_dict.get('same_root', self.default_same_root)
        e = ErrorHandler(error=self.error)

        self.pdf_files = self.config_dict.get('pdf_files', None)
        if not self.pdf_files:
            msg = ':pdf_files: not defined in config file'
            e.send(KeyError, msg)


        for item_number, task in enumerate(self.pdf_files):
            path = task.get('path', None)
            if not path:
                msg = f':pdf_files:{item_number}:path: not defined in config file'
                e.send(KeyError, msg)
                
            pages = task.get('pages', None)
            if not pages:
                msg = f':pdf_files:{item_number}:pages: not defined in config file'
                e.send(KeyError, msg)

            titles = task.get('titles', None)
            if not titles:
                msg = f':titles:{item_number}: not defined in config file'
                e.send(KeyError, msg)


    def check_path(self):
        # check main_path exits
        # check pdf_files path exists
        # check write access to output location
        # check logfile write access
        pass