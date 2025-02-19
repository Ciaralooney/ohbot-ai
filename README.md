# Ohbot - An AI Companion

## Python Setup
Download [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)

Download and setup [python 3.10](https://www.python.org/downloads/release/python-3100/)

Download the following python libraries using these commands
```
pip install "comtypes==1.1.7"
```
```
pip install wheel ohbot ollama SpeechRecognition pyaudio pocketsphinx random time threading
```
```
pip install scikit-build cmake 
```
```
pip install opencv-python
```

## Ohbot Setup
Set up ohbot by following the instructions [here](https://github.com/ohbot/ohbot-python/tree/master) according to your operating system

## How to create a local AI server on your computer
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

### If you would like to personalise the AI prompt 
```
ollama show llama3:latest --modelfile > myllama3.modelfile
```
Your file should be in this location 

![image](https://github.com/user-attachments/assets/fad576c5-e827-40d3-8443-8b3b5779f7bb)

Edit the file with notepad
You should add paramters like these depending on your goal
<img src="https://github.com/user-attachments/assets/c99af10b-4169-42df-bdf9-3a72820d68e5" height="194" width="546" />

Save your text file and then run 
```
ollama create new-phi --file myllama3.modelfile
```
to apply your changes to your AI model.

When you run the command below you should see the new custom AI model you have set up. 
```
 ollama list
```
![image](https://github.com/user-attachments/assets/2394a6c9-a0e6-4afa-a8e2-faf095a45f45)

I have switched to using this in my code but left the option for llama3 for anyone who does not wish to set this part up

