#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 09:16:11 2025

@author: mohamed
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from .views.Paths import View as PathsGroupBox
from .views.Flags import View as FlagsGroupBox
from .views.Classes import View as ClassesGroupBox
from .misc.parsers import ConfigurationFileParser

class Configuration(QWidget):
    
    def __init__(self, configuration_filepath):
        
        super().__init__()
        
        self.setWindowTitle('Tadqeeq - Image Annotator [Settings]')
        self.setFixedSize(500, 550)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(*[10]*4)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)
        
        self.__configuration_file_parser = ConfigurationFileParser(configuration_filepath, self)
        
        self.paths_groupbox = PathsGroupBox(self.configuration_file_parser)
        main_layout.addWidget(self.paths_groupbox)
        
        self.flags_groupbox = FlagsGroupBox(self.configuration_file_parser)
        main_layout.addWidget(self.flags_groupbox)
        
        self.classes_groupbox = ClassesGroupBox(self.configuration_file_parser)
        main_layout.addWidget(self.classes_groupbox)
        
        submit_layout = QHBoxLayout()
        self.__submit_button = QPushButton(QIcon.fromTheme('media-playback-start'), 'Start Annotator')
        self.submit_button.setFixedWidth(170)
        submit_layout.addStretch()
        submit_layout.addWidget(self.submit_button)
        
        main_layout.addStretch()
        main_layout.addLayout(submit_layout)
    
    @property
    def submit_button(self):
        return self.__submit_button
    
    @property
    def configuration_file_parser(self):
        return self.__configuration_file_parser
        