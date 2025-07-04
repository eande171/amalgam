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
            "Start playing music.",
            "Play the music.",
            "Play me a song.",
            "Play me some music.",
            "Play video.",
            "Toggle media playback.",
            "Resume the song.",
            "Let's play.",
            "Hit play.",
            "Begin playing.",
            "Can you play the media?",
            "Please start playback.",
            "I want to hear the music.",
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
            "Pause the music.",
            "Stop the music.",
            "Stop the video.",
            "End the song.",
            "Cease playback.",
            "Kill the music.",
            "Shut off the media.",
            "Stop the audio.",
            "Stop the video playing.",
            "Can you stop the current media?",
            "Please stop playback.",
            "I want the music to stop.",
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
            "Go to the next track.",
            "Play the next song.",
            "Forward to the next song.",
            "Skip ahead.",
            "Can you go to the next song?",
            "Please play the one after.",
            "I want to hear the next track.",
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
            "Go back one track.",
            "Play the previous song.",
            "Back to the last song.",
            "Rewind to the start of the track.",
            "Can you go to the previous song?",
            "Please play the one before.",
            "I want to hear the last track again.",
            "Let's listen to the previous one.",
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
            "Raise audio level.",
            "Raise the volume.",
            "Turn the volume up.",
            "Louden the sound.",
            "Make it more loud.",
            "Boost the sound.",
            "I need the volume to go up.",
            "Volume, please go up.",
            "Loudness up.",
            "Raise the output sound.",
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
            "Lower audio level.",
            "Lower the volume.",
            "Turn the volume down.",
            "Quiet down.",
            "Make it less loud.",
            "Soften the sound.",
            "It's too loud, decrease the volume.",
            "Make it a bit quieter.",
            "Could you reduce the sound?",
        ]

    def get_description():
        return "This plugin decreases the volume using the system's media controls."