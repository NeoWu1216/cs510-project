import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics.pairwise import linear_kernel
import sys
import search_title

# Path of parsed papers
path_parsed = "./test/"
# path_parsed = ""

def most_related_paragraph(title,paragraph_list):
    tfidf = TfidfVectorizer().fit_transform([title]+paragraph_list)
    cosine_similarities = linear_kernel(tfidf[0], tfidf[1:]).flatten()
    most_similar, similarity = paragraph_list[0], -1
    for i in range(len(paragraph_list)):
        if cosine_similarities[i] > similarity:
            similarity = cosine_similarities[i]
            most_similar = paragraph_list[i]

    return most_similar

def paragraph_rank(string,top_num):
    #feature 2, return most related paragraph
    f = open(path_parsed + "test.json", 'r')
    data = json.load(f)
    title_list = search_title.query(string,top_num)
    ret_val = [] # list of dictionary of title and info
    for idx,title in enumerate(title_list,1):
        title = title.strip()
        paragraph = most_related_paragraph(title,data[title]["paragraph"])
        ret_val.append({"paragraph": paragraph, "author":data[title]["author"], "link": data[title]["link"]})
    return ret_val

if __name__ == '__main__':
    print(json.dumps(paragraph_rank(sys.argv[1],int(sys.argv[2]))))
