# YouTube Summary

A command-line tool to extract transcripts from YouTube videos and summarize them using various LLM providers.

## Quick Start

For those who want to get started immediately:

```bash
# Clone the repository
git clone https://github.com/dawsonlp/youtube-summary.git
cd youtube-summary

# Install Python 3.10+ if you don't have it already
# On macOS: brew install python@3.10
# On Ubuntu: sudo apt install python3.10
# On Windows: Download from https://www.python.org/downloads/

# Install Poetry (dependency manager)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Create configuration file (uses default Ollama settings)
cp .env.example .env

# Summarize a YouTube video
poetry run youtube-summary summarize "https://www.youtube.com/watch?v=TdAAUoJ065o"
```

That's it! You'll get a summary of the video transcript in your terminal.

## Features

- Extract transcripts from any YouTube video
- Support for multiple languages
- Summarize transcripts using different LLM providers:
  - Local Ollama models (default)
  - OpenAI API (optional)
  - Anthropic API (optional)
- Flexible configuration using environment variables
- Simple CLI interface

## Installation

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)
- Ollama (for local LLM, optional if using cloud providers)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/dawsonlp/youtube-summary.git
   cd youtube-summary
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file to configure your preferred LLM provider

## Usage

The tool can be used in two ways:

### 1. Poetry Run

```bash
# Get a summary
poetry run youtube-summary summarize "https://www.youtube.com/watch?v=TdAAUoJ065o"

# Get just the transcript
poetry run youtube-summary transcript "https://www.youtube.com/watch?v=TdAAUoJ065o"

# Specify a different language
poetry run youtube-summary summarize "https://www.youtube.com/watch?v=TdAAUoJ065o" --languages="es,en"

# Save the summary to a file
poetry run youtube-summary summarize "https://www.youtube.com/watch?v=TdAAUoJ065o" --output-file="summary.txt"

# Specify a different LLM provider
poetry run youtube-summary summarize "https://www.youtube.com/watch?v=TdAAUoJ065o" --provider="openai"

# Specify a different model
poetry run youtube-summary summarize "https://www.youtube.com/watch?v=TdAAUoJ065o" --provider="ollama" --model="llama3.2:8b"

# Limit summary length
poetry run youtube-summary summarize "https://www.youtube.com/watch?v=TdAAUoJ065o" --max-length=200
```

### 2. Direct Python Import

```python
from youtube_summary.transcript import get_transcript_text
from youtube_summary.summarizer import summarize_text

# Get transcript
transcript = get_transcript_text("https://www.youtube.com/watch?v=TdAAUoJ065o")

# Summarize with default provider (Ollama)
summary = summarize_text(transcript)

# Summarize with a specific provider
summary = summarize_text(transcript, provider_name="openai", model_name="gpt-4")

print(summary)
```

## Configuration

The tool can be configured using environment variables in your `.env` file:

```
# LLM Provider Settings
SUMMARY_PROVIDER=ollama  # Options: 'ollama', 'openai', 'anthropic'

# Ollama Settings
OLLAMA_MODEL=llama3.2

# OpenAI Settings
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Anthropic Settings
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

## Project Structure

```
youtube-summary/
├── youtube_summary/
│   ├── __init__.py
│   ├── transcript.py    # Handles YouTube transcript extraction
│   ├── summarizer.py    # LLM provider implementations
│   └── cli.py           # Command-line interface
├── .env.example         # Example environment configuration
├── .gitignore           # Git ignore patterns
├── pyproject.toml       # Poetry project definition
└── README.md            # This file
```

## How It Works

1. The tool extracts video IDs from YouTube URLs
2. It uses the `youtube-transcript-api` to fetch the transcript
3. The transcript is sent to the configured LLM provider for summarization
4. The summary is returned to the user or saved to a file

## LLM Provider Details

### Ollama (Default)

Uses locally running Ollama models. No API key required, but you need to have Ollama installed and the specified model downloaded.

### OpenAI

Uses OpenAI's API for summarization. Requires an API key from OpenAI.

### Anthropic

Uses Anthropic's Claude models via their API. Requires an API key from Anthropic.
