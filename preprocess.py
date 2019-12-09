import numpy as np
import os
import json
import re
import traceback
import xml.etree.ElementTree as ET
import collections
import PyPDF2
import xmltodict
import pprint
import csv
with open('temp.json', 'r') as json_file:
	temp = json.load(json_file)
with open('paragraph_abstract.json', 'r') as json_file:
	dic = json.load(json_file)
print(len(temp))
print(len(dic))


def reg_remove(inp):
	return inp.replace(" ", "")\
		.replace(":", "").replace("-", "")\
		.replace("'", "").replace("/", "")\
		.replace("?", "").replace(r"\\", "").replace("\"", "").lower()

reverse_temp = {}
for key in temp:
	reverse_temp[reg_remove(key)] = key

data = []
for file_name in dic:
	res = ''
	if reg_remove(file_name) not in reverse_temp: 
		continue
	temp_key = reverse_temp[reg_remove(file_name)]
	author = temp[temp_key][0]
	link = temp[temp_key][1]
	res += file_name + " | "
	res +=  dic[file_name]["abstract"] + " | "
	res += " ".join(dic[file_name]["paragraph"])
	data.append(res)
	dic[file_name]["author"] = author
	dic[file_name]["link"] = link
print(len(data))
data = '\n'.join(data)

with open("test.dat", "w+", encoding="utf8") as file:
    file.write(data)
with open('test.json', 'w+') as json_file:
	json.dump(dic, json_file)


with open('test.json', 'r') as json_file:
	dic = json.load(json_file)
print(len(dic))
temp = list(dic.keys())
for t in temp:
	print(dic[t]["link"])


#==============================================================================================================
data = []
direc = "output/"
empty = 0
for filename in os.listdir(direc):
	res = ''
	with open(direc+filename) as file:
		content = file.read()

		res = filename + " | "
		if len(content.split("abstract"))<3:
			empty += 1
			continue
		else:
			abs_content = content.split("abstract")[1]
			start, end = abs_content.find("<p>") + 3, abs_content.find("</p>")
			abstract = abs_content[start:end]
			res += abstract
			res += " | "

		para = content.split("<p>")[1:]
		paragraph = [section.split("</p>")[0] for section in para]
		res += " ".join(paragraph)
		data.append(res)
	file.close()
print(empty)
data = '\n'.join(data)
with open("test.dat", "w", encoding="utf8") as file:
    file.write(data)


# data = []
# d = {}
# direc = "output1/"
# for filename in os.listdir(direc):
# 	res = ''
# 	with open(direc+filename) as file:
# 		content = file.read()
# 		d[filename] = {}

# 		res = filename + "|\t"
# 		if len(content.split("abstract"))<3:
# 			d[filename]["abstract"] = ""
# 			continue

# 		abs_content = content.split("abstract")[1]
# 		start, end = abs_content.find("<p>")+3, abs_content.find("</p>")
# 		abstract = abs_content[start:end]
# 		d[filename]["abstract"] = abstract
# 		res += abstract

# 		para = content.split("<p>")[1:]
# 		paragraph = [section.split("</p>")[0] for section in para]
# 		d[filename]["paragraph"] = paragraph
# 		res += " ".join(paragraph)
# 		data.append(res)
# 	file.close()

# # with open('content.json', 'w') as json_file:
# #   json.dump(d, json_file)
# data = '\n'.join(data)
# with open("test.dat", "w", encoding="utf8") as file:
#     file.write(data)

# def main():
# 	# tree = ET.parse('test.xml')
# 	# root = tree.getroot()
# 	# print(root.findall('./email'))
# 	with open('content.json', "r") as json_data:
# 		dic = json.loads(json_data)
# 	print(len(dic))

# if __name__== "__main__":
# 	main() 