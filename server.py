from utils.feedback import save_to_db
from utils.video_process import VideoProcessor, VideoNotFoundError, VideoCombinedError
from flask import Flask, request, jsonify, make_response, abort, send_file, render_template, url_for
import os
import logging
import json
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
if not os.path.exists("audio"):
    os.mkdir("audio")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/video', methods=['GET'])
def get_video():
    video_id = request.values.get('v')
    if video_id is not None:
        file_path = os.path.join("video", f"{video_id}.mp4")

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            abort(404)
    else:
        return make_response("need video id", 400)

@app.route('/audio', methods=['GET'])
def get_audio():
    audio_id = request.values.get('a')
    if audio_id is not None:
        file_path = os.path.join("audio", f"{audio_id}.mp3")

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            abort(404)
    else:
        return make_response("need audio id", 400)

@app.route('/resource', methods=['GET'])
def get_resource():
    r = request.values.get('r')
    if r is not None:
        file_path = os.path.join("resource", r)

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            abort(404)
    else:
        return make_response("need resource id", 400)

@app.route('/api/media', methods=['POST'])
def make_video():
    text = request.values.get('text')
    file_format = request.values.get('format')
    if text is not None:
        text = text.strip()
        if len(text) == 0:
            return make_response(jsonify({
                "error": "text is empty",
            }), 400)
        if len(text) > 50:
            return make_response(jsonify({
                "error": "text is too long",
            }), 400)
        try:
            dir_path, media_id = VideoProcessor().get_media(text, file_format)
            print(media_id)
            return jsonify({
                "media_id": media_id,
                "path": dir_path
            })
        except VideoNotFoundError as e:
            logging.error(e)
            return make_response(jsonify({
                "error": "video not found error",
                "detail": e.detail
            }), 500)
        except VideoCombinedError as e:
            logging.error(e)
            return make_response(jsonify({
                "error": "combine error",
            }), 500)
        except Exception as e:
            logging.error(e)
            return make_response(jsonify({
                "error": "unknown error",
            }), 500)
    else:
        return make_response(jsonify({
            "error": "need text",
        }), 400)

@app.route('/api/feedback', methods = ['POST'])
def feedback():
    feedback = request.values.get('feedback')
    if feedback is None:
        return make_response("need feedback", 400)
    feedback = feedback.strip()
    if len(feedback) == 0:
        return make_response("feedback is empty", 400)
    if len(feedback) > 500:
        return make_response("feedback is too long", 400)
    save_to_db(feedback)
    return make_response("successful", 200)
    
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
