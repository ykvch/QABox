"""
Test obtaining peak audio values with PyAV:
time python pyav_audio_vol.py ~/Videos/sample.mp4

Reference:
https://ffmpeg.org/doxygen/trunk/group__lavu__sampfmts.html
"""


import sys
import av
import numpy as np
# import matplotlib.pyplot as plt

video_file = sys.argv[1]

container = av.open(video_file)
audioStream = container.streams.audio[0]
audio_max = np.fromiter((np.abs(frame.to_ndarray()).max() for frame in
         container.decode(audioStream)), np.float)
print(audio_max.max())
# with open("out.bin", "bw") as out_f:
#     np.save(out_f,audio_max)

# plt.plot(audio_max)
# plt.show()
