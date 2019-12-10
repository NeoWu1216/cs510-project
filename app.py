from flask import Flask, request, render_template, jsonify,current_app
import json
import subprocess

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, threaded=True, debug=False)
