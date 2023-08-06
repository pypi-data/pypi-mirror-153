import configparser
from pathlib import Path

config_filepath = Path(__file__).parent.resolve() / 'config.ini'




class FilumConfig(object):
    def __init__(self):
        self.config_filepath = Path(__file__).parent.resolve() / 'config.ini'
        self.parser = configparser.ConfigParser(inline_comment_prefixes=';')


    def get_parser(self):

        # print(config_filepath)

        if not self.config_filepath.is_file():
            self.create_config()

        self.parser.read(self.config_filepath)

        return self.parser


    def create_config(self):
        config_content = '''
        [output]
            pager = true
            pager_colours = true  ; Only works if the pager supports colour. Otherwise change this to false.
        '''

        self.parser.read_string(config_content)

        with open(self.config_filepath, 'w') as config_file:
            self.parser.write(config_file)

if __name__ == '__main__':
    pass
