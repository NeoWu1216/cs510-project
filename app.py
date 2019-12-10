from flask import Flask, request, render_template, jsonify,current_app
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

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, threaded=True, debug=False)
