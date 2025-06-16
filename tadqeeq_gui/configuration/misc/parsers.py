#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 12:29:34 2025

@author: mohamed
"""

from configparser import ConfigParser
from PyQt5.QtWidgets import QMessageBox
from .constants import ConfigurationKeys, DefaultValues

class ConfigurationFileParser(ConfigParser):
    
    def __init__(self, configuration_filepath, parent_widget=None):
        
        super().__init__()
        self.__configuration_filepath = configuration_filepath
        self.__parent_widget = parent_widget
        
        read_files = self.read(configuration_filepath)
        if not read_files:
            title = 'Configuration File Missing'
            text = f'The file "{configuration_filepath}" does not exist or could not be read.\nA new configuration file will be created.'
            if parent_widget is not None:
                QMessageBox.warning(parent_widget, title, text)
            else:
                print(f'[warning] {text}')
        
        modified = False
        
        modified |= self.ensure_keys(
            ConfigurationKeys.Paths.SECTION, 
            {
                ConfigurationKeys.Paths.IMAGES : DefaultValues.IMAGES,
                ConfigurationKeys.Paths.BOUNDING_BOXES : DefaultValues.BOUNDING_BOXES,
                ConfigurationKeys.Paths.SEMANTIC_SEGMENTS : DefaultValues.SEMANTIC_SEGMENTS,
            }
        )
        
        modified |= self.ensure_keys(
            ConfigurationKeys.Flags.SECTION, 
            {
                ConfigurationKeys.Flags.VOID_BACKGROUND : DefaultValues.VOID_BACKGROUND,
                ConfigurationKeys.Flags.AUTOSAVE : DefaultValues.AUTOSAVE,
            }
        )
        
        modified |= self.ensure_keys(
            ConfigurationKeys.Classes.SECTION, 
            {
                ConfigurationKeys.Classes.NAMES : DefaultValues.CLASS_NAMES,
            }
        )
        
        if modified:
            self.writeback_changes_to_disk()
            
    def ensure_keys(self, section:str, key_value_pairs:dict):
        modified = False
        if section not in self:
            self.add_section(section)
        for key, default_value in key_value_pairs.items():
            if key not in self[section]:
                self[section][key] = default_value
                modified = True
        return modified
    
    @property
    def parent_widget(self):
        return self.__parent_widget
    
    @property
    def configuration_filepath(self):
        return self.__configuration_filepath
    
    def writeback_changes_to_disk(self):
        try:
            with open(self.configuration_filepath, 'w') as configuration_file:
                self.write(configuration_file)
        except OSError as error:
            title = 'Error Writing Configuration'
            text = f'Failed to writeback configuration parameters:\n{error}'
            if self.parent_widget is not None:
                QMessageBox.critical(self.parent_widget, title, text)
            else:
                print(f'[error] {text}')