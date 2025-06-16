#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 16:30:47 2025

@author: mohamed
"""

class Model:
    
    def __init__(self, names=None):
        self.names = [] if names is None else names
    
    @property
    def names(self):
        return self.__names
    
    @names.setter
    def names(self, value:list):
        self.__names = value
