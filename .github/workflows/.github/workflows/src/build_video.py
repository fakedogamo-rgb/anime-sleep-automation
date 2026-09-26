#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
assets = root / 'assets'
output = root / 'output'
output.mkdir(exist_ok=True)

background = assets / 'background.mp4'
music = assets / 'music.mp3'
minutes = int(os.environ.get('VIDEO_MINUTES', '1'))
duration = minutes * 60

if minutes < 1:
    raise SystemExit('VIDEO_MINUTES must be at least 1')
if not background.exists():
    raise SystemExit('Missing assets/background.mp4. Add media you created or are licensed to use.')

video_input = ['-stream_loop', '-1', '-i', str(background)]
if music.exists():
    audio_input = ['-stream_loop', '-1', '-i', str(music)]
    maps = ['-map', '0:v:0', '-map', '1:a:0']
    audio = ['-c:a', 'aac', '-b:a', '128k', '-af', 'volume=0.25']
else:
    audio_input = []
    maps = ['-map', '0:v:0']
    audio = ['-an']

cmd = ['ffmpeg', '-y', *video_input, *audio_input, *maps,
       '-t', str(duration), '-vf',
       'scale=1280:720:force_original_aspect_ratio=decrease,'
       'pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p',
       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '28',
       *audio, '-movflags', '+faststart', str(output / 'anime-sleep.mp4')]

subprocess.run(cmd, check=True)
print(f'Created {output / "anime-sleep.mp4"} ({minutes} minutes)')
