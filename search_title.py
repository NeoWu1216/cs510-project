import sys
import metapy
import os
# Path of parsed papers
path_parsed = "./test/"
# path_parsed = ""
def query(string):
	### get all papers content ###
    with open(path_parsed + 'test.dat', "r") as f:
        papers = f.read().split('\n')
        # print papers[0]
        # exit()
        
    # Create inverted index
    idx = metapy.index.make_inverted_index('main.toml')
    # print idx
    # exit()
    # Initialize ranker
    ranker = metapy.index.OkapiBM25()
    # Initialize query
    q = metapy.index.Document()
    q.content(string)
    # print q.content(string)
    # exit()
    # Get documents
    top_docs = ranker.score(idx, q, num_results=5)
    # Construct search results
    search_result = ""
    for d_id, _ in top_docs:
        search_result += papers[d_id]
        search_result += "<br><br>"
    title = search_result.split('|')[0].strip('.xml')
    title = os.path.splitext(title)[0]
    title = os.path.splitext(title)[0]
    return title

if __name__ == '__main__':
    print(query(sys.argv[1]))
