"""
Test obtaining peak audio values with PyAV:
time python pyav_audio_vol.py ~/Videos/sample.mp4

Reference:
https://ffmpeg.org/doxygen/trunk/group__lavu__sampfmts.html
"""


import sys
import av
from numpy import abs, sqrt, vdot, fromiter, float64, uint8, average, frombuffer, mean
import matplotlib.pyplot as plt

video_file = sys.argv[1]

container = av.open(video_file)
audio_stream = container.streams.audio[0]
# audio_stream.thread_type = "AUTO"
video_stream = container.streams.video[0]
video_stream.thread_type = "AUTO"

def rms(x):  # https://stackoverflow.com/a/28398092 o_O noice!
    return sqrt((vdot(x, x)>0.1)/x.size)
    # np.diff, np.gradient
    # np.where(np.convolve(all_frames_array, [1,1,-1,-1])>.7)

# audio_max = fromiter(((frame.pts, rms(frame.to_ndarray())) for frame in
# audio_max = fromiter((rms(frame.to_ndarray()) for frame in
#          container.decode(video_stream, audio_stream)), float64)
# zero for luma
# video_max = fromiter((average(frame.to_ndarray()[0].size) for frame in

video_max = fromiter((mean(frombuffer(frame.planes[0], uint8).reshape(1920, 1080)[1200:,:500]) for frame in
         container.decode(video_stream)), uint8)

# videos = [f for f in container.decode(video=0)]
# import pdb; pdb.set_trace()
container.close()
print(video_max.max())
# print(audio_max.max())
# with open("out.bin", "bw") as out_f:
#     save(out_f,audio_max)

# plt.plot(video_max)
# plt.show()
