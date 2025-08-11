#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refined UI with modern layout and styling
Created on Wed Aug  6 14:57:06 2025
@author: mohamed
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QLineEdit,
    QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QDesktopWidget, QMessageBox, 
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from viewmodel import ViewModel
from helper import INIParser
from tadqeeq.implementations import ImageAnnotatorWindow
from tadqeeq.utils import EmptyDatasetError

class PathLayout(QHBoxLayout):
    def __init__(self, hint):
        super().__init__()
        self.hint = hint
        self.path = None
        self.init_ui()
        self.bind_handlers()

    def init_ui(self):
        self.setSpacing(8)
        
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(self.hint)
        self.path_input.setFixedHeight(32)
        self.path_input.setStyleSheet("padding: 4px;")
        
        self.browse_button = QPushButton(QIcon.fromTheme('folder'), '')
        self.browse_button.setFixedSize(32, 32)
        
        self.addWidget(self.path_input)
        self.addWidget(self.browse_button)
        
    def bind_handlers(self):
        self.browse_button.clicked.connect(self.on_button_click)
        
    def on_button_click(self):
        value = QFileDialog.getExistingDirectory(
            parent=None,
            caption='Select Folder',
            directory='',
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if value:
            self.path = value
            self.path_input.setText(value)

class SingleColumnTable(QTableWidget):
    
    def set_contents(self, items:list[str]):
        self.blockSignals(True)
        n = len(items) + 1
        self.setColumnCount(1)
        self.setRowCount(n)
        for idx in range(n):
            item = QTableWidgetItem(items[idx]) if idx < n - 1 else QTableWidgetItem('')
            self.setItem(idx, 0, item)
        self.setVerticalHeaderLabels([str(idx+1) for idx in range(n-1)] + [''])
        self.blockSignals(False)
    
    def get_contents(self):
        n = self.rowCount()
        items = []
        for idx in range(n):
            item = self.item(idx, 0)
            if item is None:
                continue
            item_text = item.text().strip()
            if item_text:
                items.append(item_text)
        return items
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for selection in self.selectedRanges():
                for idx in reversed(range(selection.topRow(), selection.bottomRow() + 1)):
                    self.setItem(idx, 0, None)
            self.set_contents(self.get_contents())
            self.clearSelection()
        else:
            super().keyPressEvent(event)

class View(QWidget):
    def __init__(self, parent, viewmodel:ViewModel):
        super().__init__(parent)
        self.viewmodel = viewmodel
        self.init_ui()
        self.bind_viewmodel()

    def init_ui(self):
        
        self.setWindowTitle("Annotator Configuration")
        self.resize(560, 680)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QCheckBox {
                padding-left: 6px;
            }
        """)

        # ---- PATHS ----
        self.paths_groupbox = QGroupBox('Paths')
        hints = (
            '[import] Images Directory',
            '[export] Bounding Boxes Directory',
            '[export] Semantic Segments Directory',
        )
        self.paths_layout = QVBoxLayout()
        self.paths_layout.setSpacing(10)
        self.paths_layout.setContentsMargins(10, 10, 10, 10)
        
        for hint in hints:
            self.paths_layout.addLayout(PathLayout(hint))

        self.paths_groupbox.setLayout(self.paths_layout)

        # ---- FLAGS ----
        self.flags_groupbox = QGroupBox('Flags')
        self.flags_layout = QVBoxLayout()
        self.flags_layout.setSpacing(6)
        self.flags_layout.setContentsMargins(10, 10, 10, 10)

        self.autosave_checkbox = QCheckBox('Autosave Annotations')
        self.void_background_checkbox = QCheckBox('Ignore Background Segment')

        self.flags_layout.addWidget(self.autosave_checkbox)
        self.flags_layout.addWidget(self.void_background_checkbox)
        self.flags_groupbox.setLayout(self.flags_layout)

        # ---- CLASSES ----
        self.classes_groupbox = QGroupBox('Classes')
        self.classnames_table = SingleColumnTable(0, 1)
        self.classnames_table.setHorizontalHeaderLabels(['Class Names'])
        
        # Visual polish
        self.classnames_table.setAlternatingRowColors(True)
        self.classnames_table.setShowGrid(False)
        self.classnames_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.classnames_table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.classnames_table.setStyleSheet("""
            QTableWidget {
                font-size: 12pt;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 3px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                font-weight: bold;
                padding: 5px;
            }
        """)
        
        # Header formatting
        self.classnames_table.horizontalHeader().setStretchLastSection(True)
        self.classnames_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Minimum row height
        self.classnames_table.verticalHeader().setDefaultSectionSize(28)

        self.table_layout = QVBoxLayout()
        self.table_layout.setContentsMargins(10, 10, 10, 10)
        self.table_layout.addWidget(self.classnames_table)
        self.classes_groupbox.setLayout(self.table_layout)

        # ---- SUBMIT ----
        self.submit_button = QPushButton(
            QIcon.fromTheme('media-playback-start'),
            'Export and Start Annotator'
        )
        self.submit_button.setFixedHeight(36)
        self.submit_button.setStyleSheet("font-weight: bold; padding: 6px;")
        self.submit_button.clicked.connect(self.submit)

        self.submit_layout = QHBoxLayout()
        self.submit_layout.addStretch()
        self.submit_layout.addWidget(self.submit_button)

        # ---- MAIN LAYOUT ----
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(14)
        
        self.main_layout.addWidget(self.paths_groupbox)
        self.main_layout.addWidget(self.flags_groupbox)
        self.main_layout.addWidget(self.classes_groupbox)
        self.main_layout.addLayout(self.submit_layout)
        
        self.setLayout(self.main_layout)
        
        self.move_to_center_of_parent()
        
    def move_to_center_of_parent(self):
        parent = self.parent()
        if parent:
            parent_center = parent.frameGeometry().center()
        else:
            parent_center = QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(parent_center)
        self.move(frame.topLeft())
    
    def bind_viewmodel(self):
        
        def bind_widget_to_setter(widget, setter):
            def wrapper():
                if isinstance(widget, QLineEdit):
                    value = widget.text()
                elif isinstance(widget, SingleColumnTable):
                    value = widget.get_contents()
                else:
                    raise ValueError('A `widget` can either be a `QLineEdit` or a `SingleColumnTable`.')
                return setter(value)
            return wrapper
        
        # ---- PATHS ----
        images_input, bounding_boxes_input, semantic_segments_input = map(
            lambda idx: self.paths_layout.itemAt(idx).path_input,
            range(self.paths_layout.count())
        )
        
        images_input.editingFinished.connect(
            bind_widget_to_setter(images_input, self.viewmodel.set__images)
        )
        self.viewmodel.images__changed.connect(images_input.setText)
        images_input.setText(self.viewmodel.images)
        
        bounding_boxes_input.editingFinished.connect(
            bind_widget_to_setter(bounding_boxes_input, self.viewmodel.set__bounding_boxes)
        )
        self.viewmodel.bounding_boxes__changed.connect(bounding_boxes_input.setText)
        bounding_boxes_input.setText(self.viewmodel.bounding_boxes)

        semantic_segments_input.editingFinished.connect(
            bind_widget_to_setter(semantic_segments_input, self.viewmodel.set__semantic_segments)
        )
        self.viewmodel.semantic_segments__changed.connect(semantic_segments_input.setText)
        semantic_segments_input.setText(self.viewmodel.semantic_segments)
        
        # ---- FLAGS ----
        self.autosave_checkbox.stateChanged.connect(self.viewmodel.set__autosave)
        self.viewmodel.autosave__changed.connect(self.autosave_checkbox.setChecked)
        self.autosave_checkbox.setChecked(self.viewmodel.autosave)
        
        self.void_background_checkbox.stateChanged.connect(self.viewmodel.set__void_background)
        self.viewmodel.void_background__changed.connect(self.void_background_checkbox.setChecked)
        self.void_background_checkbox.setChecked(self.viewmodel.void_background)
        
        # ---- CLASSES ----        
        self.classnames_table.itemChanged.connect(
            bind_widget_to_setter(self.classnames_table, self.viewmodel.set__classnames)
        )
        self.viewmodel.classnames__changed.connect(self.classnames_table.set_contents)
        self.classnames_table.set_contents(self.viewmodel.classnames)
        
    def submit(self):
# =============================================================================
#         try:
# =============================================================================
            self.start_annotator()
            self.write_config()
# =============================================================================
#         except Exception as e:
#             mbox = QMessageBox.critical(self, 'Error', str(e))
#             mbox.exec()
# =============================================================================
        
    def write_config(self):
        parser = INIParser()
        parser.set('Paths', 'images', self.viewmodel.images)
        parser.set('Paths', 'bounding_boxes', self.viewmodel.bounding_boxes)
        parser.set('Paths', 'semantic_segments', self.viewmodel.semantic_segments)
        parser.set('Flags', 'autosave', str(self.viewmodel.autosave).lower())
        parser.set('Flags', 'void_background', str(self.viewmodel.void_background).lower())
        parser.set('Classes', 'names', '\n\t'.join(self.viewmodel.classnames))
        parser.write()
        
    def start_annotator(self):
        self.annotator_window = ImageAnnotatorWindow(
            parent                           = self,
            images_directory_path            = self.viewmodel.images,
            bounding_boxes_directory_path    = self.viewmodel.bounding_boxes,
            semantic_segments_directory_path = self.viewmodel.semantic_segments,
            void_background                  = self.viewmodel.void_background,
            autosave                         = self.viewmodel.autosave,
            label_color_pairs                = self.viewmodel.classnames,
            verbose                          = False,
        )
        self.hide()
        self.annotator_window.show()
        