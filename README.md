# unipdFisppaIdentityResearch

## Setup

### Ollama

Ollama (https://ollama.com/) is a service that allows the download and running of local models. In this case we will utilize a python library.

1. Install Ollama with Homebrew:

`brew install ollama`

2. Start it as a background service:

`brew services start ollama`

3. Download the models (will download to ~/.ollama/models)

`ollama pull gemma4:12b`
`ollama pull llama3.1:8b`
`ollama pull phi4-mini`

4. Finally install python libraries

`pip3 install -r requirements.txt`

## Run

To run, use the following command:

`python3 main.py`