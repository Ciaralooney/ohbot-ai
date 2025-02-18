# ohbot-ai
Ohbot - An AI Companion

# How to set up
Download [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)

Download and setup [python 3.10](https://www.python.org/downloads/release/python-3100/)

Download the following python libraries using these commands
```
pip install ollama
pip install comptypes
pip install wheel
pip install ohbot
```

Set up ohbot by following the instructions [here](https://github.com/ohbot/ohbot-python/tree/master) according to your operating system

When that is complete you need to follow these steps to make a local AI server on your computer
1. Download [Ollama](https://ollama.com/)
Open the application and go through the setup mode so it's installed
2. Open powershell and run the below commands:

To start the chatbot
```
ollama run llama3
```
To start the server. (Before doing this, check the windows toolbar and close any open Ollama programs)
```
ollama serve
```
