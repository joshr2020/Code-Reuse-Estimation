
# coding: utf-8

# In[5]:

import json
import io
import sys
import csv
import pandas as pd
import subprocess
from itertools import islice

def gatherNMDump():
    exe = input('Enter the name of the executable: ')
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

    print(df.ix[0])

def main():
    firstFH = gatherNMDump()
    secondFH = gatherNMDump()

    df = textToDataFrame(firstFH)
    df2 = textToDataFrame(secondFH)

if __name__ == "__main__": main()


# In[ ]:




# In[ ]:



