from src.main import LLM_TOOL_DIR, idenfify_wakeword
from src.llm import LLM
from src.plugin import Plugin, PluginController
from src.speech_recognition.stt_tts import Input, Output
from src.config import Config

def run_plugin_queue(queue):
    for plugin in queue:
        PluginController.set_active_plugin(plugin)
        PluginController.active_startup()
        PluginController.active_execute()
        PluginController.active_shutdown()

using_ai = False

class Stop(Plugin):
    def startup(self):
        pass

    def execute(self):
        print("Stopping amalgam...")
        Output.tts("Amalgam is shutting down.")

    def shutdown(self):
        import sys
        sys.exit(0)

    def get_identifier(self):
        return "stop_self"

    def register_commands(self):
        return [
            "Stop amalgam.",
            "Terminate amalgam.",
            "Halt amalgam.",
            "End amalgam.",
            "Power off amalgam.",
            "Shut down amalgam.",
            "Stop yourself.",
            "Shut yourself down.",
            "Stop running"
        ]

    def get_description(self):
        return "This plugin stops the amalgam program when triggered"
    
class UseAI(Plugin):
    def startup(self):
        global using_ai
        using_ai = True
    
    def execute(self):
        global using_ai
        while using_ai:
            try:
                if idenfify_wakeword() or Config.get_data("deafened"):
                    text = Input.sst().lower()
                    if text:
                        LLM.query_with_tools("For the following input, think about what plugin identifier do I need for each command? Then please add the plugin to the queue. Think step by step. Input: " + text, LLM.get_tools(LLM_TOOL_DIR))

                        from llm_data.tools.plugins import plugin_queue

                        print(plugin_queue)
                        run_plugin_queue(plugin_queue)

                        plugin_queue.clear()
                    else:
                        Output.tts("No search query provided.", Output.YELLOW)
            except KeyboardInterrupt:
                Output.tts("Stopping LLM Usage.")
                break

        PluginController.set_active_plugin("use_ai")
    
    def shutdown(self):
        global using_ai
        using_ai = False
    
    def get_identifier(self):
        return "use_ai"
    
    def register_commands(self):
        return [
            "I'd like to use AI.",
            "Start AI mode.",
            "Enable AI for plugins.",
            "Can you enable AI for me?",
            "Please switch to AI-powered plugin execution.",
            "Let's use AI for running plugins.",
            "Turn on AI capabilities."
        ]
    
    def get_description(self):
        return "This plugin will force amalgam to use AI (LLM + tools) to run the plugins from now on."
    
class RetireAI(Plugin):
    def startup(self):
        pass
    
    def execute(self):
        global using_ai
        if using_ai:
            Output.tts("Disabling AI...")
            using_ai = False
        else:
            Output.tts("AI is not active.")
            
    def shutdown(self):
        pass
    
    def get_identifier(self):
        return "retire_ai"
    
    def register_commands(self):
        return [
            "I'd like to stop using AI.",
            "Disable AI mode.",
            "Turn off AI for plugins.",
            "Can you disable AI for me?",
            "Please switch off AI-powered plugin execution.",
            "Let's stop using AI for running plugins.",
            "Turn off AI capabilities."
        ]
    
    def get_description(self):
        return "This plugin will stop amalgam from using AI (LLM + tools) to run the plugins from now on."
