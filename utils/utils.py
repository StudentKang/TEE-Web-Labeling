# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :   utils.py
@Time    :   2022/11/01 21:15:02
@Author  :   KangQing
@Version :   1.0
@Contact :   auqkang@163.com
@License :   (C)Copyright 2022-2023
@Desc    :   General functions
"""

import numpy as np
import torch
from numpy import random
import os
import json

def set_seed(seed:int):
    """Set random seed

    Args:
        seed (int): random seed number
    """
    random.seed(seed) 
    os.environ["PYTHONSEED"] = str(seed)
    np.random.seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed) 
    torch.backends.cudnn.deterministic = True 
    torch.backends.cudnn.benchmark = True 
    torch.backends.cudnn.enabled = True  
    torch.manual_seed(seed)



def createDirs(dirPath:str):
    """Create not existed dir

    Args:
        dirPath (str): dirPath
    """
    if(not os.path.exists(dirPath)):
        os.makedirs(dirPath)
        

def is_number(s:str):
    """
    Description of is_number: judge the string is a number or not

    Args:
        s (str):string for judge

    Returns:
        bool: true or false

    """
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def is_contains_chinese(strs:str):
    """is contain chainese or not

    Args:
        strs (str): string for judge
    
    Returns:
        bool: true or false

    """
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def getJsonInfo(gtJsonPath:str):
    """Get GT box class

    Args:
        gtJsonPath (str):  the path for json of GT

    Returns:
        List[int]: x1,y1,x2,y2 for the box (x1>x2,y1>y2)
    """
    with open(gtJsonPath,encoding='utf-8') as a:
        results = json.load(a)
        shapes = results.get('shapes')
        boxes = shapes[0].get('points')
        [x1,y1] = boxes[0]
        [x2,y2] = boxes[1]
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        return [x1,y1,x2,y2]
