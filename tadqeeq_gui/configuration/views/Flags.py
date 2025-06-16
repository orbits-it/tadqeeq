#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 08:02:36 2025

@author: mohamed
"""

from PyQt5.QtWidgets import QCheckBox
from ..misc.widgets import ParametersGroupBox
from ..misc.parsers import ConfigurationFileParser
from ..misc.constants import ConfigurationKeys
from ..viewmodels.Flags import ViewModel

class View(ParametersGroupBox):
    
    def __init__(self, configuration_file_parser:ConfigurationFileParser):
        
        def link_and_apply_updates():
            self.view_model.autosave_changed.connect(self.update_autosave_checkbox)
            self.view_model.void_background_changed.connect(self.update_void_background_checkbox)
            
            self.update_autosave_checkbox()
            self.update_void_background_checkbox()
        
        def link_on_checked_state_changes():
            self.components['autosave_checkbox'].stateChanged.connect(self.view_model.on_autosave_state_change)
            self.components['void_background_checkbox'].stateChanged.connect(self.view_model.on_void_background_state_change)
        
        super().__init__(
            ConfigurationKeys.Flags.SECTION, 5, 0,
            autosave_checkbox=QCheckBox('Enable Autosave'), 
            void_background_checkbox=QCheckBox('Ignore Background Segment')
        )
        self.view_model = ViewModel(configuration_file_parser)

        link_and_apply_updates()
        link_on_checked_state_changes()
        
    def update_autosave_checkbox(self):
        self.components['autosave_checkbox'].setChecked(self.view_model.autosave)
        
    def update_void_background_checkbox(self):
        self.components['void_background_checkbox'].setChecked(self.view_model.void_background)
            
        