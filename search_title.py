import sys
import metapy
import os
# Path of parsed papers
path_parsed = "./test/"
# path_parsed = ""
def query(string,top_num):
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
    top_docs = ranker.score(idx, q, num_results=top_num)
    # Construct search results
    search_result = ""
    for d_id, _ in top_docs:
        search_result += papers[d_id]
        search_result += "<br><br>"
    # print search_result
    # exit()
    ### split all documents ###
    all_title = search_result.split('<br><br>')
    title_list = []
    # print len(all_title)
    ### length ###
    length = len(all_title)
    # print all_title
    # exit()
    for i in range(length):
        if all_title[i] != '':
            tmp_content = all_title[i].split('|')[0]
            tmp_content = os.path.splitext(tmp_content)[0]
            tmp_content = os.path.splitext(tmp_content)[0]
            title_list.append(tmp_content)
        else:
            continue
    # print title_list
    # print len(title_list)

    return title_list

if __name__ == '__main__':
    print(query(sys.argv[1],int(sys.argv[2])))
