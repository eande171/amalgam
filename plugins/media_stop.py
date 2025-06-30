from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class Plugin(Plugin):
    def startup(self):
        pass

    def execute(self):
        import pyautogui
        pyautogui.press("stop")

    def shutdown(self):
        Output.tts("Media playback stopped.")

    def get_identifier(self):
        return "media_stop"

    def register_commands(self):
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

    def get_description(self):
        return "This plugin stops this media (audio/video) using the system's media controls."