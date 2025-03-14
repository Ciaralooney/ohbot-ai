# Ohbot - An AI Companion
![R](https://github.com/user-attachments/assets/ef9507f9-7db8-45b1-8a30-4eca621401b2)

## Python Setup
Download [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)

Download and setup [python 3.12](https://www.python.org/downloads/release/python-3120/)

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
# Ollama
## How to create a local AI server on your computer
1. Download [Ollama](https://ollama.com/)
Open the application and go through the setup mode so it's installed
2. Open powershell and run the below commands:

To start the chatbot
```
ollama run llama3.2-vision
```
To start the server. (Before doing this, check the windows toolbar and close any open Ollama programs)
```
ollama serve
```

### If you would like to personalise the AI prompt 
```
ollama show llama3.2-vision:latest --modelfile > newai.modelfile
```
Your file should be in this location 

![image](https://github.com/user-attachments/assets/fad576c5-e827-40d3-8443-8b3b5779f7bb)

Edit the file with notepad
You should add paramters like these depending on your goal
<img src="https://github.com/user-attachments/assets/c99af10b-4169-42df-bdf9-3a72820d68e5" height="194" width="546" />

Save your text file and then run 
```
ollama create new-phi --file newai.modelfile
```
to apply your changes to your AI model.

When you run the command below you should see the new custom AI model you have set up. 
```
 ollama list
```
![image](https://github.com/user-attachments/assets/2394a6c9-a0e6-4afa-a8e2-faf095a45f45)

I have switched to using this in my code but left the option for llama3 for anyone who does not wish to set this part up

# Gen AI 
This version is dependant on your own API key and internet connection but it is much faster. 

To install the necessary python libraries you should run all of the commands below

```
pip install os datasets openai httpx dotenv transformers PIL torch
```
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

```
pip install -U "huggingface_hub[cli]"
```
## Training AI from a Dataset

Make sure to download the excel file in github or from the original source: https://www.kaggle.com/datasets/kreeshrajani/3k-conversations-dataset-for-chatbot?resource=download 

Ensure you have the txt file downloaded and in the same directory. Txt file source: https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa-no-swears-long.txt

# Streamlit
To utilise streamlit with this 
```
pip install streamlit
```
```
streamlit hello
```
```
 streamlit run '.\GenAI with Streamlit version.py'
```

# .env File
Your .env file should have the following parameters
```
DEV_GENAI_API_KEY="your api key goes here"
url="GEN AI development website url goes here"
custom_ai="This should be your prompt to set up your AI bot initially "
code_documentation="custom prompt to fine tune code documentation output"
unit_tests="custom prompt to fine tune unit tests output"
docstrings="custom prompt to fine tune doc strings output"
```
