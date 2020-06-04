from subprocess import PIPE, run
import os
import json


class VideoSplitter:
    _LENGTH = 0.8
    
    def __init__(self, path="resource"):
        self.path = path
        self.timeline = None

    def words_iter(self, dir_name):
        file_path = os.path.join("dictionarys", f"{dir_name}.json")
        
        with open(file_path, "r", encoding="utf-8") as f:
            self.timeline = json.load(f)
        
        args = []
        for word, time_ in self.timeline.items():
            minute, sec = time_.split(":")
            minute, sec = int(minute), float(sec)
            sec = minute * 60 + sec
            file_name = os.path.join(
                self.path, "words",  dir_name, f'{word}.mp4')
            args.extend(['-ss', str(sec), '-t', str(self._LENGTH), file_name])
        # print(args)
        self.video_split(args)
        
    def video_split(self, args):
        file_path = os.path.join(self.path, "video.mp4")
        
        command = ['ffmpeg', '-y', '-i', file_path]
        command.extend(args)
        print(*command)

        run(command, stdin=PIPE, stdout=PIPE, shell=True)

if __name__ == "__main__":
    v = VideoSplitter()
    v.words_iter("ㄓ")
