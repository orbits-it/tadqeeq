#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 17:21:45 2025

@author: mohamed
"""

from PyQt5.QtCore import QObject, pyqtSignal
from ..models.Classes import Model
from ..misc.parsers import ConfigurationFileParser
from ..misc.constants import ConfigurationKeys

class ViewModel(QObject):
    
    names_changed = pyqtSignal(list)
    
    def __init__(self, configuration_file_parser:ConfigurationFileParser):
        super().__init__()
        self.__configuration_file_parser = configuration_file_parser
        lines = configuration_file_parser[ConfigurationKeys.Classes.SECTION][ConfigurationKeys.Classes.NAMES].split('\n')
        classnames = list(filter(bool, map(lambda line: line.strip(), lines)))
        self.__model = Model(classnames)
    
    @property
    def model(self):
        return self.__model
    
    @property
    def configuration_file_parser(self):
        return self.__configuration_file_parser
    
    @property
    def names(self):
        return self.model.names
    
    @names.setter
    def names(self, value:list[str]):
        if self.model.names != value:
            self.model.names = value
            self.names_changed.emit(value)
            self.configuration_file_parser[ConfigurationKeys.Classes.SECTION][ConfigurationKeys.Classes.NAMES] = '\n'.join(value)
            self.configuration_file_parser.writeback_changes_to_disk()
    
    def on_edit(self, index, text):#???
        text = text.strip()
        new_names = self.names.copy()
        if index < len(new_names):
            if text == self.names[index]:
                return False
            new_names[index] = text
        else:
            new_names.append(text)
        self.names = new_names
        return True
        
        