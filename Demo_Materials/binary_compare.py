'''
Copyright (C) 2017 Aurin Chakravarty & Joshua Russo
'''
import json
import os
import io
import sys
import csv
import pandas as pd
import subprocess
from itertools import islice
from pprint import pprint

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


def gatherNMDump(exe, rootdir):
    index = exe.rfind("/")
    justExeName = exe[index + 1:]
    write_out = open(rootdir + "bin/" + justExeName + "_dump.txt", "w")
    subprocess.run(['nm', '-S', exe], stdout=write_out)
    fileName = write_out.name
    write_out.close()
    return fileName

def textToDataFrame(fileName, rootdir):
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

def main(argv):
    if len(sys.argv) != 3:
        print("invalid arguments")
        sys.exit(0)

    rootdir = os.getcwd()
    index = rootdir.rfind("/")
    rootdir = rootdir[:index+1]

    if not os.path.exists(rootdir + "bin/"):
        os.makedirs(rootdir + "bin/")

    firstFH = gatherNMDump(sys.argv[1], rootdir)
    secondFH = gatherNMDump(sys.argv[2], rootdir)

    df = textToDataFrame(firstFH, rootdir)
    df2 = textToDataFrame(secondFH, rootdir)

    dict1 = df.set_index('Symbol_Name')['Size'].to_dict()
    dict2 = df2.set_index('Symbol_Name')['Size'].to_dict()

    result = compare(dict1, dict2)

    print('%s, %s, %f' % (sys.argv[1], sys.argv[2], result))

if __name__ == "__main__":
    main(sys.argv[0:])
