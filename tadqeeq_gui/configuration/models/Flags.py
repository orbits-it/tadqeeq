#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 16:30:46 2025

@author: mohamed
"""

class Model:
    
    def __init__(self, autosave, void_background):
        self.autosave = autosave
        self.void_background = void_background
    
    @property
    def autosave(self):
        return self.__autosave
    
    @autosave.setter
    def autosave(self, value:bool):
        self.__autosave = value
    
    @property
    def void_background(self):
        return self.__void_background
    
    @void_background.setter
    def void_background(self, value:bool):
        self.__void_background = value
