import logging

import lmstudio as lms
from src.config import Config
import subprocess

logger = logging.getLogger(__name__)

def lm_server_handler(func):
    def wrapper(*args, **kwargs):
        if not Config.get_data("ai_enabled"):
            logger.info("LLM Usage has been disabled.")
            return

        LLM._start_server()
        result = func(*args, **kwargs)
        LLM._stop_server()
        return result

    return wrapper

class LLM():
    ai_data = Config.get_data("ai_config")
    local_address = "localhost:" + ai_data["port"]

    @staticmethod
    def _silent_run(command, shell=False):
        """
        Runs a command, hiding output unless an error occurs.

        Args:
            command (list or str): The command to run.
                                    If shell=True, this should be a string.
                                    If shell=False, this should be a list of strings.
            shell (bool): Whether to execute the command through the shell.
        """
        try: 
            result = subprocess.run(
                command, 
                capture_output=True,  # Capture stdout and stderr
                text=True,            # Decode stdout and stderr as text
                check=False,          # Do not raise CalledProcessError
                shell=shell           # Whether to use the shell
            )

            if result.returncode != 0:
                logger.error(f"Error executing command: {' '.join(command) if isinstance(command, list) else command}")
                logger.error(f"Standard Output:\n{result.stdout}")
                logger.error(f"Standard Error:\n{result.stderr}")
        except FileNotFoundError:
            print(f"Error: Command not found: {' '.join(command) if isinstance(command, list) else command}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def _start_server():
        logger.debug("Starting LMS Server...")
        LLM._silent_run(["lms", "server", "start", "--port", LLM.ai_data["port"]])

    @staticmethod
    def _stop_server():
        logger.debug("Stopping LMS Server...")
        LLM._silent_run(["lms", "server", "stop"])

    @staticmethod
    @lm_server_handler
    def query(query, format = None) -> str:
        with lms.Client(LLM.local_address) as client:
            model = client.llm.model(LLM.ai_data["model"])
            return model.respond(query, response_format=format)