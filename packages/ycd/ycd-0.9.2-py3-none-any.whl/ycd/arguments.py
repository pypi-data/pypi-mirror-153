from typing import Optional, Dict, Union, List
from .singleton import Singleton

'''
This modules refer to
Petter Kraabøl's Twitch-Chat-Downloader
https://github.com/PetterKraabol/Twitch-Chat-Downloader
(MIT License)
'''


class Arguments(metaclass=Singleton):
    """
    Arguments singleton
    """

    class Name:
        SETTINGS_FILE: str = 'settings_file'
        SETTINGS: str = 'settings'
        LOG: str = 'log'
        VERSION: str = 'version'
        OUTPUT: str = 'output_dir'
        VIDEO: str = 'video_id'
        SAVE_ERROR_DATA: bool = 'save_error_data'
        CHANNEL: str = 'channel'
        FIRST: str = 'first'
        SKIP_DUPLICATE: bool = 'skip_duplicate'
        API_KEY: str = 'api_key'
        PLAYLIST: str = 'playlist_id'
        SET_API: str = 'set_api'

    def __init__(self,
                 arguments: Optional[Dict[str, Union[str, bool, int]]] = None):
        """
        Initialize arguments
        :param arguments: Arguments from cli
        (Optional to call singleton instance without parameters)
        """

        if arguments is None:
            print('Error: arguments were not provided')
            exit()

        self.settings_file: str = arguments[Arguments.Name.SETTINGS_FILE]
        self.settings: str = arguments[Arguments.Name.SETTINGS]
        self.print_version: bool = arguments[Arguments.Name.VERSION]
        self.output: str = arguments[Arguments.Name.OUTPUT]
        self.video_ids: List[int] = []
        self.channels: List[int] = []
        self.playlist_ids: List[int] = []
        self.save_error_data: bool = arguments[Arguments.Name.SAVE_ERROR_DATA]
        self.first: Optional[int] = arguments[Arguments.Name.FIRST]
        self.skip_duplicate: bool = arguments[Arguments.Name.SKIP_DUPLICATE]
        self.log: bool = arguments[Arguments.Name.LOG]
        
        # Optional or prompted arguments
        self.api_key: Optional[str] = arguments[Arguments.Name.API_KEY]
        self.set_api: Optional[str] = arguments[Arguments.Name.SET_API]
        # Videos
        if arguments[Arguments.Name.VIDEO]:
            self.video_ids = arguments[Arguments.Name.VIDEO].split(',')
    
        if arguments[Arguments.Name.CHANNEL]:
            self.channels = arguments[Arguments.Name.CHANNEL].split(',')

        if arguments[Arguments.Name.PLAYLIST]:
            self.playlist_ids = arguments[Arguments.Name.PLAYLIST].split(',')
