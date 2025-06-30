from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class Plugin(Plugin):
    def startup(self):
        pass

    def execute(self):
        import pyautogui
        pyautogui.press("prevtrack")

    def shutdown(self):
        Output.tts("Skipped to the previous track.")

    def get_identifier(self):
        return "media_track_prev"

    def register_commands(self):
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

    def get_description(self):
        return "This plugin skips to the previous media (audio/video) using the system's media controls."