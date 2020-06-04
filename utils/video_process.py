from utils import word_parse
from subprocess import PIPE, run
from time import time
import os
import uuid
import base64


class VideoNotFoundError(Exception):
    def __init__(self, words):
        self.message = f'Video is not found. {str(words)}'
        self.detail = words
        super().__init__()
    
    def __str__(self):
        return f"{__name__}: {self.message}"
        

class VideoCombinedError(Exception):
    def __init__(self, message='Video combining is failed.'):
        self.message = message
        super().__init__(message)

class VideoProcessor:
    def __init__(self, path="resource"):
        self.path = path

    def get_video(self, text):
        words = word_parse.get_bopomofo(text)
        paths = []

        not_found_words = []
        for word in words:
            file_path = os.path.join(self.path, "words", f"{word}.mp4")
            if not os.path.exists(file_path):
                not_found_words.append(word)
            paths.append(file_path)
            
        if not_found_words:
            raise VideoNotFoundError(not_found_words)
        
        video_id = str(base64.urlsafe_b64encode(text.encode("utf-8")), "utf-8")
        video_path = os.path.join("video", f"{video_id}.mp4")
        if os.path.exists(video_path):
            return video_id
        
        tmp_file = os.path.join("tmp", f"{video_id}.txt")
        
        with open(tmp_file, 'w', encoding='utf-8') as f:
            for path in paths:
                f.writelines(f"file '{path}'\n")
        
        self.combine(video_id)
        os.remove(tmp_file)
        return video_id

    def combine(self, video_id):
        input_path = os.path.join("tmp", f"{video_id}.txt")
        output_path = os.path.join("video", f'{video_id}.mp4')

        command = ['ffmpeg', '-f', 'concat', '-safe', '0',
                   '-i', input_path, '-c', 'copy', os.path.join("video", f'_{video_id}.mp4')]

        rs = run(command, stdin=PIPE, stdout=PIPE, shell=True)
        if rs.returncode:
            raise VideoCombinedError()

        command = ['ffmpeg', '-y', '-i', os.path.join("video", f'_{video_id}.mp4'),
                   '-filter_complex', '[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]',
                   '-map', '[v]', '-map', '[a]', output_path]
        rs = run(command, stdin=PIPE, stdout=PIPE, shell=True)
        os.remove(os.path.join("video", f'_{video_id}.mp4'))
        if rs.returncode:
            raise VideoCombinedError("Adjust video setpts failed.")
        
        

