import argparse
import os
from .arguments import Arguments
from .downloader import Downloader
from .settings import Settings
from .youtube import api
from pathlib import Path
try:
    from asyncio import CancelledError
except ImportError:
    from asyncio.futures import CancelledError
'''
Most of CLI modules refer to
Petter Kraabøl's Twitch-Chat-Downloader
https://github.com/PetterKraabol/Twitch-Chat-Downloader
(MIT License)

'''

__copyright__ = 'Copyright (C) 2020,2021 vb'
__version__ = '0.9.2'
__license__ = 'AGPLv3'
__author__ = 'vb'
__author_email__ = 'i@s.biz'
__url__ = "http://example.com"


def main():

    parser = argparse.ArgumentParser(description=f'ycd v{__version__}')
    parser.add_argument('-v', f'--{Arguments.Name.VIDEO}', type=str,
                        help='Video ID (or URL that includes Video ID).'
                        'You can specify multiple video IDs by '
                        'separating them with commas without spaces.\n'
                        'If ID starts with a hyphen (-), enclose the ID in square brackets.')
    parser.add_argument('-c', f'--{Arguments.Name.CHANNEL}', type=str,
                        help='Channel ID (or URL of channel page)')
    parser.add_argument(f'--{Arguments.Name.FIRST}', type=int,
                        default=5, help='Download chat from the last n VODs')
    parser.add_argument(f'--{Arguments.Name.API_KEY.replace("_", "-")}', type=str, help='YouTube API key')
    parser.add_argument('-o', f'--{Arguments.Name.OUTPUT}', type=str,
                        help='Output directory (end with "/"). default="./"', default='./')
    parser.add_argument('-e', f'--{Arguments.Name.SAVE_ERROR_DATA}', action='store_true',
                        help='Save error data when error occurs(".dat" file)')
    parser.add_argument(f'--{Arguments.Name.VERSION}', action='store_true',
                        help='Show version')
    parser.add_argument('-s', f'--{Arguments.Name.SKIP_DUPLICATE}', action='store_true',
                        help='Skip already extracted videos. This option is valid only when `-o` option is specified.')
    parser.add_argument(f'--{Arguments.Name.SETTINGS}', action='store_true', help='Print settings file location')
    parser.add_argument(f'--{Arguments.Name.SETTINGS_FILE.replace("_", "-")}', type=str,
                        # default=str(Path.home()) + '/.config/ycd/settings.json',
                        default=str(Path.home()) + '/.config/ycd/settings.json',
                        help='Use a custom settings file')
    parser.add_argument('-p', f'--{Arguments.Name.PLAYLIST}', type=str,
                        help='Playlist ID ("PL-")')
    parser.add_argument(f'--{Arguments.Name.SET_API}', action='store_true',
                        help='Set new API key')
    parser.add_argument(f'--{Arguments.Name.LOG}', action='store_true', help='Save log file')
    Arguments(parser.parse_args().__dict__)
    Settings(Arguments().settings_file,
             reference_filepath=f'{os.path.dirname(os.path.abspath(__file__))}/settings.reference.json.py')

    if not Settings().config.get('EULA', None) or not Settings().config.get('EULA', None) == 'agreed':
        print()
        print("!!CAUTION!!\n"
        "The use of this tool is at your own risk.\n"
        "The author of this program is not responsible for any damage \n"
        "caused by this tool or bugs or specifications\n"
        "or other incidental actions.\n"
        "You will be deemed to have agreed to the items listed in the LICENSE.\n"
        "Type `yes` if you agree with the above.\n")
        while True:
            ans = input()
            if ans == 'yes':
                Settings().config['EULA'] = "agreed"
                Settings().save()
                break
            elif ans == "":
                continue
            else:
                return

    # Print version
    if Arguments().print_version:
        print(f'v{__version__}')
        return

    # set api key
    if Arguments().set_api:
        if Settings().config.get('api_key', None):
            loop = True
            while loop:
                print(f"Change API Key:\n   [current key] {Settings().config.get('api_key', None)}")
                typed_apikey = ""
                while typed_apikey == "":
                    typed_apikey = input(f"Type new API Key:").strip()
                t= ""
                while not t:
                    t = input("Change OK? (y/n) ")
                    if t == "Y" or t == "y":
                        if api.check_validation(typed_apikey):
                            Settings().config['api_key'] = typed_apikey
                            Settings().save()
                            print("Changed the API key.")
                            loop = False
                            break
                        else:
                            print("[Error!] The entered API key is NOT valid or exceeds quota limit. Please try again or enter other key.\n")
                            q = input("...press any key to continue. (or press 'q' to quit)...")
                            if q == "Q" or q == "q":
                                loop = False
                                break
                    elif t == "N" or t == "n":
                        loop = False
                        break
                    else:
                        t = ""
        return


    if Arguments().api_key or Settings().config.get('api_key', None):
        Settings().config['api_key'] = Arguments().api_key or Settings().config.get('api_key', None)
    else:
        for i in range(3):
            typed_apikey = input('Enter YouTube API key: ').strip()
            if api.check_validation(typed_apikey):
                print("Confirmed the entered YouTube API key.")
                Settings().config['api_key'] = typed_apikey
                break
            print("The entered API key is NOT valid or exceeds quota limit. Please try again or enter other key.")
            print(f"--number of attempts:{3-i-1} remaining--")
            print()
        else:
            print("Unable to determine the valid YouTube API key, or you have exceeded the available quota.")
            print("(CANNOT support any inquiries about the YouTube API.)")
            return

    Settings().save()
    # Scan folder
    dir_videos = set()
    if Arguments().output:
        path = Arguments().output
    else:
        path = "./"
    if not os.path.exists(path):
        print(f"Directory not found:{path}")
        return
    if Arguments().skip_duplicate:
        print("Scanning output dirctory...")
        dir_videos.update([f[:11] for f in os.listdir(
            path) if os.path.isfile(os.path.join(path, f))])

    # Extract
    if Arguments().video_ids or Arguments().channels or Arguments().playlist_ids:
        try:
            if Arguments().video_ids:
                Downloader(dir_videos).videos(Arguments().video_ids)

            if Arguments().channels:
                Downloader(dir_videos).channels(Arguments().channels)

            if Arguments().playlist_ids:
                Downloader(dir_videos).playlist_ids(Arguments().playlist_ids)

            return
        except CancelledError:
            print('Cancelled')
            return

    parser.print_help()
