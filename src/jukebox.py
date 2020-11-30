from statemachine import StateMachine, State

class JukeBox(StateMachine):
    controller = None
    next_uri = None
    config = None
    # States
    idle = State('Idle', initial=True)
    playback = State('Playback')
    load = State('Load')
           
    # Trasitions
    pause = playback.to(idle)
    play  = idle.to(playback) | load.to(playback)
    set_playlist  = playback.to(load) | idle.to(load)
    play_pause =  play | pause
    next_track =  playback.to.itself()
      
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super(JukeBox, self).__init__()
        if self.controller == None:
            raise Exception("Controller must be passed on initialization")
        self.sync_state()
    
    def sync_state(self):
        currently_playing = self.controller.currently_playing()
        if currently_playing and currently_playing[u'is_playing']:
            self.play()
    # On Actions
    def on_pause(self):
        print('Action: Pause')
        
    def on_play_pause(self):
        print('Action: Play-Pause')
    def on

    def on_set_playlist(self, new_uri):
        self.next_uri = new_uri
        print('Set New Playlist:{}'.format(new_uri))

    def on_play(self):
        print('on_play')
    
    #State Behavior

    def on_enter_load(self):
        print('Enter:Load')
        self.play()
               
    def on_enter_idle(self):
        print('Enter: Idle state')
        self.controller.pause_playback()
    
    def on_enter_playback(self):
        print('Enter: Playback state')
        if self.next_uri:
            self.controller.start_playback(self.next_uri)
            self.next_uri = None
        else:
            self.controller.start_playback()
        currently_playing = self.controller.currently_playing()
        print(currently_playing['item']['name'])
