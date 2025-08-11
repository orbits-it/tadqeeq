#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 12:34:41 2025

@author: mohamed
"""
from helper import INIParser
from model import Model
from viewmodel import ViewModel
from PyQt5.QtWidgets import QApplication
from view import View
import sys

def main():
    app = QApplication(sys.argv)
    
    config = INIParser()
    model = Model(
        images            = config.get('Paths', 'images'),
        bounding_boxes    = config.get('Paths', 'bounding_boxes'),
        semantic_segments = config.get('Paths', 'semantic_segments'),
        autosave          = config.getboolean('Flags', 'autosave'),
        void_background   = config.getboolean('Flags', 'void_background'),
        classnames        = config.getlist('Classes', 'names'),
    )
    viewmodel = ViewModel(model)
    view = View(None, viewmodel)
    
    view.show()
    return app.exec()

if __name__ == '__main__':
    main()