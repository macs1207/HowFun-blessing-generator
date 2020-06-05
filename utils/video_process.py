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
        self.output_dir = {
            "mp4": "video",
            "mp3": "audio"
        }

    def get_media(self, text, file_format="mp4"):
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
        
        media_id = str(base64.urlsafe_b64encode(text.encode("utf-8")), "utf-8")
        media_path = os.path.join(self.output_dir[file_format], f"{media_id}.{file_format}")
        if os.path.exists(media_path):
            return self.output_dir[file_format], media_id
        
        tmp_file = os.path.join("tmp", f"{media_id}.txt")
        
        with open(tmp_file, 'w', encoding='utf-8') as f:
            for path in paths:
                f.writelines(f"file '{path}'\n")
        
        self.combine(media_id, file_format)
        os.remove(tmp_file)
        return self.output_dir[file_format], media_id

    def combine(self, media_id, file_format="mp4"):
        input_path = os.path.join("tmp", f"{media_id}.txt")
        output_path = os.path.join(self.output_dir[file_format], f'{media_id}.{file_format}')
        command = {
            "mp4": ['ffmpeg', '-f', 'concat', '-safe', '0',
                       '-i', input_path, '-c', 'copy', os.path.join("video", f'_{media_id}.mp4')],
            "mp3": ['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                    '-i', input_path, '-b:a', '192K', '-vn', os.path.join("video", f'_{media_id}.mp3')]
        }   

        rs = run(command[file_format], stdin=PIPE, stdout=PIPE, shell=True)
        if rs.returncode:
            raise VideoCombinedError()

        command = {
            "mp4": ['ffmpeg', '-y', '-i', os.path.join("video", f'_{media_id}.mp4'),
                    '-filter_complex', '[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]',
                    '-map', '[v]', '-map', '[a]', output_path],
            "mp3": ['ffmpeg', '-y', '-i', os.path.join("video", f'_{media_id}.mp3'),
                    '-filter:a', 'atempo=2.0', '-vn', output_path]
        }

        rs = run(command[file_format], stdin=PIPE, stdout=PIPE, shell=True)
        os.remove(os.path.join("video", f'_{media_id}.{file_format}'))
        if rs.returncode:
            raise VideoCombinedError("Adjust media speed failed.")
        
        

