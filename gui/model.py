#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 12:24:16 2025

@author: mohamed
"""
from pathlib import Path

class Model:
    
    def __init__(self, images, bounding_boxes, 
                 semantic_segments, autosave,
                 void_background, classnames):
        
        self._images = images
        self._bounding_boxes = bounding_boxes
        self._semantic_segments = semantic_segments
        self._autosave = autosave
        self._void_background = void_background
        self._classnames = classnames
        
    @property
    def images(self):
        return self._images
    
    @images.setter
    def images(self, value:str):
        self._images = value
        
    @property
    def bounding_boxes(self):
        return self._bounding_boxes
    
    @bounding_boxes.setter
    def bounding_boxes(self, value:str):
        Path(value).mkdir(parents=True, exist_ok=True)
        self._bounding_boxes = value
        
    @property
    def semantic_segments(self):
        return self._semantic_segments
    
    @semantic_segments.setter
    def semantic_segments(self, value:str):
        Path(value).mkdir(parents=True, exist_ok=True)
        self._semantic_segments = value
        
    @property
    def autosave(self):
        return self._autosave
    
    @autosave.setter
    def autosave(self, value:bool):
        self._autosave = value
        
    @property
    def void_background(self):
        return self._void_background
    
    @void_background.setter
    def void_background(self, value:bool):
        self._void_background = value
        
    @property
    def classnames(self):
        return self._classnames
    
    @classnames.setter
    def classnames(self, value:list[str]):
        self._classnames = value
        
    def __repr__(self):
        quote = lambda value: '"' if type(value) is str else ''
        str_attrs = [f'{name[1:]}={quote(value)}{value}{quote(value)}' for name, value in self.__dict__.items()]
        str_attrs = '\t' + ', \n\t'.join(str_attrs)
        return f"Model(\n{str_attrs}\n)"
