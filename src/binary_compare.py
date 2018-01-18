'''
Copyright (C) 2017 Aurin Chakravarty & Joshua Russo.
'''
import os
import argparse
import sys
import pandas as pd
import subprocess

def getTotalSize(x):
    '''
    Sums up all string values in base 16 and converts to base 10.

    x is a dictionary with keys as symbols and values as sizes in base 16.
    '''
    x_total = 0
    for size in x:
        x_total += int(x.get(size), 16)
    return x_total

def jaccard(x, y):
    '''
    Compares two dictionaries using the jaccard index.
    '''
    keysx = set(x.keys())
    keysy = set(y.keys())
    intersection = keysx.intersection(keysy)
    x_total = getTotalSize(x)
    y_total = getTotalSize(y)

    overlap_size = 0
    for key in intersection:
        if int(x.get(key), 16) == int(y.get(key), 16):
            overlap_size += int(x.get(key), 16)

    result = float(overlap_size) / float(x_total + y_total - overlap_size)
    return result


def gatherNMDump(exe, rootdir):
    '''
    Populates dataframe with nm output of exe file.
    '''
    index = exe.rfind("/")
    justExeName = exe[index + 1:]
    with open(rootdir + "/.bin/" + justExeName + "_dump.txt", "w") as write_out:
        subprocess.run(['nm', '-S', exe], stdout=write_out)
        fileName = write_out.name

    tempFileName = fileName.rsplit(".", 1)[0]
    # filter out symbols without associated sizes
    with open(tempFileName + "_filtered.txt", 'w+') as outfile:
        with open(fileName) as file2:
            for line in file2:
                line = line.lstrip()
                if(line.count(' ') == 3):
                    outfile.write(line)
    df = pd.read_table(outfile.name, header = None, delim_whitespace=True)
    df.columns = ['Address', 'Size', 'Type', 'Symbol_Name']
    df.reset_index().to_json(orient='records')
    return df

def compare(input, rootdir):
    '''
    Two file compare from filenames to result.
    '''
    df = gatherNMDump(input[0], rootdir)
    df2 = gatherNMDump(input[1], rootdir)

    dict1 = df.set_index('Symbol_Name')['Size'].to_dict()
    dict2 = df2.set_index('Symbol_Name')['Size'].to_dict()

    result = jaccard(dict1, dict2)

    print('%s, %s, %f' % (os.path.abspath(input[0]), os.path.abspath(input[1])
    , result))

def multiCompare(input, rootdir):
    '''
    Multiple file compare with input as a directory.
    '''
    filenames = os.listdir(input[0])
    filepaths = []
    for name in filenames:
        filepaths.append(input[0] + "/" + name)

    for x in range(0, int(input[1])):
        for y in range(x, int(input[1])):
            if x == y:
                continue
            else:
                compare([filepaths[x], filepaths[y]], rootdir)

def main(argv):
    rootdir = os.getcwd()
    rootdir = os.path.dirname(rootdir)
    if not os.path.exists(rootdir + "/.bin/"):
        os.makedirs(rootdir + "/.bin/")

    parser = argparse.ArgumentParser(description='Compare binaries.')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_many = subparsers.add_parser('many', help='recurse help')
    parser_many.add_argument('dir', help='dir to compare pairs')
    parser_many.add_argument('number_of_comparisons',
        help='number of comparisons', type=int)
    parser_two = subparsers.add_parser('two', help='two file help')
    parser_two.add_argument('file1', help='file to compare')
    parser_two.add_argument('file2', help='file to compare')

    args = parser.parse_args()
    args_dict = vars(args)
    if 'dir' in args_dict.keys():
        multiCompare([args_dict['dir'],
            args_dict['number_of_comparisons']], rootdir)
    else:
        compare([args_dict['file1'], args_dict['file2']], rootdir)

if __name__ == "__main__":
    main(sys.argv[0:])
