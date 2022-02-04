from dbus_next.service import ServiceInterface, method, dbus_property, signal, Variant
from dbus_next.aio import MessageBus
from mycroft_bus_client import MessageBusClient, Message
from time import sleep
import asyncio

class MprisBusClient():
    
    def __init__(self):
        self.bus = MessageBusClient()
        self.bus.run_in_thread()
        
    def client(self):
        return self.bus

class MediaPlayer2Interface(ServiceInterface):
    def __init__(self, name, mycroftBus=None):
        super().__init__(name)
        self.bus = mycroftBus
        self._identity = "Mycroft Mpris Service"
        self._desktopEntry = "Mycroft"
        self._supportedMimeTypes = ["audio/mpeg", "audio/x-mpeg", "video/mpeg", "video/x-mpeg", "video/mpeg-system", "video/x-mpeg-system", "video/mp4", "audio/mp4", "video/x-msvideo", "video/quicktime", "application/ogg", "application/x-ogg", "video/x-ms-asf", "video/x-ms-asf-plugin", "application/x-mplayer2", "video/x-ms-wmv", "video/x-google-vlc-plugin", "audio/wav", "audio/x-wav", "audio/3gpp", "video/3gpp", "audio/3gpp2", "video/3gpp2", "video/divx", "video/flv", "video/x-flv", "video/x-matroska", "audio/x-matroska", "application/xspf+xml"]
        self._supoortedUriSchemes = ["file", "http", "https", "rtsp", "realrtsp", "pnm", "ftp", "mtp", "smb", "mms", "mmsu", "mmst", "mmsh", "unsv", "itpc", "icyx", "rtmp", "rtp", "dccp", "dvd", "vcd"]
        self._hasTrackList = False
        self._canQuit = True
        self._canSetFullscreen = True
        self._fullscreen = False
        self._canRaise = True
                
    @dbus_property()
    def Identity(self) -> 's':
        return self._identity
    
    @Identity.setter
    def Identity_setter(self, val: 's'):
        self._identity = val
                
    @dbus_property()
    def DesktopEntry(self) -> 's':
        return self._desktopEntry
    
    @DesktopEntry.setter
    def DesktopEntry_setter(self, val: 's'):
        self._desktopEntry = val
    
    @dbus_property()
    def SupportedMimeTypes(self) -> 'as':
        return self._supportedMimeTypes
    
    @SupportedMimeTypes.setter
    def SupportedMimeTypes_setter(self, val: 'as'):
        self._supportedMimeTypes = val
    
    @dbus_property()
    def SupportedUriSchemes(self) -> 'as':
        return self._supoortedUriSchemes
    
    @SupportedUriSchemes.setter
    def SupportedUriSchemes_setter(self, val: 'as'):
        self._supoortedUriSchemes = val
        
    @dbus_property()
    def HasTrackList(self) -> 'b':
        return self._hasTrackList
    
    @HasTrackList.setter
    def HasTrackList_setter(self, val: 'b'):
        self._hasTrackList = val
    
    @dbus_property()
    def CanQuit(self) -> 'b':
        return self._canQuit
    
    @CanQuit.setter
    def CanQuit_setter(self, val: 'b'):
        self._canQuit = val 
    
    @dbus_property()
    def CanSetFullscreen(self) -> 'b':
        return False
    
    @CanSetFullscreen.setter
    def CanSetFullscreen_setter(self, val: 'b'):
        self._CanSetFullscreen = val
    
    @dbus_property()
    def Fullscreen(self) -> 'b':
        return self._fullscreen
    
    @Fullscreen.setter
    def Fullscreen_setter(self, val: 'b'):
        self._fullscreen = val
    
    @dbus_property()
    def CanRaise(self) -> 'b':
        return self._canRaise
    
    @CanRaise.setter
    def CanRaise_setter(self, val: 'b'):
        self._canRaise = val
    
    @method()
    def Quit(self):
        self.bus.emit(Message("mpris.skill.interface.client.quit", {}))

    @method()
    def Raise(self):
        self.bus.emit(Message("mpris.skill.interface.client.raise", {}))
        
