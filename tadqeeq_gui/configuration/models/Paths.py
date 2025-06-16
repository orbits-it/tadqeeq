#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 16:30:26 2025

@author: mohamed
"""

import os

class Model:
    
    def __init__(self, images:str, bounding_boxes:str, semantic_segments:str):
        self.images = images
        self.bounding_boxes = bounding_boxes
        self.semantic_segments = semantic_segments
        
    def _ensure_directory(self, value:str):
        if not value.strip():
            raise ValueError(f'Invalid directory path: "{value}"')
        os.makedirs(value, exist_ok=True)
        return value
    
    @property
    def images(self):
        return self.__images
    
    @images.setter
    def images(self, value:str):
        self.__images = self._ensure_directory(value)
    
    @property
    def bounding_boxes(self):
        return self.__bounding_boxes
    
    @bounding_boxes.setter
    def bounding_boxes(self, value:str):
        self.__bounding_boxes = self._ensure_directory(value)
    
    @property
    def semantic_segments(self):
        return self.__semantic_segments
    
    @semantic_segments.setter
    def semantic_segments(self, value:str):
        self.__semantic_segments = self._ensure_directory(value)
