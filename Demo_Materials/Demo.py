
# coding: utf-8

# In[29]:

import json
import io
from pprint import pprint

#base32Dict Compilation
with io.open('base32SizeDump.json', 'r', encoding='utf-8-sig') as base32Data:    
    base32_data = json.load(base32Data) 
base32Dict = {}

for obj in base32_data:
    base32Dict[obj['Symbol_Name']] = obj['Size']

#base64Dict compilation
with io.open('base64SizeDump.json', 'r', encoding='utf-8-sig') as base64Data:    
    base64_data = json.load(base64Data)
base64Dict = {}

for obj in base64_data:
    base64Dict[obj['Symbol_Name']] = obj['Size']
    
#pwdDict compilation
with io.open('pwdSizeDump.json', 'r', encoding='utf-8-sig') as pwdData:    
    pwdData = json.load(pwdData)
pwdDict = {}

for obj in pwdData:
    pwdDict[obj['Symbol_Name']] = obj['Size']
    


#Compare base32 to base64
keys_base32 = set(base32Dict.keys())
keys_base64 = set(base64Dict.keys())
base32_base64_intersection = keys_base32.intersection(keys_base64)

pprint(base32_base64_intersection)

print("base32 - intersection: ", (keys_base32 - base32_base64_intersection))
print("base64 - intersection: ", (keys_base64 - base32_base64_intersection))

b64exclusive = 0
for keys in (keys_base64 - base32_base64_intersection):
    b64exclusive += int(base64Dict[keys], 16)

print("b64exclusive: ", b64exclusive)

b32exclusive = 0
b32exclusive_keys = set()
for keys in (keys_base32 - base32_base64_intersection):
    b32exclusive += int(base32Dict[keys], 16)

print("b32exclusive: ", b32exclusive)


                   
base32_total = 0
base64_total = 0
base32_base64_overlap_size = 0
for size in base32Dict:
    base32_total += int(base32Dict.get(size), 16 )
    
for size in base64Dict:
    base64_total += int(base64Dict.get(size), 16)

for key in base32_base64_intersection:
    base32_base64_overlap_size += int(base32Dict.get(key), 16)
    
    
base32_base64_result = base32_base64_overlap_size / ( (base32_total + base64_total) - base32_base64_overlap_size ) 

print("new intersection calc", (base32_base64_overlap_size / (b32exclusive + b64exclusive)))
    
#Compare pwd to base64
keys_pwd = set(pwdDict.keys())
keys_base64 = set(base64Dict.keys())
pwd_base64_intersection = keys_pwd & keys_base64
    
pwd_total = 0
pwd_base64_overlap_size = 0

for size in pwdDict:
    pwd_total += int(pwdDict.get(size), 16)
    
for key in pwd_base64_intersection:
    pwd_base64_overlap_size += int(pwdDict.get(key), 16)

pwd_base64_result = pwd_base64_overlap_size / ( (pwd_total + base64_total) - pwd_base64_overlap_size )



#Printing results
print("base32 total symbol size: ", base32_total)
print("base64 total symbol size: ", base64_total)
print("pwd total symbol size: ", pwd_total)
print("base32 and base64 overlap size: ", base32_base64_overlap_size)
print("pwd and base64 overlap size: ", pwd_base64_overlap_size)
print("Percentage overlap between base32 and base64: ", base32_base64_result)
print("Percentage overlap between pwd and base64: ", pwd_base64_result)



# In[ ]:



