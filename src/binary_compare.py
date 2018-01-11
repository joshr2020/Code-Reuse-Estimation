'''
Copyright (C) 2017 Aurin Chakravarty & Joshua Russo
'''
import os
import io
import sys
import pandas as pd
import subprocess

#x is a dictionary
def getTotalSize(x):
    x_total = 0
    for size in x:
        x_total += int(x.get(size), 16)
    return x_total

#x and y are both dictionaries holding data of executables to compare
def compareDicts(x, y):
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
    write_out = open(rootdir + "/bin/" + justExeName + "_dump.txt", "w")
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

def handleInput(input):
    if len(input) == 4:
        if input[1] == "-r":
            if os.path.isdir(input[2]):
                return 0
            else:
                badInput()
        else:
            badInput()
    elif len(input) == 3:
        if os.path.exists(input[1]):
            if os.path.exists(input[2]):
                return 1
            else:
                badInput()
        else:
            badInput()
    else:
        badInput()

def badInput():
    print("invalid input. format to run: \"binary_compare.py <fullfilepath1> <fullfilepath2>\" or \"binary_compare.py -r <directory> <number_of_comparisons>\"")
    sys.exit(0)

def compare(input):
    rootdir = os.getcwd()
    rootdir = os.path.dirname(rootdir)

    if not os.path.exists(rootdir + "/bin/"):
        os.makedirs(rootdir + "/bin/")

    firstFH = gatherNMDump(input[0], rootdir)
    secondFH = gatherNMDump(input[1], rootdir)

    df = textToDataFrame(firstFH, rootdir)
    df2 = textToDataFrame(secondFH, rootdir)

    dict1 = df.set_index('Symbol_Name')['Size'].to_dict()
    dict2 = df2.set_index('Symbol_Name')['Size'].to_dict()

    result = compareDicts(dict1, dict2)

    print('%s, %s, %f' % (input[0], input[1], result))

def main(argv):
    if handleInput(argv) == 1:
        compare(argv[1:])

    if handleInput(argv) == 0:
        filenames = os.listdir(sys.argv[2])
        filepaths = []
        for name in filenames:
            filepaths.append((os.path.normpath(sys.argv[2]) + "/" + name))

        for x in range(0, int(sys.argv[3])):
            for y in range(x, int(sys.argv[3])):
                if x == y:
                    continue
                else:
                    compare([filepaths[x], filepaths[y]])

if __name__ == "__main__":
    main(sys.argv[0:])
