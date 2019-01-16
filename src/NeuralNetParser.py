#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 19:44:37 2018

@author: Musau
"""


from abc import ABC, abstractmethod
class NeuralNetParser(ABC):
    
    @abstractmethod
    def __init__(self,pathToOriginalFile, OutputFilePath,*vals):
        pass
    @abstractmethod
    def create_matfile(self):
        pass
    def create_onnx_model(self):
        pass
    

