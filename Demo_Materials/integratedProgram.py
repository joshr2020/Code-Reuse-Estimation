import json
import io
import sys
import csv
import pandas as pd
import subprocess
from itertools import islice
from pprint import pprint

#x is a json filename
# def compileDict(x):
#     with io.open(x, 'r', encoding='utf-8-sig') as filex:
#         datax = json.load(filex)
#     dictx = {}
#     for obj in datax:
#         dictx[obj['Symbol_Name']] = obj['Size']
#     return dictx

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

def gatherNMDump(exe):
    filepath = "../testecutables/" + exe
    write_out = open(exe + "_dump.txt", "w")
    subprocess.run(['nm', '-S', filepath], stdout=write_out)
    fileName = write_out.name
    write_out.close()
    return fileName

def textToDataFrame(fileName):
    #File handle for first executable
    tempFileName = fileName.rsplit(".", 1)[0]
    outfilename = open(tempFileName + "_filtered.txt", 'w+')

    with open(fileName) as file:
        for line in file:
            line = line.lstrip()
            if(line.count(' ') == 3):
                outfilename.write(line)

    outfilename.close()


    df = pd.read_table(outfilename.name, header = None, delim_whitespace=True)
    df.columns = ['Address', 'Size', 'Type', 'Symbol_Name']
    df.reset_index().to_json(orient='records')
    return df

def main():
    exe1 = input('Enter the name of the executable: ')
    exe2 = input('Enter the name of the executable: ')

    firstFH = gatherNMDump(exe1)
    secondFH = gatherNMDump(exe2)

    df = textToDataFrame(firstFH)
    df2 = textToDataFrame(secondFH)
    
    dict1 = df.set_index('Symbol_Name')['Size'].to_dict()
    dict2 = df2.set_index('Symbol_Name')['Size'].to_dict()

    result = compare(dict1, dict2)

    print('Overlap of %s and %s is: %f' % (exe1, exe2, result))

if __name__ == "__main__": main()
