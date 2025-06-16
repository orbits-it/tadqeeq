#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 16:31:04 2025

@author: mohamed
"""

from configuration.window import Configuration as ConfigurationWindow
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QPoint
import sys
import os
from tadqeeq.utils import EmptyDatasetError
from tadqeeq.implementations import ImageAnnotatorWindow

class Application(QApplication):
    
    def __init__(self, argv):
        super().__init__(sys.argv)
        
        script_filepath = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_filepath)
        configuration_filepath = os.path.join(script_directory, 'config.ini')
        self.configuration_window = ConfigurationWindow(configuration_filepath)
        self.configuration_window.submit_button.clicked.connect(self.close_configuration_window_and_start_annotator)
        
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        configuration_window_center = QPoint(screen_center.x(), screen_center.y() - 50)
        
        configuration_window_geometry = self.configuration_window.frameGeometry()
        configuration_window_geometry.moveCenter(configuration_window_center)
        
        self.configuration_window.move(configuration_window_geometry.topLeft())
        
        self.configuration_window.show()
        
    @property
    def configuration_file_parser(self):
        return self.configuration_window.configuration_file_parser
        
    def close_configuration_window_and_start_annotator(self):
        try:
            kwargs = self.get_annotator_kwargs()
            self.annotator_window = ImageAnnotatorWindow(**kwargs)
            self.annotator_window.move(0, 0)
            self.annotator_window.show()
            self.configuration_window.close()
        except EmptyDatasetError:
            QMessageBox.critical(
                self.configuration_window,
                'Empty Dataset',
                'No compatible image files found at the given directory'
            )
            
    def get_annotator_kwargs(self):
        return {
            'images_directory_path'            : self.configuration_window.paths_groupbox.view_model.model.images,
            'bounding_boxes_directory_path'    : self.configuration_window.paths_groupbox.view_model.model.bounding_boxes,
            'semantic_segments_directory_path' : self.configuration_window.paths_groupbox.view_model.model.semantic_segments,
            'void_background'                  : self.configuration_window.flags_groupbox.view_model.model.void_background,
            'autosave'                         : self.configuration_window.flags_groupbox.view_model.model.autosave,
            'label_color_pairs'                : self.configuration_window.classes_groupbox.view_model.model.names,
        }

if __name__ == '__main__':
    app = Application(sys.argv)
    sys.exit(app.exec_())
    
    