#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 14:01:29 2025

@author: mohamed
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty
from model import Model
import numpy as np

class ViewModel(QObject):
    
    images__changed            = pyqtSignal(str)
    bounding_boxes__changed    = pyqtSignal(str)
    semantic_segments__changed = pyqtSignal(str)
    autosave__changed          = pyqtSignal(bool)
    void_background__changed   = pyqtSignal(bool)
    classnames__changed        = pyqtSignal(list)
    
    def __init__(self, model:Model):
        super().__init__()
        self._model = model
        
    def get__images(self):
        return self._model.images
    
    def set__images(self, value:str):
        if self._model.images != value:
            self._model.images = value
            self.images__changed.emit(value)
            
    images = pyqtProperty(str, fget=get__images,
                          fset=set__images,
                          notify=images__changed)
            
    def get__bounding_boxes(self):
        return self._model.bounding_boxes
    
    def set__bounding_boxes(self, value:str):
        if self._model.bounding_boxes != value:
            self._model.bounding_boxes = value
            self.bounding_boxes__changed.emit(value)
            
    bounding_boxes = pyqtProperty(str, fget=get__bounding_boxes,
                                  fset=set__bounding_boxes,
                                  notify=bounding_boxes__changed)
    
    def get__semantic_segments(self):
        return self._model.semantic_segments
    
    def set__semantic_segments(self, value:str):
        if self._model.semantic_segments != value:
            self._model.semantic_segments = value
            self.semantic_segments__changed.emit(value)
            
    semantic_segments = pyqtProperty(str, fget=get__semantic_segments,
                                     fset=set__semantic_segments,
                                     notify=semantic_segments__changed)
    
    def get__autosave(self):
        return self._model.autosave
    
    def set__autosave(self, value:bool):
        value = bool(value)
        if self._model.autosave != value:
            self._model.autosave = value
            self.autosave__changed.emit(value)
    
    autosave = pyqtProperty(bool, fget=get__autosave,
                            fset=set__autosave,
                            notify=autosave__changed)
    
    def get__void_background(self):
        return self._model.void_background
    
    def set__void_background(self, value:bool):
        value = bool(value)
        if self._model.void_background != value:
            self._model.void_background = value
            self.void_background__changed.emit(value)
    
    void_background = pyqtProperty(bool, fget=get__void_background,
                                   fset=set__void_background,
                                   notify=void_background__changed)
    
    def get__classnames(self):
        return self._model.classnames
    
    def set__classnames(self, value:list[str]):
        if not np.array_equal(self._model.classnames, value):
            self._model.classnames = value
            self.classnames__changed.emit(value)
    
    classnames = pyqtProperty(list, fget=get__classnames,
                              fset=set__classnames,
                              notify=classnames__changed)
    