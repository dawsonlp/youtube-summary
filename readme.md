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

## Extensions

### Creating an MCP Server

You can convert this tool into a Model Context Protocol (MCP) server that can be used with AI assistants like Claude:

1. **Install the MCP SDK**:
   ```bash
   poetry add @modelcontextprotocol/sdk
   ```

2. **Create an MCP server implementation**:
   ```bash
   mkdir -p mcp_server
   touch mcp_server/__init__.py
   ```

3. **Implement the MCP server**:
   Create a file `mcp_server/server.py` with the following structure:

   ```python
   #!/usr/bin/env python3
   from modelcontextprotocol.sdk.server import Server
   from modelcontextprotocol.sdk.server.stdio import StdioServerTransport
   from modelcontextprotocol.sdk.types import (
       CallToolRequestSchema,
       ErrorCode,
       ListToolsRequestSchema,
       McpError,
   )
   from youtube_summary.transcript import get_transcript_text
   from youtube_summary.summarizer import summarize_text

   class YouTubeSummaryServer:
       def __init__(self):
           self.server = Server(
               {
                   "name": "youtube-summary-server",
                   "version": "0.1.0",
               },
               {
                   "capabilities": {
                       "tools": {},
                   },
               }
           )
           
           self.setup_tool_handlers()
           
           # Error handling
           self.server.onerror = (error) => console.error('[MCP Error]', error)
           
       def setup_tool_handlers(self):
           self.server.setRequestHandler(ListToolsRequestSchema, async () => ({
               tools: [
                   {
                       name: 'get_transcript',
                       description: 'Get the transcript from a YouTube video',
                       inputSchema: {
                           type: 'object',
                           properties: {
                               url: {
                                   type: 'string',
                                   description: 'YouTube video URL or ID',
                               },
                               languages: {
                                   type: 'array',
                                   items: {
                                       type: 'string',
                                   },
                                   description: 'List of language codes to try',
                               },
                           },
                           required: ['url'],
                       },
                   },
                   {
                       name: 'summarize_video',
                       description: 'Get a summary of a YouTube video transcript',
                       inputSchema: {
                           type: 'object',
                           properties: {
                               url: {
                                   type: 'string',
                                   description: 'YouTube video URL or ID',
                               },
                               languages: {
                                   type: 'array',
                                   items: {
                                       type: 'string',
                                   },
                                   description: 'List of language codes to try',
                               },
                               max_length: {
                                   type: 'number',
                                   description: 'Maximum length of the summary in words',
                               },
                               provider: {
                                   type: 'string',
                                   description: 'LLM provider to use (ollama, openai, anthropic)',
                               },
                               model: {
                                   type: 'string',
                                   description: 'Model name to use with the provider',
                               },
                           },
                           required: ['url'],
                       },
                   },
               ],
           }))
           
           self.server.setRequestHandler(CallToolRequestSchema, async (request) => {
               if request.params.name == 'get_transcript':
                   try:
                       url = request.params.arguments.url
                       languages = request.params.arguments.languages or ['en']
                       
                       transcript = get_transcript_text(url, languages=languages)
                       
                       return {
                           content: [
                               {
                                   type: 'text',
                                   text: transcript,
                               },
                           ],
                       }
                   except Exception as e:
                       return {
                           content: [
                               {
                                   type: 'text',
                                   text: f"Error getting transcript: {str(e)}",
                               },
                           ],
                           isError: True,
                       }
               elif request.params.name == 'summarize_video':
                   try:
                       url = request.params.arguments.url
                       languages = request.params.arguments.languages or ['en']
                       max_length = request.params.arguments.max_length
                       provider = request.params.arguments.provider
                       model = request.params.arguments.model
                       
                       transcript = get_transcript_text(url, languages=languages)
                       
                       kwargs = {}
                       if provider:
                           kwargs['provider_name'] = provider
                       if model:
                           kwargs['model_name'] = model
                           
                       summary = summarize_text(transcript, max_length=max_length, **kwargs)
                       
                       return {
                           content: [
                               {
                                   type: 'text',
                                   text: summary,
                               },
                           ],
                       }
                   except Exception as e:
                       return {
                           content: [
                               {
                                   type: 'text',
                                   text: f"Error summarizing video: {str(e)}",
                               },
                           ],
                           isError: True,
                       }
               else:
                   throw new McpError(
                       ErrorCode.MethodNotFound,
                       `Unknown tool: ${request.params.name}`
                   )
           })
       
       async def run(self):
           transport = StdioServerTransport()
           await self.server.connect(transport)
           print("YouTube Summary MCP server running on stdio", file=sys.stderr)

   if __name__ == "__main__":
       server = YouTubeSummaryServer()
       server.run().catch(print)
   ```

4. **Make the server executable**:
   ```bash
   chmod +x mcp_server/server.py
   ```

