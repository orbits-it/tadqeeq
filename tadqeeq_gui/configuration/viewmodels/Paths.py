#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 16:33:36 2025

@author: mohamed
"""

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from ..models.Paths import Model
from ..misc.parsers import ConfigurationFileParser
from ..misc.constants import ConfigurationKeys
import re
import os

class ViewModel(QObject):
    
    images_changed = pyqtSignal(str)
    bounding_boxes_changed = pyqtSignal(str)
    semantic_segments_changed = pyqtSignal(str)
    
    def __init__(self, configuration_file_parser:ConfigurationFileParser):
        super().__init__()
        self.__configuration_file_parser = configuration_file_parser
        self.__model = Model(configuration_file_parser[ConfigurationKeys.Paths.SECTION][ConfigurationKeys.Paths.IMAGES],
                             configuration_file_parser[ConfigurationKeys.Paths.SECTION][ConfigurationKeys.Paths.BOUNDING_BOXES], 
                             configuration_file_parser[ConfigurationKeys.Paths.SECTION][ConfigurationKeys.Paths.SEMANTIC_SEGMENTS])
    
    @property
    def configuration_file_parser(self):
        return self.__configuration_file_parser
    
    @property
    def model(self):
        return self.__model
    
    @property
    def images(self):
        return self.model.images
    
    @images.setter
    def images(self, value:str):
        if self.model.images != value:
            self.model.images = value
            self.configuration_file_parser[ConfigurationKeys.Paths.SECTION][ConfigurationKeys.Paths.IMAGES] = value
            self.configuration_file_parser.writeback_changes_to_disk()
            self.images_changed.emit(value)
        
    @property
    def bounding_boxes(self):
        return self.model.bounding_boxes
    
    @bounding_boxes.setter
    def bounding_boxes(self, value:str):
        if self.model.bounding_boxes != value:
            self.model.bounding_boxes = value
            self.configuration_file_parser[ConfigurationKeys.Paths.SECTION][ConfigurationKeys.Paths.BOUNDING_BOXES] = value
            self.configuration_file_parser.writeback_changes_to_disk()
            self.bounding_boxes_changed.emit(value)
            
    @property
    def semantic_segments(self):
        return self.model.semantic_segments
    
    @semantic_segments.setter
    def semantic_segments(self, value:str):
        if self.model.semantic_segments != value:
            self.model.semantic_segments = value
            self.configuration_file_parser[ConfigurationKeys.Paths.SECTION][ConfigurationKeys.Paths.SEMANTIC_SEGMENTS] = value
            self.configuration_file_parser.writeback_changes_to_disk()
            self.semantic_segments_changed.emit(value)
            
    @staticmethod
    def check_subject(subject:str):
        valid_subjects = {ConfigurationKeys.Paths.IMAGES,
                          ConfigurationKeys.Paths.BOUNDING_BOXES,
                          ConfigurationKeys.Paths.SEMANTIC_SEGMENTS}
        if subject not in valid_subjects:
            raise ValueError(f'The parameter `subject` should be one of the following: {tuple(valid_subjects)}')
    
    def on_edit(self, subject:str, text:str):
        self.check_subject(subject)
        text = os.path.normpath(text)
        match subject:
            case ConfigurationKeys.Paths.IMAGES:
                self.images = text
            case ConfigurationKeys.Paths.BOUNDING_BOXES:
                self.bounding_boxes = text
            case ConfigurationKeys.Paths.SEMANTIC_SEGMENTS:
                self.semantic_segments = text
        
    def browse_for_directory(self, subject:str):
        self.check_subject(subject)
        subject_directory_map = self.get_subject_directory_map()
        titled_subject = self.subject_to_titled_subject(subject)
        text = QFileDialog.getExistingDirectory(
            self.configuration_file_parser.parent_widget,
            f'Select the {titled_subject} Directory', subject_directory_map[subject],
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if text:
            self.on_edit(subject, text)
        
    def get_subject_directory_map(self):
        valid_subjects = [ConfigurationKeys.Paths.IMAGES,
                          ConfigurationKeys.Paths.BOUNDING_BOXES,
                          ConfigurationKeys.Paths.SEMANTIC_SEGMENTS]
        directory_paths = [self.images, self.bounding_boxes, self.semantic_segments]
        return dict(zip(valid_subjects, directory_paths))
    
    @staticmethod
    def subject_to_titled_subject(subject:str):
        separators = re.sub(r'[a-zA-Z0-9]', '', subject)
        if separators:
            patterned_separators = '|'.join(separators)
            subject = re.sub(fr"[{patterned_separators}]+", ' ', subject)
        titled_subject = subject.title()
        return titled_subject
    
    @staticmethod
    def subject_to_hint(subject:str):
        titled_subject = ViewModel.subject_to_titled_subject(subject)
        hint = '[to import from]' if subject == ConfigurationKeys.Paths.IMAGES else '[to export to]'
        hint += f' {titled_subject} Directory Path...'
        return hint
    