from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class Plugin(Plugin):
    def startup(self):
        pass

    def execute(self):
        import pyautogui
        Output.tts("Media playback toggled.")
        pyautogui.press("playpause")

    def shutdown(self):
        pass
    
    def get_identifier(self):
        return "media_play_pause"

    def register_commands(self):
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

    def get_description(self):
        return "This plugin plays/pauses media (audio/video) using the system's media controls."