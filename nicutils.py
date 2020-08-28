import sys
import os
import csv
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore")

class DotDict(dict):
  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
    self.__dict__ = self
  def allowDotting(self, state=True):
    if state:
      self.__dict__ = self
    else:
      self.__dict__ = dict()

def read_by_line(fnm):
    newlines = []
    f = open(fnm,"r")
    lines = f.readlines()#读取全部内容  
    for line in lines: 
        if line is not None and line != "\n":
            line = line.strip()
            newlines.append(line)
    return newlines

def mkdir(path):
    if not os.path.exists(path):
        #print("No Found Folder {}.Creating folder {} for you".format(path,path))
        os.makedirs(path)
    else:
        #pass
        print("Folder {} already exists.".format(path))

def sigmoid(x):
  return 1 / (1 + np.exp(-x))


def list_subdirs(dir):
    "Get a list of immediate subdirectories"
    return next(os.walk(dir))[1]


def list_subfiles(dir):
    # 该函数与list_basefiles有异曲同工之效
    "Get a list of immediate subfiles"
    return next(os.walk(dir))[2]


def list_files(dir):
    "List all files in the current directory"
    fnms = [os.path.join(dir, f).replace("\\","/") for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return fnms


def list_basefiles(dir):
    "List basename of all files in the current directory"
    fnms = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return fnms


def save_as_json(json_dict,json_file_name,mode="w"):
    """在保存中文时，会出现格式错误"""
    # 为indent关键字设置参数，可以保持缩进格式
    json_str = json.dumps(json_dict, indent=4)
    with open(json_file_name,mode) as json_file:
        json_file.write(json_str)
