from utils import word_parse
from flask import Flask, request, jsonify
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/video', methods=['GET'])
def hello_world():
    content = request.args.get('content')
    bopomofo = word_parse.get_bopomofo(content)
    return jsonify(bopomofo)

app.run(host='127.0.0.1', port=8080)
