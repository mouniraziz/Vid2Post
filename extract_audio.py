from moviepy.editor import *

def extract(Video_path, save_audio_path):
    video = VideoFileClip(Video_path) # 2.
    audio = video.audio # 3.
    audio.write_audiofile(save_audio_path) # 4.from moviepy.editor import *
