from flask import Flask, request, render_template, jsonify
import search
import sys
import os
import time
import threading
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    # restart_app()
    return render_template('index.html')

@app.route("/query", methods=['POST'])
def query():
    query_string = request.json["queryString"]
    print(query_string)
    # restart_app()
    output = subprocess.Popen(['python3' ,'search.py', query_string], stdout=subprocess.PIPE).stdout.read()
    return jsonify([output.decode('utf8')])

def restart_app_internal():
    time.sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)

def restart_app(*items):
    t = threading.Thread(target=restart_app_internal)
    t.start()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, threaded=True, debug=False)
