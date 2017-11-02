
# coding: utf-8

# In[1]:

import json
import io
import sys
import csv
import pandas as pd
import subprocess
from itertools import islice

exe_one = input('Enter the name of the first executable: ')
exe_two = input('Enter the name of the second executable: ')

filepath_one = "../testecutables/" + exe_one
filepath_two = "../testecutables/" + exe_two

file_one_write_out = open("file_one_dump.txt", "w")
file_two_write_out = open ("file_two_dump.txt", "w")


exe_one_dump = subprocess.run(['nm', '-S', filepath_one], stdout=file_one_write_out)
exe_two_dump = subprocess.run(['nm', '-S', filepath_two], stdout=file_two_write_out)
           

# Working code for one
# outfilename  = open("base32SizeDump_test_output.txt",'w')
# sys.stdout = outfilename

# with open("base32SizeDump_test.txt") as file:
#     for line in file:
#         line = line.lstrip()
#         if (line.count(" ") == 3):
#             print (line)



            




# In[6]:

#File handle for first executable
first_outfilename = open('file_one_dump_filtered.txt', 'w')
with open("file_one_dump.txt") as first_file:
    for line in first_file:
        line = line.lstrip()
        if(line.count(" ") == 3):
            first_outfilename.write(line)
            
file_one_write_out.close()
first_outfilename.close()
    
df1 = pd.read_table('file_one_dump_filtered.txt', delimiter = ' ', header = None)
df1.columns = ['Address', 'Size', 'Type', 'Symbol_Name']
df1.reset_index().to_json(orient='records')

df1.ix[0]


# In[4]:

#File handle for second executable    
second_outfilename = open('file_two_dump_filtered.txt', 'w')

with open("file_two_dump.txt") as second_file:
    for line in second_file:
        line = line.lstrip()
        if(line.count(" ") == 3):
            second_outfilename.write(line)
            
file_two_write_out.close()
second_outfilename.close()
df2 = pd.read_table('file_two_dump_filtered.txt', delimiter = ' ', header = None)
df2.columns = ['Address', 'Size', 'Type', 'Symbol_Name']
df2.reset_index().to_json(orient='records')

df2.ix[0]


# In[39]:

# df = pd.read_table('base32SizeDump_test_output.txt', delimiter = ' ', header = None)
# df.columns = ['Address', 'Size', 'Type', 'Symbol_Name']
# df.reset_index().to_json(orient='records')
# df.ix[0]





# exe_one = input('Enter the name of the first executable: ')
# exe_two = input('Enter the name of the second executable: ')

# filepath_one = "../testecutables/" + exe_one
# filepath_two = "../testecutables/" + exe_two

# print(filepath_one)
# print(filepath_two)

# result = subprocess.run(['nm', '-S', filepath_one], stdout=subprocess.PIPE)
# result.stdout