5. **Add to your MCP configuration**:
   Add the server to your MCP configuration file, typically located at:
   - VSCode: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - Claude desktop app: `~/Library/Application Support/Claude/claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "youtube-summary": {
         "command": "python",
         "args": ["/path/to/youtube-summary/mcp_server/server.py"],
         "env": {
           "SUMMARY_PROVIDER": "ollama",
           "OLLAMA_MODEL": "llama3.2"
         },
         "disabled": false,
         "autoApprove": []
       }
     }
   }
   ```

6. **Restart your AI assistant application** to load the new MCP server.

### Creating a Firefox Browser Extension

You can create a Firefox browser extension that lets users summarize YouTube videos directly from their browser:

1. **Create the extension structure**:
   ```bash
   mkdir -p firefox-extension/icons
   touch firefox-extension/manifest.json
   touch firefox-extension/background.js
   touch firefox-extension/popup.html
   touch firefox-extension/popup.js
   touch firefox-extension/content.js
   ```

2. **Create a manifest file** (`firefox-extension/manifest.json`):
   ```json
   {
     "manifest_version": 2,
     "name": "YouTube Summary",
     "version": "1.0",
     "description": "Summarize YouTube video transcripts",
     "icons": {
       "48": "icons/icon-48.png",
       "96": "icons/icon-96.png"
     },
     "permissions": [
       "activeTab",
       "tabs",
       "nativeMessaging",
       "http://localhost/*"
     ],
     "browser_action": {
       "default_icon": {
         "48": "icons/icon-48.png"
       },
       "default_title": "YouTube Summary",
       "default_popup": "popup.html"
     },
     "content_scripts": [
       {
         "matches": ["*://*.youtube.com/watch*"],
         "js": ["content.js"]
       }
     ],
     "background": {
       "scripts": ["background.js"]
     }
   }
   ```

3. **Create a simple backend API** that the extension can call:
   ```bash
   touch firefox-extension/server.py
   ```

   With the following code:
   ```python
   #!/usr/bin/env python3
   import flask
   from flask import Flask, request, jsonify
   from flask_cors import CORS
   import sys
   import os

   # Add the parent directory to the path so we can import the youtube_summary package
   sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

   from youtube_summary.transcript import get_transcript_text
   from youtube_summary.summarizer import summarize_text

   app = Flask(__name__)
   CORS(app)  # Enable CORS for all routes

   @app.route('/api/transcript', methods=['POST'])
   def get_transcript():
       data = request.json
       video_url = data.get('url')
       languages = data.get('languages', ['en'])
       
       try:
           transcript = get_transcript_text(video_url, languages=languages)
           return jsonify({'success': True, 'transcript': transcript})
       except Exception as e:
           return jsonify({'success': False, 'error': str(e)}), 400

   @app.route('/api/summarize', methods=['POST'])
   def summarize():
       data = request.json
       video_url = data.get('url')
       languages = data.get('languages', ['en'])
       max_length = data.get('max_length')
       provider = data.get('provider')
       model = data.get('model')
       
       try:
           # Get transcript
           transcript = get_transcript_text(video_url, languages=languages)
           
           # Prepare kwargs for summarize_text
           kwargs = {}
           if provider:
               kwargs['provider_name'] = provider
           if model:
               kwargs['model_name'] = model
               
           # Summarize
           summary = summarize_text(transcript, max_length=max_length, **kwargs)
           
           return jsonify({
               'success': True, 
               'summary': summary,
               'transcript': transcript
           })
       except Exception as e:
           return jsonify({'success': False, 'error': str(e)}), 400

   if __name__ == '__main__':
       app.run(debug=True, port=5000)
   ```

