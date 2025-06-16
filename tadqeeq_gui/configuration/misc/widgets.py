#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 18:48:44 2025

@author: mohamed
"""

from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QSizePolicy

class ParametersGroupBox(QGroupBox):
    
    def __init__(self, title, interior_boundary_margin, inter_component_spacing, **components):
        super().__init__(title)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(*[interior_boundary_margin]*4)
        self.layout.setSpacing(inter_component_spacing)
        self.setLayout(self.layout)
        self.components = components
        
    @property
    def components(self):
        return self.__components
    
    @components.setter
    def components(self, value:dict):
        self.__components = value
        for item in value.values():
            if isinstance(item, QWidget):
                self.layout.addWidget(item)
            else:
                self.layout.addLayout(item)
        
        