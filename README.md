# AutoCommitMessage
Automatically generate concise git commit messages based on the changes in your code using a local Ollama model.

## Installation
In order to use AutoCommitMessage, you need to have [Ollama](https://ollama.com/) installed on your machine. You can install it using the following command:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Also, make sure you have uv installed. You can then install AutoCommitMessage using uv:

```bash
uv tool install .
```

## Usage
To generate a commit message, simply run the following command in your terminal:

```bash
acm
```

Make sure you have staged your changes before running the command. The tool will analyze the changes and generate a concise commit message for you.