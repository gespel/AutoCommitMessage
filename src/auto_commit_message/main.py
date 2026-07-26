# AutoCommitMessage
import logging
import argparse
import os
import subprocess
import colorama
import yaml
from ollama import chat, ChatResponse

class AutoCommitMessage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.model = None
        self.system_prompt = None

    def read_config(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        if not os.path.exists(config_path):
            self.logger.error(f"Configuration file not found at {config_path}. Please create a config.yaml file.")
            return None

        with open(config_path, 'r') as config_file:
            try:
                config = yaml.safe_load(config_file)
                self.model = config.get('model', self.model)
                self.system_prompt = config.get('system_prompt', self.system_prompt)
                return config
            except yaml.YAMLError as e:
                self.logger.error(f"Error reading configuration file: {e}")
                return None

    def generate_commit_message(self, diff_text=None):
        if diff_text is None:
            if not os.path.exists("changes.diff"):
                self.logger.error("No changes.diff file found. Do you have the files staged for commit?")
                return None
            with open("changes.diff", "r") as diff_file:
                diff_text = diff_file.read()

        if self.model is None or self.system_prompt is None:
            self.logger.error("Model or system prompt not set. Please check your configuration.")
            return None

        response: ChatResponse = chat(model=self.model, messages=[
            {
                'role': 'system',
                'content': self.system_prompt,
                },
                {
                    'role': 'user',
                    'content': diff_text,
                },
            ])
        self.logger.debug(f"Generated commit message: {colorama.Fore.GREEN}{response['message']['content']}{colorama.Style.RESET_ALL}")
        return response['message']['content']


    def create_git_diff_file(self):
        subprocess.run(["git", "diff", "--staged"], stdout=open("changes.diff", "w"))

    def get_git_diff(self):
        diff = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
        return diff.stdout

    def cleanup(self):
        if os.path.exists("changes.diff"):
            os.remove("changes.diff")
            self.logger.debug("Cleaned up changes.diff file.")

    def commit_commit_message(self, commit_message):
        if commit_message:
            subprocess.run(["git", "commit", "-m", commit_message])
            self.logger.debug(f"Committed changes with message: {colorama.Fore.GREEN}{commit_message}{colorama.Style.RESET_ALL}")
        else:
            self.logger.error("No commit message generated. Commit aborted.")


def main():
    argument_parser = argparse.ArgumentParser(description="Auto Commit Message Generator using a Ollama local model")
    argument_parser.add_argument("--config", type=str, help="Specify an alternative configuration file path")

    args = argument_parser.parse_args()

    if args.config:
        config_path = args.config
    else:
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    acm = AutoCommitMessage()
    try:
        acm.read_config(config_path)

        diff_text = acm.get_git_diff()
        commit_message = acm.generate_commit_message(diff_text=diff_text)
        acm.commit_commit_message(commit_message)
    finally:
        acm.cleanup()


if __name__ == "__main__":
    main()
