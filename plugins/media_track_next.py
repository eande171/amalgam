from src.plugin import Plugin
from src.speech_recognition.stt_tts import Output

class Plugin(Plugin):
    def startup(self):
        pass

    def execute(self):
        import pyautogui
        pyautogui.press("nexttrack")

    def shutdown(self):
        Output.tts("Skipped to the next track.")

    def get_identifier(self):
        return "media_track_next"

    def register_commands(self):
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

    def get_description(self):
        return "This plugin skips this media (audio/video) using the system's media controls."