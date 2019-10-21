# cs510-preproject

## Preproject

### Tool used  
We mainly used metapy for the purpose of this project to construct a demo search engine  

### Data preprocessing
For metapy engine to operate properly, we need to put each file in one line inside a dat file. To do this, we wrote a simple python script. Instead of putting all the file content, we simply strip out title and abstract and use that as our file representation because we believe that they must contain the most important information and are most revelent to the user.

### Search Engine
We used metapy's builtin OkapiBM25 as our ranker. We tested many simple queries to verify its performance. We fit the corpus using the unigram language model. Eventually we added a simple frontend that can be accessed here.

### Instruction for preprocessing
python3 preprocess.py

### Instruction for deployment
python3 app.py

### Demo App
https://cs510-preproject.herokuapp.com
