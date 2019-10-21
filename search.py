import sys
import metapy

# Path of parsed papers
path_parsed = "./parsed_paper/"

def query(string):
    with open(path_parsed + 'parsed_paper.dat', "r", encoding='utf-8') as f:
        papers = f.read().split('\n')
        
    # Create inverted index
    idx = metapy.index.make_inverted_index('main.toml')
    # Initialize ranker
    ranker = metapy.index.OkapiBM25()
    # Initialize query
    q = metapy.index.Document()
    q.content(string)
    # Get documents
    top_docs = ranker.score(idx, q, num_results=5)
    # Construct search results
    search_result = ""
    for d_id, _ in top_docs:
        search_result += papers[d_id]
        search_result += "<br><br>"
        
    return search_result

if __name__ == '__main__':
    print(query(sys.argv[1]))
