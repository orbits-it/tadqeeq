#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 18:50:41 2025

@author: mohamed
"""

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from ..misc.widgets import ParametersGroupBox
from ..viewmodels.Classes import ViewModel
from ..misc.parsers import ConfigurationFileParser
from ..misc.constants import ConfigurationKeys
from functools import partial

class View(ParametersGroupBox):
    
    def __init__(self, configuration_file_parser:ConfigurationFileParser):
        
        def link_and_apply_update():
            update_classnames_table = partial(self.components['classnames_table'].update, self.view_model)
            self.view_model.names_changed.connect(update_classnames_table)
            update_classnames_table()
        
        def link_edit_entry_event():
            self.components['classnames_table'].itemChanged.connect(self.view_model.on_edit)
        
        super().__init__(ConfigurationKeys.Classes.SECTION, 10, 0, classnames_table=ClassnamesTable())
        self.view_model = ViewModel(configuration_file_parser)
        
        link_and_apply_update()
        link_edit_entry_event()
        

class ClassnamesTable(QTableWidget):
    
    def __init__(self):
        super().__init__(0, 1)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setVisible(False)
        self.setShowGrid(True)
        
    def update(self, view_model:ViewModel):
        self.blockSignals(True)
        header_height = self.horizontalHeader().height()
        self.setRowCount(0)
        for name in view_model.names:
            row_index = self.rowCount()
            self.insertRow(row_index)
            self.setRowHeight(row_index, header_height)
            self.setItem(row_index, 0, QTableWidgetItem(name.strip()))
        self.blockSignals(False)
        