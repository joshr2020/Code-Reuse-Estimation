import json
import io
from pprint import pprint
import sys

#x is a json filename
def compileDict(x):
    with io.open(x, 'r', encoding='utf-8-sig') as filex:
        datax = json.load(filex)
    dictx = {}
    for obj in datax:
        dictx[obj['Symbol_Name']] = obj['Size']
    return dictx

#x is a dictionary
def getTotalSize(x):
    x_total = 0
    for size in x:
        x_total += int(x.get(size), 16)
    return x_total

#x and y are both dictionaries holding data of executables to compare
def compare(x, y):
    keysx = set(x.keys())
    keysy = set(y.keys())
    intersection = keysx.intersection(keysy)
    assert intersection == keysy.intersection(keysx)
    x_total = getTotalSize(x)
    y_total = getTotalSize(y)

    overlap_size = 0
    for key in intersection:
        overlap_size += int(x.get(key), 16)

    result = float(overlap_size) / float(x_total + y_total - overlap_size)
    return result

#x and y are both json filenames
def calculateOverlap(x, y):
    dictx = compileDict(x)
    dicty = compileDict(y)
    print("Overlap: ", compare(dictx, dicty))

calculateOverlap()
