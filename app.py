from flask import Flask, request, render_template, jsonify,current_app
from flask_cors import CORS
import json
import subprocess
import pickle
import collections

# load lda mapping
lda_file_path = 'lda/gensim-topic-mapping.p'
with open(lda_file_path, 'rb') as fp:
    lda_raw_dict = pickle.load(fp)
with open('test/test.json', 'r') as fp:
    test_jsn = json.load(fp)
with open('label_to_title.json', 'r') as fp:
    label_to_title = json.load(fp)


def get_lda_prob(title, topic):
    candidate_topics = lda_raw_dict[title.strip()]
    print(title, topic, candidate_topics)
    for prob, cand_topic in candidate_topics:
        if cand_topic == topic or topic == 'All':
            return prob 
    return 0


# mapping = {0:"Dataset", 1:"Graphic", 2:"Video", 3:"Similarity", 4:"Object Detection", 5:"Convolution", 6:"Points"}



app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return current_app.send_static_file('index.html')

@app.route("/query_all", methods=['POST'])
def query_all():
    print(label_to_title)
    return jsonify(label_to_title)

@app.route("/query_title", methods=['POST'])
def query_title():
    query_string = request.json["queryString"]
    output = subprocess.Popen(['python3' ,'search_title.py', query_string, "10"], stdout=subprocess.PIPE).stdout.read()
    print(output.decode('utf-8'))
    return jsonify(json.loads(output.decode('utf8')))

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

    lst_json = list(map(lambda x: x.strip(), output_json))
    # sort result by how much it matches the given topic
    lst_json.sort(key=lambda x: -get_lda_prob(x, topic_string))
    # remove other topics
    
    lst_json = [{'title':x, 'link':test_jsn[x]['link']} for x in lst_json if get_lda_prob(x, topic_string) != 0]
    return jsonify(lst_json)
@app.route("/query_similar", methods=['POST'])
def query_similar():
    query_title = request.json["queryString"]
    print(query_title)
    summary = []
    for title in query_title:
        query_string = test_jsn[title]["abstract"]
        output = subprocess.Popen(['python3' ,'search_title.py', query_string, "100"], stdout=subprocess.PIPE).stdout.read()
        summary += json.loads(output.decode('utf8'))
    print(summary)
    summary = collections.Counter(summary)
    print(summary)
    output = []
    for title, cnt in sorted(summary.items(), key = lambda item: item[1], reverse=True)[:(min(len(summary), 30))]:
        title = title.strip()
        output.append({"title":title, "link":test_jsn[title]})

    return jsonify(output)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, threaded=True, debug=False)
