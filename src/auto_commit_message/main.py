# AutoCommitMessage
import logging
import argparse
import os
import subprocess
import colorama
from ollama import chat, ChatResponse

class AutoCommitMessage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def generate_commit_message(self):
        if not os.path.exists("changes.diff"):
            self.logger.error("No changes.diff file found. Do you have the files staged for commit?")
            return None

        with open("changes.diff", "r") as diff_file:
            diff_content = diff_file.read()
            response: ChatResponse = chat(model='gemma4:e2b', messages=[
                {
                    'role': 'user',
                    'content': 'Create a concise and short git commit message based on the following diff:\n\n' + diff_content + '\n\nPlease provide only the commit message without any additional text.',
                },
            ])
            self.logger.debug(f"Generated commit message: {colorama.Fore.GREEN}{response['message']['content']}{colorama.Style.RESET_ALL}")
            return response['message']['content']


    def create_git_diff_file(self):
        subprocess.run(["git", "diff", "--staged"], stdout=open("changes.diff", "w"))

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

    argument_parser.parse_args()

    auto_commit_message = AutoCommitMessage()

    auto_commit_message.create_git_diff_file()
    commit_message = auto_commit_message.generate_commit_message()
    auto_commit_message.commit_commit_message(commit_message)
    auto_commit_message.cleanup()


if __name__ == "__main__":
    main()
