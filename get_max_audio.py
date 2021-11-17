"""
Test obtaining peak audio values with PyAV:
time python pyav_audio_vol.py ~/Videos/sample.mp4

Reference:
https://ffmpeg.org/doxygen/trunk/group__lavu__sampfmts.html
"""


import sys
import av
import numpy as np
import matplotlib.pyplot as plt

video_file = sys.argv[1]

container = av.open(video_file)
audioStream = container.streams.audio[0]

def rms(x):  # https://stackoverflow.com/a/28398092 o_O noice!
    return np.sqrt(np.vdot(x, x)/x.size)

audio_max = np.fromiter((rms(frame.to_ndarray()) for frame in
         container.decode(audioStream)), np.float)
print(audio_max.max())
# with open("out.bin", "bw") as out_f:
#     np.save(out_f,audio_max)

plt.plot(audio_max)
plt.show()
