import subprocess
cmd = [
    'ffmpeg', '-i', 'test_video.mp4', '-vf',
    "drawtext=text='test':fontfile='C\\:/Windows/Fonts/arial.ttf'",
    '-y', 'out.mp4'
]
print(subprocess.run(cmd, capture_output=True, text=True).stderr)
