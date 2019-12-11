# cs510-preproject


## Tool used  
We mainly used metapy for the purpose of this project to construct a demo search engine  

## Demo App
https://cs510-project.herokuapp.com

## Developer's guide

### Local
To run frontend, just `yarn && yarn start`. You have to run backend individually `python3 app.py`

### Deployment
To deploy, just `yarn && yarn build && cp -r ./frontend/build/static . && cp ./static/index.html ./static`
