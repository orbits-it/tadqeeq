# -*- coding: utf-8 -*-

""" 
GUI for `Tadqeeq - Image Annotator Tool`
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-05-27).
"""

from PyQt5.QtWidgets import QHBoxLayout, QFileIconProvider, QPushButton, QLineEdit
from ..viewmodels.Paths import ViewModel
from ..misc.widgets import ParametersGroupBox
from ..misc.parsers import ConfigurationFileParser
from ..misc.constants import ConfigurationKeys
from functools import partial
        
class View(ParametersGroupBox):
    
    def __init__(self, configuration_file_parser:ConfigurationFileParser):
        
        def link_and_apply_updates():
            update_images_selector = partial(self.components['images_selector'].update, self.view_model)
            update_bounding_boxes_selector = partial(self.components['bounding_boxes_selector'].update, self.view_model)
            update_semantic_segments_selector = partial(self.components['semantic_segments_selector'].update, self.view_model)
            
            self.view_model.images_changed.connect(update_images_selector)
            self.view_model.bounding_boxes_changed.connect(update_bounding_boxes_selector)
            self.view_model.semantic_segments_changed.connect(update_semantic_segments_selector)
            
            update_images_selector()
            update_bounding_boxes_selector()
            update_semantic_segments_selector()
            
        def link_edit_text_events():
            images_text_input = self.components['images_selector'].text_input
            bounding_boxes_text_input = self.components['bounding_boxes_selector'].text_input
            semantic_segments_text_input = self.components['semantic_segments_selector'].text_input
            
            on_edit_images = partial(self.view_model.on_edit, ConfigurationKeys.Paths.IMAGES, images_text_input.text())
            on_edit_bounding_boxes = partial(self.view_model.on_edit, ConfigurationKeys.Paths.BOUNDING_BOXES, bounding_boxes_text_input.text())
            on_edit_semantic_segments = partial(self.view_model.on_edit, ConfigurationKeys.Paths.SEMANTIC_SEGMENTS, semantic_segments_text_input.text())
            
            images_text_input.editingFinished.connect(on_edit_images)
            bounding_boxes_text_input.editingFinished.connect(on_edit_bounding_boxes)
            semantic_segments_text_input.editingFinished.connect(on_edit_semantic_segments)
            
        def link_button_click_events():        
            on_click_images = partial(self.view_model.browse_for_directory, ConfigurationKeys.Paths.IMAGES)
            on_click_bounding_boxes = partial(self.view_model.browse_for_directory, ConfigurationKeys.Paths.BOUNDING_BOXES)
            on_click_semantic_segments = partial(self.view_model.browse_for_directory, ConfigurationKeys.Paths.SEMANTIC_SEGMENTS)
            
            self.components['images_selector'].browse_button.clicked.connect(on_click_images)
            self.components['bounding_boxes_selector'].browse_button.clicked.connect(on_click_bounding_boxes)
            self.components['semantic_segments_selector'].browse_button.clicked.connect(on_click_semantic_segments)
            
        super().__init__(
            'Paths', 6, 8, 
            images_selector=DirectorySelectorLayout(ConfigurationKeys.Paths.IMAGES),
            bounding_boxes_selector=DirectorySelectorLayout(ConfigurationKeys.Paths.BOUNDING_BOXES),
            semantic_segments_selector=DirectorySelectorLayout(ConfigurationKeys.Paths.SEMANTIC_SEGMENTS),
        )
        self.view_model = ViewModel(configuration_file_parser)
        link_and_apply_updates()
        link_edit_text_events()
        link_button_click_events()


class DirectorySelectorLayout(QHBoxLayout):
    
    def __init__(self, subject:str):
        super().__init__()
        ViewModel.check_subject(subject)
        
        self.__subject = subject
        
        self.text_input = QLineEdit()
        hint = ViewModel.subject_to_hint(subject)
        self.text_input.setPlaceholderText(hint)
        self.addWidget(self.text_input)
        
        self.browse_button = BrowseButton()
        self.addWidget(self.browse_button)
        
        
    def update(self, view_model:ViewModel):
        match self.subject:
            case ConfigurationKeys.Paths.IMAGES:
                text = view_model.images
            case ConfigurationKeys.Paths.BOUNDING_BOXES:
                text = view_model.bounding_boxes
            case ConfigurationKeys.Paths.SEMANTIC_SEGMENTS:
                text = view_model.semantic_segments
        self.text_input.setText(text)
    
    @property
    def subject(self):
        return self.__subject

class BrowseButton(QPushButton):
    
    def __init__(self):
        super().__init__()
        folder_icon = QFileIconProvider().icon(QFileIconProvider.Folder)
        self.setText('')
        self.setIcon(folder_icon)