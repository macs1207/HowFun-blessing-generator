from utils import word_parse
from utils.video_process import VideoProcessor, VideoNotFoundError, VideoCombinedError
from flask import Flask, request, jsonify, make_response, abort, send_file
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
if not os.path.exists("tmp"):
    os.mkdir("video")


@app.route('/video', methods=['GET', 'POST'])
def get_video():
    if request.method == 'GET':
        video_id = request.values.get('v')
        file_path = os.path.join("video", f"{video_id}.mp4")

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            abort(404)

@app.route('/api/video', methods=['POST'])
def make_video():
    if request.method == 'POST':
        text = request.values.get('text')
        
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
        except VideoCombinedError as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)

if __name__ == "__main__":
    app.run(host=args.host, port=args.port, debug=args.debug)
