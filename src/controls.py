import spotipy
import configparser
import os
from spotipy.oauth2 import SpotifyOAuth

class Controller:
    def __init__(self, config:object):
        """Initiazlization for Controller object

        Args:
            config (object): configuration object
        """        ''''''
        self.config = config
        self.auth = SpotifyOAuth(
            scope=config['SETTINGS']['SCOPE'],
            client_id= config['CREDENTIALS']['CLIENT_ID'],
            client_secret=config['CREDENTIALS']['CLIENT_SECRET'],
            redirect_uri=config['CREDENTIALS']['REDIRECT_URI']
        )
        self.device_id = self.config['SETTINGS']['DEVICE_ID']
        self.sp = spotipy.Spotify(auth_manager = self.auth)
        #self.sp.pause_playback()
        #self.sp.start_playback()
        #playlist = self.sp.current_user_playlists()
        #print(playlist)
           

    def play(self):
        user_playlists = self.sp.current_user_playlists()
        self.start_playback(user_playlists['items'][0]['uri'])

    def currently_playing(self, device_id:str = None):
        device_id = device_id if device_id else self.device_id
        device_info = self.get_device_status(self.device_id)
        if device_info and device_info['is_active']:
            return self.sp.current_user_playing_track()
        return None

    def pause_playback(self, device_id:str=None ):
        device_id = device_id if device_id else self.device_id
        device_info = self.get_device_status(device_id)
        if device_info:
            if device_info['is_active']:
                self.sp.pause_playback(device_id=device_id)
        else:
            raise Exception('Device not available')    

    def get_device_status(self, device_id:str)->object:
        """Get device info from spotify

        Args:
            device_id (str): device id

        Returns:
            object: device object
        """        
        devices = self.sp.devices()['devices']
        devices = [ d for d in devices if d['id'] == device_id]
        if len(devices)>0:
            return devices[0]
        else:
            return None

    def start_playback(self, context_uri:str=None, device_id:str = None ):
        """[summary]

        Args:
            uri (str): Context URI to play ( playlist, artist, etc)
            device_id (str, optional): device id to start playback. Defaults to None.

        Raises:
            Exception: Device not available
        """         
        device_id = device_id if device_id else self.device_id
        device_info = self.get_device_status(device_id)
        if device_info:
            if not device_info['is_active']:
                self.sp.transfer_playback(device_id)    
            self.sp.start_playback(context_uri=context_uri, device_id=device_id)
        else:
            raise Exception('Device not available')    
        
    def get_auth(self)->object:
        """Get Spotify OAuth object

        Returns:
            object: Spotify OAuth obejct
        """        
        return self.auth

    def get_new_access_token(self):
        auth_code = self.auth.get_authorization_code()
        self.auth.get_access_token(auth_code)
        
           

#config = configparser.ConfigParser()
#config.read("config/settings.ini")
#os.environ['SPOTIPY_CLIENT_ID'] = config['CREDENTIALS']['CLIENT_ID']
#os.environ['SPOTIPY_CLIENT_SECRET'] = config['CREDENTIALS']['CLIENT_SECRET']
#os.environ['SPOTIPY_REDIRECT_URI'] = config['CREDENTIALS']['REDIRECT_URI']
#ctrl = Controller(config)