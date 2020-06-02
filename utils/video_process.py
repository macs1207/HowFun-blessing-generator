from subprocess import PIPE, run
from time import time
import os
import uuid


class VideoNotFoundError(Exception):
    def __init__(self, words):
        self.message = f'Video is not found. {str(words)}'
        super().__init__()
    
    def __str__(self):
        return f"{__name__}: {self.message}"
        

class VideoCombinedError(Exception):
    def __init__(self, message='Video combining is failed.'):
        self.message = message
        super().__init__(message)

class VideoProcessor:
    def __init__(self, path="data"):
        self.path = path

    def get_video(self, words):
        
        paths = []
        for word in words:
            file_path = os.path.join(self.path, "words", f"{word}.mp4")
            if not os.path.exists(file_path):
                raise VideoNotFoundError(words)
            paths.append(file_path)
        
        video_id = f"{uuid.uuid4()}"
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
                   '-filter_complex', '[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]',
                   '-map', '[v]', '-map', '[a]', output_path]
        rs = run(command, stdin=PIPE, stdout=PIPE, shell=True)
        os.remove(os.path.join("video", f'_{video_id}.mp4'))
        if rs.returncode:
            raise VideoCombinedError("Adjust video setpts failed.")
        
        
