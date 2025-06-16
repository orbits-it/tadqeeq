#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 17:14:50 2025

@author: mohamed
"""

from PyQt5.QtCore import QObject, pyqtSignal, Qt
from ..models.Flags import Model
from ..misc.parsers import ConfigurationFileParser
from ..misc.constants import ConfigurationKeys
from ..misc.constants import BoolKey

class ViewModel(QObject):
    
    void_background_changed = pyqtSignal(bool)
    autosave_changed = pyqtSignal(bool)
    
    def __init__(self, configuration_file_parser:ConfigurationFileParser):
        super().__init__()
        self.__configuration_file_parser = configuration_file_parser
        self.__model = Model(
            configuration_file_parser[ConfigurationKeys.Flags.SECTION][ConfigurationKeys.Flags.AUTOSAVE].strip() == BoolKey.TRUE,
            configuration_file_parser[ConfigurationKeys.Flags.SECTION][ConfigurationKeys.Flags.VOID_BACKGROUND].strip() == BoolKey.TRUE,
        )
    
    @property
    def model(self):
        return self.__model
    
    @property
    def configuration_file_parser(self):
        return self.__configuration_file_parser
    
    @property
    def autosave(self):
        return self.model.autosave
    
    @autosave.setter
    def autosave(self, value:bool):
        if self.model.autosave != value:
            self.model.autosave = value
            self.configuration_file_parser[ConfigurationKeys.Flags.SECTION][ConfigurationKeys.Flags.AUTOSAVE] = BoolKey.TRUE if value else BoolKey.FALSE
            self.configuration_file_parser.writeback_changes_to_disk()
            self.autosave_changed.emit(value)
    
    @property
    def void_background(self):
        return self.model.void_background
    
    @void_background.setter
    def void_background(self, value:bool):
        if self.model.void_background != value:
            self.model.void_background = value
            self.configuration_file_parser[ConfigurationKeys.Flags.SECTION][ConfigurationKeys.Flags.VOID_BACKGROUND] = BoolKey.TRUE if value else BoolKey.FALSE
            self.configuration_file_parser.writeback_changes_to_disk()
            self.void_background_changed.emit(value)

    def on_autosave_state_change(self, state):
        self.autosave = state == Qt.Checked
    
    def on_void_background_state_change(self, state):
        self.void_background = state == Qt.Checked