import ffmpeg
import os


# os.system('ffmpeg -version')

probe = ffmpeg.probe(filename='a.mp4')
video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
video_length = video_info['duration']
print(video_length)
