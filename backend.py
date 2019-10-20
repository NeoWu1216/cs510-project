from flask import Flask, request, render_template, jsonify
import search

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/query", methods=['POST'])
def query():
    query_string = request.json["queryString"]
    print(query_string)
    return jsonify([search.query(query_string)])


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug=False)
