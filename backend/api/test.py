import ffmpeg
import os
from pathlib import Path

# os.system('ffmpeg -version')

probe = ffmpeg.probe(filename='a.mp4')
video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
video_length = video_info['duration']
print(video_length)

a = Path("C:\\Users\\12009\\Pictures\\Cyberpunk 2077")
files_in_basepath = (entry for entry in a.iterdir() if entry.is_file())
for item in files_in_basepath:
    print(item.absolute())