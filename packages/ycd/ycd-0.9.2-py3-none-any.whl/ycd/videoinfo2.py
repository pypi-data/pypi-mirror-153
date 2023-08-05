import requests
import re
import time
from .exceptions import InvalidVideoIdException, UnknownConnectionError
from .util import extract_video_id
from . settings import Settings


API_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&fields=items(id,snippet(channelId,title,channelTitle,publishedAt),contentDetails(duration))"


tt = re.compile(
    r"^P?([0-9]*Y)?([0-9]*M)?([0-9]*D)?T?([0-9]*H)?([0-9]*M)?([0-9]*S)?")
units = {"D": 24*60*60, "H": 60*60, "M": 60, "S": 1}


def convert_duration(duration):
    if duration is None:
        return 0
    s = 0
    t = tt.search(duration)
    for i in range(2, 7):
        if t.group(i) is not None:
            s += (int(t.group(i)[:-1])*(int)(units.get(t.group(i)[-1])))
    return s


class VideoInfo:
    '''
    VideoInfo object retrieves YouTube video information.

    Parameter
    ---------
    video_id : str

    Exception
    ---------
    InvalidVideoIdException :
        Occurs when video_id does not exist on YouTube.
    '''

    def __init__(self, video_id):
        self.video_id = extract_video_id(video_id)
        self.client = requests.Session()
        self.api_key = Settings().config['api_key']
        err = None
        for _ in range(3):
            try:
                text = self._get_page_text(self.video_id)
                self._parse(text)
                break
            except (InvalidVideoIdException, UnknownConnectionError) as e:
                raise e
            except Exception as e:
                err = e
                time.sleep(2)
                pass
        else:
            raise err

    def _get_page_text(self, video_id):

        err = None
        for _ in range(3):
            try:
                resp = self.client.get(
                    API_ENDPOINT+f"&id={video_id}&key={self.api_key }")
                resp.raise_for_status()
                break
            except requests.HTTPError as e:
                err = e
                time.sleep(3)
        else:
            raise UnknownConnectionError(str(err))

        return resp.json()

    def _parse(self, text):
        self.duration = text["items"][0]["contentDetails"]["duration"]
        self.channelId = text["items"][0]["snippet"]["channelId"]
        self.channelTitle = text["items"][0]["snippet"]["channelTitle"]
        self.title = text["items"][0]["snippet"]["title"]

    def get_duration(self):
        return convert_duration(self.duration)

    def get_title(self):
        return self.title

    def get_channel_id(self):
        return self.channelId

    def get_channel_name(self):
        return self.channelTitle
