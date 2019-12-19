# cs510-preproject


## Tool used  
We mainly used metapy for the purpose of this project to construct a demo search engine  

## Demo App
http://cs510-project.herokuapp.com

## Developer's guide

### Local
To run frontend, just `cd frontend && yarn && yarn start`. You have to run backend individually `pip3 install -r requirements.txt && python3 app.py`

### Deployment
To deploy, just `cd frontend && yarn && yarn build && cp ./build/index.html ./build/static && cp -r ./build/static ..`

### Topic Modeling
We implemented Latent Dirichlet Allocation (LDA) using both metapy and Gensim. LDA takes text corpus as input and output the word distributions of topics and topic proportion of documents.
##### To use Gensim to generate topic distributions:
First change the number of topic at line 88 in `gensim_.py`, for example, to set the number of topics to be 7:
```python
if not os.path.isfile('gensim_model'):
	tpc = 7
	lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
						id2word=id2word,
						num_topics=tpc, 
						random_state=100,
						update_every=1,
						chunksize=100,
						passes=10,
						alpha='auto',
						per_word_topics=True)
```
then run `python gensim_.py` to execute the program.

##### To use Metapy to generate topic distributions:
Run the following with number of topics as the first argument
```python
python lda.py <number of topics>
```
For example, to generate 7 topics, run `python lda.py 7`
