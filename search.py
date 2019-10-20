import metapy
# import importlib


# ranker = metapy.index.OkapiBM25()
with open('./parsed_paper/parsed_paper.dat', "r", encoding='utf-8') as input_file:
    all_lines = input_file.read().split('\n')

def query(string):
    # importlib.reload(metapy)
    idx = metapy.index.make_inverted_index('main.toml')
    idx.num_docs()
    idx.avg_doc_length()
    # print('received')
    ranker = metapy.index.OkapiBM25()
    q = metapy.index.Document()
    q.content(string) # query from AP news
    # print('created query doc')
    top_docs = ranker.score(idx, q, num_results=5)
    # print('found top 5')
    str_to_return = ""
    for num, (d_id, _) in enumerate(top_docs):
#     print(idx.metadata(d_id).__dict__())
#     print(inspect.getdoc(idx.metadata(d_id)))
# content = idx.metadata(d_id)
        str_to_return+= all_lines[d_id]
        str_to_return += "<br>"
    print(str_to_return)
    return str_to_return


if __name__ == '__main__':
    import sys
    print(sys.argv)
    print(query(sys.argv[1]))