import numpy as np
import os
import re
import traceback
## root path
path = "./papers_to_index" 
### file name ###
files= os.listdir(path)
# print(files)
s = []
for file in files:
    if not os.path.isdir(file): #if folder or not 
        with open(path+"/"+file, encoding="utf8") as f:
            try:
                text = f.read() # open
            except:
                traceback.print_exc()
                print(f'file: {file}')
            
            res = re.findall('<title>(.*)</title>',text)[0]
            res += " "
            res += re.findall('<abstract>(.*)</abstract>',text)[0]
            if res.strip():
                s.append(res) 
print(len(s))

s = [' '.join(line.split('\n')) for line in s]
s = '\n'.join(s)

with open('parsed_paper/parsed_paper.dat', 'w', encoding="utf8") as f:
    f.write(s)