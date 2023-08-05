import requests
import re
from . import api
from ..videoinfo2 import VideoInfo


mobile_user_agent = 'Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'
mobile_ua = (('User-Agent', mobile_user_agent),)
headers_mobile = (
    ('Accept', '*/*'),
    ('Accept-Language', 'en-US,en;q=0.5'),
    ('X-YouTube-Client-Name', '2'),
    ('X-YouTube-Client-Version', '2.20180830'),
) + mobile_ua

channel_id_re = re.compile(r'videos\.xml\?channel_id=([a-zA-Z0-9_-]{24})"')
ch_id_pattern_0 = re.compile(r'(^PL[\w-]+)')
ch_id_pattern_1 = re.compile(r'/playlist\?list=(PL[\w-]+)')


def get_playlist_id(base_url):
    match = re.search(ch_id_pattern_0, base_url)
    if match:
        return match.group(1)

    match = re.search(ch_id_pattern_1, base_url)
    if match:
        return match.group(1)

    # match = re.search(ch_id_pattern_2, base_url)
    # if match:
    #     client = requests.Session()
    #     base_url = 'https://m.' + match.group(1)
    #     response = client.get(base_url + '/about?pbj=1',
    #                           headers=dict(headers_mobile)).text
    #     match = channel_id_re.search(response)
    #     if match:
    #         return match.group(1)
    return None


def get_videos_from_playlist(playlist_id):
    cache = set()
    cache.add("")
    counter = 0
    for items in api.get_video_items(playlist_id):
        for item in items:

            if not item:
                return
            video = parse(item)
            if video.get('id') in cache:
                counter += 1
                if counter > 20:
                    return
                continue
            cache.add(video.get('id'))
            yield video


def parse(item):
    video = dict()
    try:
        video["id"] = item["snippet"]["resourceId"]["videoId"]
        video["title"] = video["time_published"] = item["snippet"]["title"]
        video["time_published"] = item["snippet"]["publishedAt"]
        video["author"] = item["snippet"]["channelTitle"]
        info = VideoInfo(video["id"])
        video['duration'] = info.get_duration()
        return video
    except KeyError as e:
        print(type(e), str(e))
        video["error"] = True
        return video
    except Exception:
        video["error"] = True
        return video


# def get_video_ids(playlist_id):
#     cache = set()
#     cache.add("")
#     counter = 0
#     for items in api.get_video_items(playlist_id):
#         for item in items:

#             if not item:
#                 return
#             video_id = parse_id(item)
#             if video_id in cache:
#                 counter += 1
#                 if counter > 20:
#                     return
#                 continue
#             cache.add(video_id)
#             yield video_id


def parse_id(item):
    try:
        video_id = item["snippet"]["resourceId"]["videoId"]
        return video_id
    except KeyError as e:
        print(type(e), str(e))
        return "vid_error"
