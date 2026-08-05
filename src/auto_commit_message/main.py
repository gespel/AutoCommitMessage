# AutoCommitMessage
import logging
import argparse
import os
from termcolor import colored
import yaml
import ollama
from ollama import chat, ChatResponse
from .acm import AutoCommitMessage

def main():
    argument_parser = argparse.ArgumentParser(description="Auto Commit Message Generator using a Ollama local model")
    argument_parser.add_argument("--config", type=str, help="Specify an alternative configuration file path")
    argument_parser.add_argument("--model", type=str, help="Specify the model to use for generating commit messages")
    argument_parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    argument_parser.add_argument("--show-config", action="store_true", help="Show the current configuration and exit")

    args = argument_parser.parse_args()

    if args.config:
        config_path = args.config
    else:
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    acm = AutoCommitMessage(model=args.model)
    if args.debug:
        acm.logger.setLevel(logging.DEBUG)
        acm.logger.debug("Debug logging enabled.")

    try:
        acm.logger.debug(f"Using configuration file: {config_path}")
        acm.read_config(config_path=config_path)
        acm.logger.debug(f"Configuration loaded: Model='{acm.model}', System Prompt='{acm.system_prompt[:50]}...'")

        if args.show_config:
            print(f"Current configuration:\n\nModel: {colored(acm.model, 'green')}\n\nSystem Prompt: {colored(acm.system_prompt, 'green')}")
            return

        acm.logger.debug("Getting git diff...")
        diff_text = acm.get_git_diff()
        acm.logger.debug(f"Git diff obtained: {colored(diff_text[:100], 'yellow')}...")

        commit_message = acm.generate_commit_message(diff_text=diff_text)

        acm.commit_commit_message(commit_message)

    except Exception as e:
        acm.logger.error(f"An error occurred: {e}")
    finally:
        acm.cleanup()


if __name__ == "__main__":
    main()
