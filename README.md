# cs510-project

## Preproject

### Tool used  
We mainly used metapy for the purpose of this project.  

### Data preprocessing
For metapy engine to operate properly, we need to put each file in one line inside a dat file. To do this, we wrote a simple python script. Instead of putting all the file content, we simply strip out title and abstract and use that as our file representation.

### Search Engine
We used metapy's builtin OkapiBM25 as our ranker. We tested many simple queries to verify its performance. 
