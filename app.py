from flask import Flask, request, render_template, jsonify,current_app
from flask_cors import CORS
import json
import subprocess
import pickle

# load lda mapping
lda_file_path = 'lda/gensim-topic-mapping.p'
with open(lda_file_path, 'rb') as fp:
    lda_raw_dict = pickle.load(fp)


def get_lda_prob(title, topic):
    candidate_topics = lda_raw_dict[title.strip()]
    print(title, topic, candidate_topics)
    for prob, cand_topic in candidate_topics:
        if cand_topic == topic:
            return prob 
    return 0


# mapping = {0:"Dataset", 1:"Graphic", 2:"Video", 3:"Similarity", 4:"Object Detection", 5:"Convolution", 6:"Points"}



app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return current_app.send_static_file('index.html')

@app.route("/query", methods=['POST'])
def query():
    query_string = request.json["queryString"]
    output = subprocess.Popen(['python3' ,'search.py', query_string], stdout=subprocess.PIPE).stdout.read()
    return jsonify([output.decode('utf8')])

@app.route("/query_title_paragraph", methods=['POST'])
def query_title_paragraph():
    query_string = request.json["queryString"]
    output = subprocess.Popen(['python3' ,'search_title_paragraph.py', query_string, "10"], stdout=subprocess.PIPE).stdout.read()
    print(output.decode('utf-8'))
    return jsonify(json.loads(output.decode('utf8')))

@app.route("/query_topic", methods=['POST'])
def query_topic():
    query_string = request.json["queryString"]
    topic_string = request.json["topicString"]
    output = subprocess.Popen(['python3' ,'search_title.py', query_string, "100"], stdout=subprocess.PIPE).stdout.read()
    print('Output', type(output))
    print(output.decode('utf8'))
    output_json = json.loads(output.decode('utf8'))

    lst_json = output_json
    # sort result by how much it matches the given topic
    lst_json.sort(key=lambda x: -get_lda_prob(x, topic_string))
    # remove other topics
    lst_json = [x for x in lst_json if get_lda_prob(x, topic_string) != 0]
    return jsonify(lst_json)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, threaded=True, debug=False)
