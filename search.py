import metapy
import inspect

idx = metapy.index.make_inverted_index('main.toml')
idx.num_docs()
idx.avg_doc_length()
ranker = metapy.index.OkapiBM25()
with open('./parsed_paper/parsed_paper.dat', encoding='utf8') as input_file:
    all_lines = input_file.read().split('\n')

def query(string):
    q = metapy.index.Document()
    q.content(string) # query from AP news

    top_docs = ranker.score(idx, q, num_results=5)

    str_to_return = ""
    for num, (d_id, _) in enumerate(top_docs):
#     print(idx.metadata(d_id).__dict__())
#     print(inspect.getdoc(idx.metadata(d_id)))
        content = idx.metadata(d_id)
        str_to_return+= all_lines[d_id]
        str_to_return += "<br>"
    return str_to_return