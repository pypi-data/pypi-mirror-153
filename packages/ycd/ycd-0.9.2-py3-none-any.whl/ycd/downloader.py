import asyncio
import os
import time
from chat_downloader import ChatDownloader, utils
from chat_downloader.output.continuous_write import ContinuousWriter
from ycd.youtube.channel import get_videos
from ycd.youtube.playlist import get_videos_from_playlist
from .arguments import Arguments
from json.decoder import JSONDecodeError
from pathlib import Path
from .videoinfo2 import VideoInfo
from .exceptions import InvalidVideoIdException, NoContents, PatternUnmatchError, ZeroDuration
from .progressbar import ProgressBar
from .util import extract_video_id, checkpath
from . import util
from typing import List, Dict
from .youtube import channel
from .youtube import playlist
import sys

class Downloader:

    def __init__(self, dir_videos: set):
        self._dir_videos = dir_videos


    def video(self, video) -> None:
        is_complete = False
        video_id = extract_video_id(video.get('id'))
        try:
            if not os.path.exists(Arguments().output):
                raise FileNotFoundError
            separated_path = str(Path(Arguments().output)) + os.path.sep
            path = checkpath(separated_path + video_id + '.txt')
            # check if the video_id is already exists the output folder
            if video_id in self._dir_videos:
                # raise Exception(f"Video [{video_id}] is already exists in {os.path.dirname(path)}. Skip process.")
                print(
                    f"Video [{video_id}] is already exists in {os.path.dirname(path)}. Skip process.")
                sys.argv = []
                return

            print(
                f"\n"
                f"[title]    {video.get('title')}\n"
                f"[id]       {video_id}    [published] {video.get('time_published')}\n"
                f"[channel]  {video.get('author')}"
            )
            print(f"[path]     {path}  [duration]{video.get('duration')}")

            duration = video["duration"]
            if duration == 0:
                return
            url = f"https://www.youtube.com/watch?v={video_id}"
            downloader = ChatDownloader()
            chat = downloader.get_chat(url)
            writer = ContinuousWriter(
                path, indent=14, sort_keys=True, overwrite=True)

            pbar = ProgressBar(int(duration) * 1000, status='Extracting...'+" "*20)

            for item in chat:
                    time_in_seconds = item.get('time_in_seconds')
                    pbar._disp(None, time_in_seconds)
                    writer.write(chat.format(item), flush=True)

            pbar.reset(total=1, status="Complete.   ")
            pbar._disp(None, 1)
            pbar.reset(status="Complete.")
            print()

            is_complete = True

        except InvalidVideoIdException:
            print("Invalid Video ID or URL:", video_id)
        except NoContents as e:
            print('---' + str(e)[:80] + '---')
        except FileNotFoundError:
            print("The specified directory does not exist.:{}".format(
                Arguments().output))
            exit(0)
        except (JSONDecodeError, PatternUnmatchError) as e:
            print(type(e),str(e))
            if Arguments().save_error_data:
                util.save(e.doc, "ERR_", ".dat")
        except ZeroDuration:
            print("Duration of this video is zero. Skip process.")
        except Exception as e:
            print(str(e))
        finally:
            clear_tasks()
            return is_complete

    def videos(self, video_ids: List[int]) -> None:
        for i, video_id in enumerate(video_ids):
            print(f"\n{'-'*10} video:{i+1} of {len(video_ids)} {'-'*10}")
            if '[' in video_id or ']' in video_id:
                video_id = video_id.replace('[', '').replace(']', '')
            try:
                video = self.get_info(video_id)
                if video.get('error'):
                    continue
                self.video(video)
            except InvalidVideoIdException:
                print(f"Invalid video id: {video_id}")
                continue

    def channels(self, channels: List[str]) -> None:
        for i, ch in enumerate(channels):
            counter = 0
            for video in get_videos(channel.get_channel_id(ch)):
                if counter > Arguments().first - 1:
                    break
                print(
                    f"\n{'-'*10} channel: {i+1} of {len(channels)} / video: {counter+1} of {Arguments().first} {'-'*10}")
                ret = self.video(video)
                if ret:
                    counter += 1

    def playlist_ids(self, playlist_ids: List[str]) -> None:
        for i, pl_id in enumerate(playlist_ids):
            counter = 0
            for video in get_videos_from_playlist(playlist.get_playlist_id(pl_id)):
                if counter > Arguments().first - 1:
                    break
                print(
                    f"\n{'-'*10} playlist: {i+1} of {len(playlist_ids)} / video: {counter+1} of {Arguments().first} {'-'*10}")
                ret = self.video(video)
                if ret:
                    counter += 1

    def cancel(self, ex, pbar) -> None:
        '''Called when keyboard interrupted has occurred.
        '''
        print("\nKeyboard interrupted.\n")
        if ex:
            ex.cancel()
        if pbar:
            pbar.cancel()
        exit(0)

    def get_info(self, video_id: str) -> Dict:
        video = dict()
        for i in range(3):
            try:
                info = VideoInfo(video_id)
                break
            except PatternUnmatchError:
                time.sleep(2)
                continue
        else:
            print(f"PatternUnmatchError:{video_id}")
            return {'error': True}

        video['id'] = video_id
        video['author'] = info.get_channel_name()
        video['time_published'] = "Unknown"
        video['title'] = info.get_title()
        video['duration'] = info.get_duration()
        return video


def clear_tasks():
    '''
    Clear remained tasks.
    Called when internal exception has occurred or
    after each extraction process is completed.
    '''
    async def _shutdown():
        tasks = [t for t in asyncio.all_tasks()
                 if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_shutdown())
    except Exception as e:
        print(e)
