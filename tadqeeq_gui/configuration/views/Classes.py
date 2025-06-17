#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 18:50:41 2025

@author: mohamed
"""

from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from ..misc.widgets import ParametersGroupBox
from ..viewmodels.Classes import ViewModel
from ..misc.parsers import ConfigurationFileParser
from ..misc.constants import ConfigurationKeys

class View(ParametersGroupBox):
    
    def __init__(self, configuration_file_parser:ConfigurationFileParser):
        view_model = ViewModel(configuration_file_parser)
        table = Table(TableModel(view_model))
        super().__init__(ConfigurationKeys.Classes.SECTION, 10, 0, classnames_table=table)
        
class TableModel(QAbstractTableModel):
    
    def __init__(self, view_model:ViewModel):
        super().__init__()        
        self.view_model = view_model
    
    @property
    def names(self):
        return self.view_model.model.names
    
    def rowCount(self, parent=None):
        return len(self.names) + 1
    
    def columnCount(self, parent=None):
        return 1
    
    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            row_index = index.row()
            if row_index < len(self.names):
                return self.names[row_index]
            return ''
        
    def setData(self, index, value, role):#???
        if role == Qt.EditRole:
            row_index = index.row()
            result = self.view_model.on_edit(row_index, value)
            is_appended = result and row_index == len(self.names) - 1
            if is_appended:
                self.insertRow(row_index + 1, QModelIndex())
            self.dataChanged.emit(index, index)
        return result
    
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return "Label Name"
            if orientation == Qt.Vertical:
                return str(section + 1)
        
class Table(QTableView):
    
    def __init__(self, table_model:TableModel):
        super().__init__()
        
        self.setModel(table_model)
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setVisible(False)
        
        self.verticalHeader().setVisible(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        
        self.set_uniform_row_heights()
        table_model.modelReset.connect(self.set_uniform_row_heights)
        table_model.rowsInserted.connect(self.set_uniform_row_heights)
        
    def set_uniform_row_heights(self):
        header_height = self.horizontalHeader().height()
        for row in range(self.model().rowCount()):
            self.setRowHeight(row, header_height)


# =============================================================================
#     @property
#     def view_model(self):
#         return self.__view_model
#     
#     @view_model.setter
#     def view_model(self, value:ViewModel):
#         self.__view_model = value
#         value.names_changed.connect(self.update)
#         self.itemChanged.connect(value.on_edit)
#         self.update(value.names)
#         
#     def update(self, classnames:list[str]):
#         self.blockSignals(True)
#         header_height = self.horizontalHeader().height()
#         self.setRowCount(0)
#         for name in classnames:
#             row_index = self.rowCount()
#             self.insertRow(row_index)
#             self.setRowHeight(row_index, header_height)
#             self.setItem(row_index, 0, QTableWidgetItem(name.strip()))
#         self.blockSignals(False)
# =============================================================================
        