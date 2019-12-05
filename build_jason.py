# -*- coding: utf-8 -*-
import os
import re
import urllib
import json
import requests


#get web context
def get_context(url):
    """
    params: 
        url: link
    return:
        web_context
    """
    web_context = requests.get(url)
    return web_context.text

url = 'http://openaccess.thecvf.com//CVPR2016.py'
web_context = get_context(url)

#find paper files

#link pattern: href="***_CVPR_2016_paper.pdf">pdf
link_list = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)",web_context)
# print web_context
# exit()
author_list = re.findall(r"(?<=author = ).+(?=<br>)",web_context)
# print 'link:',link_list[0]
# print 'title:',title[0]
# exit()
#name pattern: <a href="***_CVPR_2016_paper.html">***</a>
title = re.findall(r"(?<=2016_paper.html\">).+(?=</a>)",web_context)

#download
# create local filefolder  
local_dir = '../data_base/'
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

cnt = 0
data = dict()
while cnt < len(link_list):
    value = []
    author = re.sub('[:\?/]+',"_",author_list[cnt]).replace('{','').replace('}','').strip(',')

    value.append(author)
    link = "http://openaccess.thecvf.com/" + link_list[cnt]
    value.append(link)
    data[title[cnt]] = value


    

    cnt += 1
file_name = local_dir + 'data.json'
with open(file_name, 'w') as f:
    json.dump(data, f)
    f.close()
print 'Finished'
