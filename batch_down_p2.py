# -*- coding: utf-8 -*-
import os
import re
import urllib

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
#name pattern: <a href="***_CVPR_2016_paper.html">***</a>
name_list = re.findall(r"(?<=2016_paper.html\">).+(?=</a>)",web_context)

#download
# create local filefolder  
local_dir = '../raw_paper/'
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

cnt = 0
while cnt < len(link_list):
    file_name = name_list[cnt]
    download_url = link_list[cnt]
    #为了可以保存为文件名，将标点符号和空格替换为'_'
    file_name = re.sub('[:\?/]+',"_",file_name).replace(' ','_')
    file_path = local_dir + file_name + '.pdf'
    #download
    print '['+str(cnt)+'/'+str(len(link_list))+'] Downloading' + file_path
    try:
        urllib.urlretrieve("http://openaccess.thecvf.com/" + download_url, file_path)
    except Exception,e:
        print 'download Fail: ' + file_path
    cnt += 1
print 'Finished'
