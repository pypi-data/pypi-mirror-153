# from ycd import videoinfo2
# info = videoinfo2.VideoInfo("rJoy6e48MIo")
# ycd\ycd\youtube
from .youtube.channel import get_videos_ex
# print(info.get_title())
counter=0
ret=[]
for video in get_videos_ex("UCD-miitqNY3nyukJ4Fnf4_A"):
                print(video)
                # ret = self.video(video)
                # if ret:
                ret.append(video)
                counter += 1

print(counter)
import pickle
with open("yt_json.bin",mode="wb") as f:
    pickle.dump(ret,f)
# print(ret)