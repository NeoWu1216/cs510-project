from os.path import basename
import urllib.request 
import urllib.error
import chardet   #需要导入这个模块，检测编码格式
from tqdm import tqdm
# filepath = '../batch_download/test.txt'
# url = 'https://infobridge.fhwa.dot.gov/Data/BridgeDetail/21006621'
# headers = { #伪装为浏览器抓取
#         'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
#     }
 
# req = urllib.request.Request(url,headers=headers)
# content = urllib.request.urlopen(req).read()

# urllib.request.urlretrieve(url, filepath)

# exit()

import re                                                         
 
def getPDFFromNet(inputURL):
        req = urllib.request.Request(inputURL)
        f = urllib.request.urlopen(req)                           # open web
        localDir = '../test/\\'                             
        urlList = []                                             
        for eachLine in f:                                       
                line = eachLine.strip() ### type = bytes

                print(line)
                if re.match('.*PDF.*', str(line)):                
                        wordList = str(line).split('\"')          
                        for word in wordList:                     
                                if re.match('.*\.pdf$', word):    # get all word including .pdf
                                        urlList.append(word)
        # print(urlList)
        print('Extraction is Done !')                         
        exit()
        for i in tqdm(range(len(urlList))):
            everyURL = urlList[i]
        # for everyURL in urlList:                            
            wordItems = everyURL.split('/')                   
            for item in wordItems:                            
                    if re.match('.*\.pdf$', item):            
                            PDFName = item                    
            localPDF = localDir + PDFName                     
            try:                                             
                    urllib.request.urlretrieve(everyURL, localPDF) # download and save in local machine. 
            except Exception:
                    continue
        print('Download is done!')
websit = 'http://www.cvpapers.com/cvpr2014.html'
getPDFFromNet(websit)
