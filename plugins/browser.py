from src.plugin import Plugin
from src.speech_recognition.stt_tts import Input, Output

class Search(Plugin):
    def startup():
        pass

    def execute():
        import pyautogui
        pyautogui.press("browsersearch")

        Output.tts("Opened browser search. What would you like to search for?", Output.GREEN)
        text = Input.sst()
        if text:
            pyautogui.write("Web: " + text)
            pyautogui.press("enter")
        else:
            Output.tts("No search query provided.", Output.YELLOW)


    def shutdown():
        Output.tts("Search completed", Output.GREEN)
        pass

    def get_identifier():
        return "browser_search"

    def register_commands():
        return [
            "Open browser search.",
            "Search the web.",
            "Launch browser search.",
            "Start browser search.",
            "Initiate web search.",
            "Open web search.",
            "Search online.",
            "Begin browser search.",
            "Activate browser search.",
            "Open internet search."
        ]

    def get_description():
        return "This plugin opens the browser search using the system"