class MediaPlayer2PlayerInterface(ServiceInterface):
    def __init__(self, name, mycroftBus=None):
        super().__init__(name)
        self.bus = mycroftBus
        self._metadata = {}
        self._playbackStatus = "Stopped"
        self._loopStatus = "None"
        self._volume = 1.0
        self._shuffle = False
        self._position = 0
        self._rate = 1.0
        self._minimumRate = 1.0
        self._maximumRate = 1.0
        self._canControl = False
        self._canPlay = False
        self._canPause = False
        self._canSeek = False
        self._canGoNext = False
        self._canGoPrevious = False
        
        self.bus.on("mpris.skill.interface.server.request.metadata.response", self.on_metadata_response)
        self.bus.on("mpris.skill.interface.server.request.playbackstatus.response", self.on_playbackstatus_response)
        self.bus.on("mpris.skill.interface.server.request.loopstatus.response", self.on_loopstatus_response)
        self.bus.on("mpris.skill.interface.server.request.volume.response", self.on_volume_response)
        self.bus.on("mpris.skill.interface.server.request.shuffle.response", self.on_shuffle_response)
        self.bus.on("mpris.skill.interface.server.request.position.response", self.on_position_response)
        self.bus.on("mpris.skill.interface.server.request.rate.response", self.on_rate_response)
        self.bus.on("mpris.skill.interface.server.request.minimumrate.response", self.on_minimumrate_response)
        self.bus.on("mpris.skill.interface.server.request.maximumrate.response", self.on_maximumrate_response)
        self.bus.on("mpris.skill.interface.server.request.cancontrol.response", self.on_cancontrol_response)
        self.bus.on("mpris.skill.interface.server.request.canplay.response", self.on_canplay_response)
        self.bus.on("mpris.skill.interface.server.request.canpause.response", self.on_canpause_response)
        self.bus.on("mpris.skill.interface.server.request.canseek.response", self.on_canseek_response)
        self.bus.on("mpris.skill.interface.server.request.cangoforward.response", self.on_cangoforward_response)
        self.bus.on("mpris.skill.interface.server.request.cangobackward.response", self.on_cangobackward_response)
        self.bus.on("mpris.skill.interface.client.set.play", self.on_play)
        self.bus.on("mpris.skill.interface.client.set.pause", self.on_pause)
        self.bus.on("mpris.skill.interface.client.set.stop", self.on_stop)
        self.bus.on("mpris.skill.interface.client.set.next", self.on_next)
        self.bus.on("mpris.skill.interface.client.set.previous", self.on_previous)
        
    def on_metadata_response(self, message):
        self.metadata = {}
    
    def on_playbackstatus_response(self, message):
        self._playbackStatus = message.data["playbackStatus"]
    
    def on_loopstatus_response(self, message):
        self._loopStatus = message.data["loopStatus"]
        
    def on_volume_response(self, message):
        self._volume = message.data["volume"]
        
    def on_shuffle_response(self, message):
        self._shuffle = message.data["shuffle"]
    
    def on_position_response(self, message):
        self._position = message.data["position"]
        
    def on_rate_response(self, message):
        self._rate = message.data["rate"]
        
    def on_minimumrate_response(self, message):
        self._minimumRate = message.data["minimumRate"]
        
    def on_maximumrate_response(self, message):
        self._maximumRate = message.data["maximumRate"]
        
    def on_cancontrol_response(self, message):
        self._canControl = message.data["canControl"]
        self.emit_properties_changed({"CanControl": self._canControl})
        
    def on_canplay_response(self, message):
        self._canPlay = message.data["canPlay"]
        self.emit_properties_changed({"CanPlay": self._canPlay})
        
    def on_canpause_response(self, message):
        self._canPause = message.data["canPause"]
        self.emit_properties_changed({"CanPause": self._canPause})
        
    def on_canseek_response(self, message):
        self._canSeek = message.data["canSeek"]
        self.emit_properties_changed({"CanSeek": self._canSeek})
        
    def on_cangoforward_response(self, message):
        self._canGoNext = message.data["canGoNext"]
        self.emit_properties_changed({"CanGoNext": self._canGoNext})
        
    def on_cangobackward_response(self, message):
        self._canGoPrevious = message.data["canGoPrevious"]
        self.emit_properties_changed({"CanGoPrevious": self._canGoPrevious})
    
    def on_play(self, message):
        self._playbackStatus = "Playing"
        self._canControl = True
        self._canPause = True
        self._canPlay = False
        self._canSeek = True
        self._canGoNext = True
        self._canGoPrevious = True
        
        self.emit_properties_changed({"PlaybackStatus": self._playbackStatus, "CanControl": self._canControl, "CanPause": self._canPause, "CanPlay": self._canPlay, "CanSeek": self._canSeek, "CanGoNext": self._canGoNext, "CanGoPrevious": self._canGoPrevious})

        
    def on_pause(self, message):
        self._playbackStatus = "Paused"
        self._canControl = True
        self._canPause = False
        self._canPlay = True
        self._canSeek = True
        self._canGoNext = True
        self._canGoPrevious = True
        
        self.emit_properties_changed({"PlaybackStatus": self._playbackStatus, "CanControl": self._canControl, "CanPause": self._canPause, "CanPlay": self._canPlay, "CanSeek": self._canSeek, "CanGoNext": self._canGoNext, "CanGoPrevious": self._canGoPrevious})

        
    def on_stop(self, message):
        self._playbackStatus = "Stopped"
        self._canControl = True
        self._canPause = False
        self._canPlay = True
        self._canSeek = True
        self._canGoNext = True
        self._canGoPrevious = True

        self.emit_properties_changed({"PlaybackStatus": self._playbackStatus, "CanControl": self._canControl, "CanPause": self._canPause, "CanPlay": self._canPlay, "CanSeek": self._canSeek, "CanGoNext": self._canGoNext, "CanGoPrevious": self._canGoPrevious})

    def on_next(self, message):
        self.bus.emit(Message("mpris.skill.interface.server.request.metadata", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.playbackstatus", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.cancontrol", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.canplay", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.canpause", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.canseek", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.cangoforward", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.cangobackward", {}))
        
    def on_previous(self, message):
        self.bus.emit(Message("mpris.skill.interface.server.request.metadata", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.playbackstatus", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.cancontrol", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.canplay", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.canpause", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.canseek", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.cangoforward", {}))
        self.bus.emit(Message("mpris.skill.interface.server.request.cangobackward", {}))
       
    @dbus_property()
    def Metadata(self) -> 'a{sv}':
        self.bus.emit(Message("mpris.skill.interface.server.request.metadata", {}))
        return self._metadata
    
    @Metadata.setter
    def Metadata_setter(self, val: 'a{sv}'):
        self._metadata = val
    
    @dbus_property()
    def PlaybackStatus(self) -> 's':
        return self._playbackStatus
    
    @PlaybackStatus.setter
    def PlaybackStatus_setter(self, val: 's'):
        self._playbackStatus = val
    
    @dbus_property()
    def LoopStatus(self) -> 's':
        return self._loopStatus
    
    @LoopStatus.setter
    def LoopStatus_setter(self, val: 's'):
        self._loopStatus = val
    
    @dbus_property()
    def Volume(self) -> 'd':
        return self._volume
    
    @Volume.setter
    def Volume_setter(self, val: 'd'):
        self._volume = val
    
    @dbus_property()
    def Shuffle(self) -> 'b':
        return self._shuffle
    
    @Shuffle.setter
    def Shuffle_setter(self, val: 'b'):
        self._shuffle = val
        
    @dbus_property()
    def Position(self) -> 'x':
        return self._position
    
    @Position.setter
    def Position_setter(self, val: 'x'):
        self._position = val
    
    @dbus_property()
    def Rate(self) -> 'd':
        return self._rate
    
    @Rate.setter
    def Rate_setter(self, val: 'd'):
        self._rate = val
        
    @dbus_property()
    def MinimumRate(self) -> 'd':
        return self._minimumRate
    
    @MinimumRate.setter
    def MinimumRate_setter(self, val: 'd'):
        self._minimumRate = val
        
    @dbus_property()
    def MaximumRate(self) -> 'd':
        return self._maximumRate
    
    @MaximumRate.setter
    def MaximumRate_setter(self, val: 'd'):
        self._maximumRate = val
    
    @dbus_property()
    def CanControl(self) -> 'b':
        return self._canControl
    
    @CanControl.setter
    def CanControl_setter(self, val: 'b'):
        self._canControl = val
    
    @dbus_property()
    def CanPlay(self) -> 'b':
        return self._canPlay
    
    @CanPlay.setter
    def CanPlay_setter(self, val: 'b'):
        self._canPlay = val
        
    @dbus_property()
    def CanPause(self) -> 'b':
        return self._canPause
    
    @CanPause.setter
    def CanPause_setter(self, val: 'b'):
        self._canPause = val
    
    @dbus_property()
    def CanSeek(self) -> 'b':
        return self._canSeek
    
    @CanSeek.setter
    def CanSeek_setter(self, val: 'b'):
        self._canSeek = val
        
    @dbus_property()
    def CanGoNext(self) -> 'b':
        return self._canGoNext
    
    @CanGoNext.setter
    def CanGoNext_setter(self, val: 'b'):
        self._canGoNext = val
    
    @dbus_property()
    def CanGoPrevious(self) -> 'b':
        return self._canGoPrevious
    
    @CanGoPrevious.setter
    def CanGoPrevious_setter(self, val: 'b'):
        self._canGoPrevious = val
        
    @method()
    def Previous(self):
        print("Previous")
    
    @method()
    def Next(self):
        print("Next")
    
    @method()
    def Stop(self):
        self.bus.emit(Message("mpris.skill.interface.server.request.stop", {}))
    
    @method()
    def Play(self):
        self.bus.emit(Message("mpris.skill.interface.server.request.play", {}))
        
    @method()
    def Pause(self):
        self.bus.emit(Message("mpris.skill.interface.server.request.pause", {}))
    
    @method()
    def PlayPause(self):
        if self._playbackStatus == "Playing":
            self.bus.emit(Message("mpris.skill.interface.server.request.pause", {}))
        else:
            self.bus.emit(Message("mpris.skill.interface.server.request.play", {}))
    
    @method()
    def Seek(self, argument: 'd') -> 'd':
        return self._position
    
    @method()
    def OpenUri(self, argument: 's'):
        print("OpenUri")
    
async def main():
    mycroftBusClient = MprisBusClient()
    bus = await MessageBus().connect()
    mediaPlayer2Interface = MediaPlayer2Interface('org.mpris.MediaPlayer2', mycroftBus=mycroftBusClient.client())
    mediaPlayer2PlayerInterface = MediaPlayer2PlayerInterface('org.mpris.MediaPlayer2.Player', mycroftBus=mycroftBusClient.client())
    bus.export('/org/mpris/MediaPlayer2', mediaPlayer2Interface)
    bus.export('/org/mpris/MediaPlayer2', mediaPlayer2PlayerInterface)
    await bus.request_name('org.mpris.MediaPlayer2.mycroft')
    await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
