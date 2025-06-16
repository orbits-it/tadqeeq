#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 13:59:49 2025

@author: mohamed
"""

from os import getcwd
    
class PathKey:
    IMAGES = 'images'
    BOUNDING_BOXES = 'bounding_boxes'
    SEMANTIC_SEGMENTS = 'semantic_segments'
    
class FlagKey:
    VOID_BACKGROUND = 'void_background'
    AUTOSAVE = 'autosave'
    
class ClassKey:
    NAMES = 'names'
    
class BoolKey:
    FALSE = 'false'
    TRUE = 'true'
    
class SectionMeta(type):
    def __new__(cls, name, bases, dct):
        dct['SECTION'] = name
        return super().__new__(cls, name, bases, dct)

class ConfigurationKeys:
    
    class Paths(metaclass=SectionMeta):
        IMAGES = PathKey.IMAGES
        BOUNDING_BOXES = PathKey.BOUNDING_BOXES
        SEMANTIC_SEGMENTS = PathKey.SEMANTIC_SEGMENTS
    
    class Flags(metaclass=SectionMeta):
        VOID_BACKGROUND = FlagKey.VOID_BACKGROUND
        AUTOSAVE = FlagKey.AUTOSAVE
    
    class Classes(metaclass=SectionMeta):
        NAMES = ClassKey.NAMES
        
class DefaultValues:
    IMAGES = getcwd()
    BOUNDING_BOXES = getcwd()
    SEMANTIC_SEGMENTS = getcwd()
    VOID_BACKGROUND = BoolKey.FALSE
    AUTOSAVE = BoolKey.TRUE
    CLASS_NAMES = ''