4. **Create a popup UI** (`firefox-extension/popup.html`):
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <meta charset="utf-8">
     <style>
       body {
         width: 400px;
         padding: 10px;
         font-family: system-ui, -apple-system, sans-serif;
       }
       button {
         margin-top: 10px;
         padding: 5px 10px;
         background-color: #0060df;
         color: white;
         border: none;
         border-radius: 4px;
         cursor: pointer;
       }
       button:hover {
         background-color: #003eaa;
       }
       .result {
         margin-top: 10px;
         max-height: 300px;
         overflow-y: auto;
         border: 1px solid #ccc;
         padding: 10px;
         white-space: pre-wrap;
       }
       .error {
         color: red;
       }
       .loading {
         color: #666;
         font-style: italic;
       }
       .options {
         margin-top: 10px;
         padding: 5px;
         border: 1px solid #eee;
         border-radius: 4px;
       }
       label {
         display: block;
         margin: 5px 0;
       }
     </style>
     <script src="popup.js"></script>
   </head>
   <body>
     <h2>YouTube Summary</h2>
     <div id="not-youtube" style="display: none;">
       <p>This is not a YouTube video page. Please navigate to a YouTube video to use this extension.</p>
     </div>
     <div id="youtube-content">
       <button id="get-transcript">Get Transcript</button>
       <button id="get-summary">Get Summary</button>
       
       <div class="options">
         <label>
           Languages:
           <input type="text" id="languages" placeholder="en,fr,es" value="en">
         </label>
         <label>
           Provider:
           <select id="provider">
             <option value="ollama">Ollama (Local)</option>
             <option value="openai">OpenAI</option>
             <option value="anthropic">Anthropic</option>
           </select>
         </label>
         <label>
           Max Length:
           <input type="number" id="max-length" placeholder="Optional">
         </label>
       </div>
       
       <div id="result" class="result" style="display: none;"></div>
     </div>
   </body>
   </html>
   ```

5. **Create popup logic** (`firefox-extension/popup.js`):
   ```javascript
   document.addEventListener('DOMContentLoaded', () => {
     const getTranscriptBtn = document.getElementById('get-transcript');
     const getSummaryBtn = document.getElementById('get-summary');
     const resultDiv = document.getElementById('result');
     const notYoutubeDiv = document.getElementById('not-youtube');
     const youtubeContentDiv = document.getElementById('youtube-content');
     
     // Check if current page is a YouTube video
     browser.tabs.query({ active: true, currentWindow: true }).then(tabs => {
       const url = tabs[0].url;
       if (!url.includes('youtube.com/watch')) {
         notYoutubeDiv.style.display = 'block';
         youtubeContentDiv.style.display = 'none';
       }
     });
     
     // Get transcript button
     getTranscriptBtn.addEventListener('click', () => {
       resultDiv.style.display = 'block';
       resultDiv.textContent = 'Loading transcript...';
       resultDiv.className = 'result loading';
       
       const languages = document.getElementById('languages').value.split(',').map(lang => lang.trim());
       
       browser.tabs.query({ active: true, currentWindow: true }).then(tabs => {
         const url = tabs[0].url;
         
         fetch('http://localhost:5000/api/transcript', {
           method: 'POST',
           headers: {
             'Content-Type': 'application/json',
           },
           body: JSON.stringify({ url, languages }),
         })
         .then(response => response.json())
         .then(data => {
           if (data.success) {
             resultDiv.textContent = data.transcript;
             resultDiv.className = 'result';
           } else {
             resultDiv.textContent = `Error: ${data.error}`;
             resultDiv.className = 'result error';
           }
         })
         .catch(error => {
           resultDiv.textContent = `Error: ${error.message}`;
           resultDiv.className = 'result error';
         });
       });
     });
     
     // Get summary button
     getSummaryBtn.addEventListener('click', () => {
       resultDiv.style.display = 'block';
       resultDiv.textContent = 'Generating summary...';
       resultDiv.className = 'result loading';
       
       const languages = document.getElementById('languages').value.split(',').map(lang => lang.trim());
       const provider = document.getElementById('provider').value;
       const maxLength = document.getElementById('max-length').value || null;
       
       browser.tabs.query({ active: true, currentWindow: true }).then(tabs => {
         const url = tabs[0].url;
         
         fetch('http://localhost:5000/api/summarize', {
           method: 'POST',
           headers: {
             'Content-Type': 'application/json',
           },
           body: JSON.stringify({ 
             url, 
             languages,
             provider,
             max_length: maxLength,
           }),
         })
         .then(response => response.json())
         .then(data => {
           if (data.success) {
             resultDiv.textContent = data.summary;
             resultDiv.className = 'result';
           } else {
             resultDiv.textContent = `Error: ${data.error}`;
             resultDiv.className = 'result error';
           }
         })
         .catch(error => {
           resultDiv.textContent = `Error: ${error.message}\n\nMake sure the backend server is running: python firefox-extension/server.py`;
           resultDiv.className = 'result error';
         });
       });
     });
   });
   ```

6. **Create content script** (`firefox-extension/content.js`):
   ```javascript
   // This script runs on YouTube pages
   console.log("YouTube Summary extension loaded");
   
   // You can add functionality to inject UI elements into the YouTube page if desired
   // For example, adding a "Summarize" button next to the video title
   ```

7. **Create background script** (`firefox-extension/background.js`):
   ```javascript
   // Background script for handling events
   console.log("YouTube Summary background script loaded");
   
   // You can add functionality like context menu items here
   ```

8. **Load the extension in Firefox**:
   - Open Firefox
   - Navigate to `about:debugging`
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Select any file in your extension directory

9. **Start the backend server**:
   ```bash
   python firefox-extension/server.py
   ```

10. **Use the extension**:
    - Navigate to a YouTube video
    - Click the extension icon
    - Click "Get Summary"

This is a simplified implementation and would need additional error handling and features for a production-ready extension.
