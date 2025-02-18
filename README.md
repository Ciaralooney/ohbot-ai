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

If you would like to personalise the AI prompt 
```
ollama show llama3:latest --modelfile > myllama3.modelfile
```
Your file should be in this location 
![image](https://github.com/user-attachments/assets/fad576c5-e827-40d3-8443-8b3b5779f7bb)
Edit the file with notepad
You should add paramters like these depending on your goal
![image](https://github.com/user-attachments/assets/c99af10b-4169-42df-bdf9-3a72820d68e5)

Save your text file and then run 
```
ollama create new-phi --file myllama3.modelfile
```
to apply your changes to your AI model.

