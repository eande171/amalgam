from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class PlayPause(Plugin):
    def startup():
        pass

    def execute():
        import pyautogui
        Output.tts("Media playback toggled.")
        pyautogui.press("playpause")

    def shutdown():
        pass
    
    def get_identifier():
        return "media_play_pause"

    def register_commands():
        return [
            "Play media.",
            "Start media playback.",
            "Begin media playback.",
            "Launch media player.",
            "Open media file.",
            "Play audio.",
            "Start video playback.",
            "Begin audio playback.",
            "Start playing music.",
            "Play the music.",
            "Play me a song"
            "Play video.",
            "Toggle media playback.",
            "Toggle audio playback.",
            "Toggle video playback.",
            "Toggle music playback.",
            "Toggle play/pause.",
            "Toggle media controls.",
        ]

    def get_description():
        return "This plugin plays/pauses media (audio/video) using the system's media controls."

class Stop(Plugin):
    def startup():
        pass

    def execute():
        import pyautogui
        pyautogui.press("stop")

    def shutdown():
        Output.tts("Media playback stopped.")

    def get_identifier():
        return "media_stop"

    def register_commands():
        return [
            "Stop current media.",
            "Stop playback.",
            "Halt audio/video.",
            "End current track.",
            "Stop this media.",
            "Pause and stop media.",
            "Terminate current media.",
            "Stop playing audio/video.",
            "End playback of this media.",
            "Halt current audio/video.",
            "Pause current media.",
            "Pause the music."
        ]

    def get_description():
        return "This plugin stops this media (audio/video) using the system's media controls."

class NextTrack(Plugin):
    def startup():
        pass

    def execute():
        import pyautogui
        pyautogui.press("nexttrack")

    def shutdown():
        Output.tts("Skipped to the next track.")

    def get_identifier():
        return "media_track_next"

    def register_commands():
        return [
            "Skip to next track.",
            "Next song.",
            "Advance to next media.",
            "Move to next audio track.",
            "Go to next video.",
            "Next audio track.",
            "Next video track.",
            "Skip current media.",
            "Next media track.",
            "Advance to next song.",
            "Skip to next song.",
        ]

    def get_description():
        return "This plugin skips this media (audio/video) using the system's media controls."

class PrevTrack(Plugin):
    def startup():
        pass

    def execute():
        import pyautogui
        pyautogui.press("prevtrack")

    def shutdown():
        Output.tts("Skipped to the previous track.")

    def get_identifier():
        return "media_track_prev"

    def register_commands():
        return [
            "Skip to previous track.",
            "Previous song.",
            "Go back to previous media.",
            "Return to previous audio track.",
            "Go to previous video.",
            "Previous audio track.",
            "Previous video track.",
            "Skip current media back.",
            "Previous media track.",
            "Return to previous song.",
            "Skip to previous song.",
        ]

    def get_description():
        return "This plugin skips to the previous media (audio/video) using the system's media controls."

class VolumeUp(Plugin):
    def startup():
        pass

    def execute():
        import pyautogui
        pyautogui.press("volumeup")

    def shutdown():
        Output.tts("Volume increased.")

    def get_identifier():
        return "media_volume_up"

    def register_commands():
        return [
            "Increase volume.",
            "Raise volume level.",
            "Turn up the volume.",
            "Boost audio volume.",
            "Amplify sound output.",
            "Enhance audio level.",
            "Make it louder.",
            "Volume up.",
            "Increase sound volume.",
            "Raise audio level."
        ]

    def get_description():
        return "This plugin increases the volume using the system's media controls."
    
class VolumeDown(Plugin):
    def startup():
        pass

    def execute():
        import pyautogui
        pyautogui.press("volumedown")

    def shutdown():
        Output.tts("Volume decreased.")

    def get_identifier():
        return "media_volume_down"

    def register_commands():
        return [
            "Decrease volume.",
            "Lower volume level.",
            "Turn down the volume.",
            "Reduce audio volume.",
            "Diminish sound output.",
            "Lower audio level.",
            "Make it quieter.",
            "Volume down.",
            "Decrease sound volume.",
            "Lower audio level."
        ]

    def get_description():
        return "This plugin decreases the volume using the system's media controls."