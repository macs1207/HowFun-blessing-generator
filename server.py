from utils import word_parse
from utils.video_process import VideoProcessor, VideoNotFoundError, VideoCombinedError
from flask import Flask, request, jsonify, make_response, abort, send_file, render_template, url_for
import os
import logging
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-host', type=str, default='127.0.0.1')
parser.add_argument('-port', type=int, default=8080)
parser.add_argument('-d', '--debug', default=False, action="store_true")

args = parser.parse_args()

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.FileHandler('error.log', 'a', 'utf-8'), ])

app = Flask(__name__)

if not os.path.exists("tmp"):
    os.mkdir("tmp")
if not os.path.exists("video"):
    os.mkdir("video")


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/video', methods=['GET'])
def get_video():
    if request.method == 'GET':
        video_id = request.values.get('v')
        file_path = os.path.join("video", f"{video_id}.mp4")

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            abort(404)


@app.route('/resource', methods=['GET'])
def get_resource():
    if request.method == 'GET':
        r = request.values.get('r')
        file_path = os.path.join("resource", r)

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            abort(404)

@app.route('/api/video', methods=['POST'])
def make_video():
    if request.method == 'POST':
        text = request.values.get('text')
        text = text.strip()
        if len(text) == 0:
            return make_response("empty", 500)
        if len(text) > 50:
            return make_response("too long", 500)
        try:
            bopomofo = word_parse.get_bopomofo(text)
            v = VideoProcessor()
            video_id = v.get_video(bopomofo)
            print(video_id)
            return jsonify({
                "video_id": video_id
            })
        except VideoNotFoundError as e:
            logging.error(e)
            return make_response("not found", 500)
        except VideoCombinedError as e:
            logging.error(e)
            return make_response("unknown", 500)
        except Exception as e:
            logging.error(e)
            return make_response("unknown", 500)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(host=args.host, port=args.port, debug=args.debug)
