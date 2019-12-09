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

def paragraph_rank(string):
    #feature 2, return most related paragraph
    f = open(path_parsed + "test.json", 'r')
    data = json.load(f)
    title_list = search_title.query(string)
    ret_val = [] #list of (title. paragraph)
    for title in title_list:
        paragraph = most_related_paragraph(title,data[title]["paragraph"])
        ret_val.append((title,paragraph))
    return ret_val

if __name__ == '__main__':
    print(paragraph_rank(sys.argv[1]))