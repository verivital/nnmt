#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 20:24:39 2018

@author: Patrick Musau and Diego Manzanas
"""



from __future__ import print_function
import argparse
import os
import warnings
os.environ['KMP_WARNINGS'] = 'FALSE'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from src.reluPlexPrinter import reluplexPrinter
from src.sherlockPrinter import sherlockPrinter
from src.kerasPrinter import kerasPrinter
from src.TensorflowPrinter import TensorflowPrinter
from src.tf_eran_printer import Tf_eran_printer
#from src.onnxPrinter import onnxPrinter



#function that gets input format from the user
def commandLineInterface():
    #create a commmand line tool for NNMT using argparse 
    ap=argparse.ArgumentParser(description="Neural Network Model Translation Tool")
    
    #add argument for input file path
    ap.add_argument("-i","--inputFile", required=True, help="path to the input file",dest="input")
    #add argument for output path
    ap.add_argument("-o","--outputFile", required=True, help="output file path",dest="output")
    #add argument for the input file type
    ap.add_argument("-t","--tool", required=True, help='input file type i.e (Reluplex,Keras...)',dest="tool")
    #add argument for the format you want the input file to be translated into
    ap.add_argument("-f","--format", help='output format to be translated to default: matfile (.mat)',dest="outputFormat",default="mat")
    #add optional argument for Keras json files
    ap.add_argument("-j","--json", help='optional json model for keras models',dest="json",default=None)
    #parses the arguments and stores them in a dictionary
    args=vars(ap.parse_args())
    return args


#function that decides which tool the model file is 
def decideTool(name,inputPath):
    #get the base name of the path:
    basename=os.path.basename(inputPath)
    if (name=="Reluplex") or (name=="reluplex") or (name=="nnet"):
        #if its from reluplex it will end in .nnet. If not throw an error
        if('.nnet' in basename):
            fileType="Reluplex"
        else:
            print("Error: Unrecognized Reluplex format. Reluplex files end in .nnet")
            fileType=None
    elif name=="Sherlock" or name=="sherlock":
        #check to see if the input file ends in .txt or nothing
        if(".txt" in basename or len(basename.split("."))==1): 
            fileType="Sherlock"
        else:
            print("Error: Unrecognized Sherlock format. Sherlock files end in .txt or nothing")
            fileType=None
    elif name=="Keras" or name=="keras":
        #check to see if the files provided are correct
        if('.h5' in basename):
            fileType="Keras"
        else:
            print("Error: Unrecognized Keras format. Expected filename extension is .h5")
            fileType=None
    elif name =="Tensorflow" or name == "tensorflow":
        #check to see if the files provided are correct
        if('.meta' in basename):
            fileType="Tensorflow"
        else:
            print("Error: Unrecognized Tensorflow format. Expected filename extension is .meta")
            fileType=None
    elif name=="mat" or name=="Matfile":
        if('.mat' in basename):
            fileType="mat"
        else:
            print("Error: Unrecognized Matfile format. Expected filename extension is .mat")
            fileType=None
    else:
        print("Error: Unrecognized input format. Tools currently supported (Reluplex, Sherlock)")
        fileType=None
    return fileType


#function that checks if json file is correct
def checkJson(filepath):
    if filepath:
        basename=os.path.basename(filepath)
        if('.json' in basename):
            return 1
        else:
            return 0
    else:
        return 2
    
#function that decides what the output file should be
def decideOutput(name):
    if name=="mat" or name=="Mat" or name=='Matfile' or name=="matfile":
        outputType="mat"
    elif name=="onnx" or name=="ONNX":
        outputType="onnx"
    elif name=="tf" or name=="ERAN":
        outputType="tf"
    else:
        print("Error: Unrecognized output format. Output formats currently supported (Onnx, Mat)")
        outputType=None
    return outputType

#function that hadles the parsing and printing
def parseHandler(toolName,outputFormat, inputPath, outputpath,jsonFile):
    if(toolName=="Reluplex" and outputFormat=="mat"):
        printer=reluplexPrinter(inputPath,outputpath)
        printer.saveMatfile()
    elif(toolName=="Reluplex" and outputFormat=="onnx"):
        printer=reluplexPrinter(inputPath,outputpath)
        printer.create_onnx_model()
    elif(toolName=="Sherlock" and outputFormat=="mat"):
        printer=sherlockPrinter(inputPath,outputpath)
        printer.saveMatfile()
    elif(toolName=="Sherlock" and outputFormat=="onnx"):
        printer=sherlockPrinter(inputPath,outputpath)
        printer.create_onnx_model()
    elif(toolName=="Tensorflow" and outputFormat=="mat"):
        printer=TensorflowPrinter(inputPath,outputpath,jsonFile)
        #printer.saveMatfile()
    elif(toolName=="Keras" and outputFormat=="mat"):
        #check the json file
        checkNum=checkJson(jsonFile)
        if(checkNum==2):
            printer=kerasPrinter(inputPath,outputpath)
        elif(checkNum==1):
            printer=kerasPrinter(inputPath,outputpath,jsonFile)
        else: 
            print("Error: Unrecognized Keras format. Expected .json file")
    elif(toolName=="Keras" and outputFormat=="onnx"):
        print("Sorry still developping this")
    elif (toolName=="mat" and outputFormat=="tf"):
        Tf_eran_printer(inputPath,outputpath)
    else:
        print(toolName,outputFormat)
        
    

#parse aguments
def parseArguments(arguments):
    inputPath=arguments["input"]
    outputPath=arguments["output"]
    inputFileType=arguments["tool"]
    outputFileType=arguments["outputFormat"]
    jsonFile=arguments["json"]
    
    #decideWhichTool
    toolName=decideTool(inputFileType,inputPath)
    #decide which outputFormat
    if(toolName):
        outputFormat=decideOutput(outputFileType)
    #if both names exist then parse the files using the correct printers
    if(toolName and outputFormat):
        parseHandler(toolName,outputFormat,inputPath,outputPath,jsonFile)
        
    
    
    
    


if __name__=='__main__':
    items=commandLineInterface()
    parseArguments(items)
    

