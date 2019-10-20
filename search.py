#%%
import metapy
import inspect
#%%
idx = metapy.index.make_inverted_index('main.toml')
#%%
idx.num_docs()
#%%
idx.avg_doc_length()
#%%
ranker = metapy.index.OkapiBM25()
#%%
query = metapy.index.Document()
query.content('mining') # query from AP news
#%%
top_docs = ranker.score(idx, query, num_results=5)
top_docs
#%%
for num, (d_id, _) in enumerate(top_docs):
#     print(idx.metadata(d_id).__dict__())
#     print(inspect.getdoc(idx.metadata(d_id)))
    content = idx.metadata(d_id).
    idx.
    content = idx.metadata(d_id).get('hello')
    print(content)
#     print("{}. {}...\n".format(num + 1, content[0:250]))
#%%
