# AutoCommitMessage

<div align="center">

**Stop writing commit messages. Let a local LLM do it.**

AutoCommitMessage inspects your staged git diff and generates a concise, relevant commit message using a locally-hosted [Ollama](https://ollama.com/) model — no API keys, no cloud calls, no data leaving your machine.

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/powered%20by-Ollama-black)](https://ollama.com/)
[![License](https://img.shields.io/badge/license-unspecified-lightgrey)](#)

</div>

---

## ✨ Features

- 🧠 **Local-first** — runs entirely against your own Ollama instance, nothing is sent to a third party
- ⚡ **One command** — stage your changes, run `acm`, done
- 🛠️ **Configurable** — swap the model or tune the system prompt via a simple YAML file

## 🚀 Quick Start

```bash
curl -fsSL https://storage.sten-heimbrodt.de/acm-install.sh | sh
```

That's it — the script takes care of dependencies and installation for you.

## 🔧 Manual Installation

<details>
<summary>Click to expand step-by-step instructions</summary>

**1. Install Ollama**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**2. Pull the default model**

```bash
ollama pull ministral-3:3b
```

**3. Install [uv](https://docs.astral.sh/uv/)** (if you don't already have it)

**4. Install AutoCommitMessage**

```bash
uv tool install .
```

</details>

## 📦 Usage

1. Stage the changes you want to commit:

   ```bash
   git add .
   ```

2. Run:

   ```bash
   acm
   ```

AutoCommitMessage will read your staged diff, send it to your local model, and commit the result automatically with the generated message.

### Custom configuration

Point AutoCommitMessage at an alternative config file with `--config`:

```bash
acm --config /path/to/my-config.yaml
```

A config file looks like this:

```yaml
model: "ministral-3:3b"
system_prompt: >
  You generate concise and short git commit messages based on the provided
  diff content. Only provide the commit message without any additional text
  or explanations.
```

| Key | Description |
| --- | --- |
| `model` | Name of the Ollama model to use for generation (must be pulled locally) |
| `system_prompt` | Instructions given to the model that shape the style of the generated commit message |

Swap in any Ollama-compatible model — larger models tend to produce more nuanced messages at the cost of speed.

## 🩺 Requirements

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running locally
- Staged changes in a git repository (`git add` before running `acm`)

## ⚙️ How it works

1. `acm` reads its configuration (model + system prompt)
2. It exports your staged changes with `git diff --staged`
3. The diff is sent to the configured local model as the user message, alongside the system prompt
4. The model's response becomes your commit message
5. AutoCommitMessage commits the change and cleans up its temporary files

---

<div align="center">
Made for developers who'd rather write code than commit messages.
</div>
