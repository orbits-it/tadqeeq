# -*- coding: utf-8 -*-

from configparser import ConfigParser
from pathlib import Path

class INIParser(ConfigParser):
    
    _current_dirpath = Path(__file__).parent
    
    def __init__(self):
        super().__init__()
        self.read()
    
    def read(self):
        try:
            super().read(self.filepath)
        except FileNotFoundError:
            raise AttributeError(f'"config.ini" is not found in "{self._current_dirpath}"')
        
    def write(self):
        with open(self.filepath, 'w') as file:
            super().write(file, space_around_delimiters=True)
            
    def getlist(self, section, option):
        return [line.strip() for line in self.get(section, option).split('\n') if line.strip()]
        
    @property
    def filepath(self):
        return self._current_dirpath / 'config.ini'