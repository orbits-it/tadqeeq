""" 
Tadqeeq - Image Annotator Tool
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-04-27).
Licensed under the MIT License.
"""

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer
import os
from collections import Iterable
from .widgets import ImageAnnotator
from .utils import get_pixmap_compatible_image_filepaths

class MainWindow(QMainWindow):
    
    def __init__(self,
                 images_directory_path,
                 annotations_directory_path,
                 use_bounding_boxes=False,
                 image_navigation_keys=[Qt.Key_A, Qt.Key_D],
                 **image_annotator_kwargs):
        
        def initialize_image_filepaths():
            self.images_directory_path = images_directory_path
            
        def initialize_annotation_filepaths():
            self.__annotations_directory_path = annotations_directory_path
            self.use_bounding_boxes = use_bounding_boxes
            
        def initialize_image_annotator_widget():
            self.__image_annotator_kwargs = image_annotator_kwargs
            self.image_index = 0
            self.__resize_user_interface_update_routine()
        
        def disable_maximize_button():
            self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        def configure_resize_scheduler():
            self.__resize_scheduler = QTimer(self)
            self.__resize_scheduler.setSingleShot(True)
            self.__resize_scheduler.timeout.connect(self.__resize_user_interface_update_routine)
        
        super().__init__()
        
        initialize_image_filepaths()
        initialize_annotation_filepaths()
        initialize_image_annotator_widget()
        
        disable_maximize_button()
        configure_resize_scheduler()
        
        self.image_navigation_keys = image_navigation_keys
        
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowTitle('Tadqeeq - a Minimalist Image Annotator')
        self.setCentralWidget(self.__image_annotator)
        
    @property
    def images_directory_path(self):
        return self.__images_directory_path
    
    @images_directory_path.setter
    def images_directory_path(self, value:str):
        if not os.path.isdir(value):
            raise ValueError('`images_directory_path` should refer to a directory.')
        self.__images_directory_path = value
        self.__image_filepaths = get_pixmap_compatible_image_filepaths(value)
        
    @property
    def annotations_directory_path(self):
        return self.__annotations_directory_path
    
    @property
    def use_bounding_boxes(self):
        return self.__use_bounding_boxes
    
    @use_bounding_boxes.setter
    def use_bounding_boxes(self, value:bool):
        self.__use_bounding_boxes = value
        self.__annotation_filepaths = list(map(self.image_filepath_to_annotation_filepath, self.image_filepaths))
    
    def image_filepath_to_annotation_filepath(self, image_filepath):
        filename = os.path.basename(image_filepath)
        file_extension = '.txt' if self.use_bounding_boxes else '.png'
        annotation_filename = os.path.splitext(filename)[0] + file_extension
        annotation_filepath = os.path.join(self.annotations_directory_path, annotation_filename)
        return annotation_filepath
    
    @property
    def image_filepaths(self):
        return self.__image_filepaths
    
    @property
    def annotation_filepaths(self):
        return self.__annotation_filepaths
    
    @property
    def image_navigation_keys(self):
        return self.__image_navigation_keys
    
    @image_navigation_keys.setter
    def image_navigation_keys(self, value:Iterable):
        if len(value) != 2:
            raise ValueError('`image_navigation_keys` should be an `Iterable` of two items.')
        self.__image_navigation_keys = list(value)
    
    def keyPressEvent(self, event):
        if event.key() == self.image_navigation_keys[0] and self.image_index > 0:
            self.image_index -= 1
        elif event.key() == self.image_navigation_keys[1] and self.image_index < len(self.image_filepaths) - 1:
            self.image_index += 1
    
    @property
    def image_index(self):
        return self.__image_index
    
    @image_index.setter
    def image_index(self, value:int):
        self.__image_index = value
        self.__current_image_filepath = self.image_filepaths[value]
        self.__current_annotation_filepath = self.annotation_filepaths[value]
        self.__update_image_annotator()
            
    def __update_image_annotator(self):
        if hasattr(self, '_MainWindow__image_annotator'):
            self.__image_annotator.image_path = self.current_image_filepath
            self.__image_annotator.annotation_path = self.current_annotation_filepath
        else:
            self.__image_annotator = ImageAnnotator(
                self.current_image_filepath, 
                self.current_annotation_filepath, 
                **self.__image_annotator_kwargs
            )
    
    @property
    def current_image_filepath(self):
        return self.__current_image_filepath
    
    @property
    def current_annotation_filepath(self):
        return self.__current_annotation_filepath
    
    def resizeEvent(self, event):
        self.__resize_scheduler.start(
            self.__image_annotator.RESIZE_DELAY
        )
        
    def __resize_user_interface_update_routine(self):
        self.resize(self.__image_annotator.size())