import base64
import os
import random
from datetime import datetime
from tkinter import *
from tkinter import filedialog
import httpx
import pandas as pd
import streamlit as st
from cv2 import VideoCapture, imwrite
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from movement import *

load_dotenv('.env', override=True)

http_client=httpx.Client(verify=False)

# Loading API key and URL for the AI
client = OpenAI(
    base_url=os.environ["url"],
    http_client=http_client,
    api_key=os.environ["DEV_GENAI_API_KEY"]
)

# Settings for my AI model
streaming = False  # Makes answers more coherent
#max_output_tokens = 200
max_output_tokens = 50
custom = os.getenv("custom_ai")
custom_prompt = os.getenv("code_documentation")


available_models = ["llama-3-8b-instruct", "mixtral-8x7b-instruct-v01", "llamaguard-7b", "mistral-7b-instruct-v03", "phi-3-mini-128k-instruct",
                    "phi-3-5-moe-instruct", "llama-3-1-8b-instruct", "llama-3-2-3b-instruct",
                    "codellama-13b-instruct", "sqlcoder-7b-2", "codestral-22b-v0-1"]

# Selecting a model
model_selected = available_models[0]

stop_conversation = threading.Event()


def train_from_dataset():
    df = pd.read_csv('Conversation.csv')

    # Preprocessing data
    df['text'] = df['question'] + ' ' + df['answer']
    df = df.drop(columns=['Unnamed: 0', 'question', 'answer'])

    # Splitting data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(df['text'], df['text'], test_size=0.2, random_state=42)

    model = make_pipeline(CountVectorizer(), MultinomialNB())

    # Training model
    model.fit(X_train, y_train)


def ohbot_text_to_speech(text):
    ohbot.say(text)

def get_response(prompt):
    response = client.completions.create(
        model=model_selected,
        max_tokens=max_output_tokens,
        prompt= custom + prompt,
        stream=streaming,
        temperature=0.5
    )

    response_text = ""
    if streaming:
        for chunk in response:
            response_text += chunk.choices[0].text
    else:
        response_text = response.choices[0].text

    return response_text


def take_image():
    cam_port = 0
    camera = VideoCapture(cam_port)
    success, image = camera.read()
    file = "Capture.png"
    if success:
        imwrite(file, image)
        image_thread = threading.Thread(target=identify_image, args=(file,))
        image_thread.start()
        return file
    else:
        print("No camera found")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def identify_image(image_path):
    # Encoding the image
    base64_image = encode_image(image_path)
    image_url = f"data:image/jpeg;base64,{base64_image}"

    image_models = ["llama-3-2-11b-vision-instruct", "llava-v1-6-34b-hf-vllm"]
    selected_model = image_models[0]

    completion = client.chat.completions.create(
        model=selected_model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text",
                 "text": "What object can you see on the image? You should just name the object. "
                         "The answer should be one sentence at a maximum"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ],
        }],
        stream=streaming
    )

    if streaming:
        for chunk in completion:
            if chunk.id:
                if chunk.choices[0].delta.content is None and chunk.choices[0].delta.role is not None:
                    print(chunk.choices[0].delta.role + ': ', end='')
                elif chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end='')
    else:
        print(completion.choices[0].message.role + ': ' + completion.choices[0].message.content)



def generate_unit_tests(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    response = client.completions.create(
        model=model_selected,
        max_tokens=max_output_tokens,
        prompt= f"Generate unit tests for the following code:\n\n{code}",
        stream=streaming
    )

    unit_tests = response["message"]["content"]
    print("Generated Unit Tests:\n", unit_tests)
    ohbot_text_to_speech("I have created unit tests for you in the same folder as your code. Check it out")


def choose_file():
    file_path = filedialog.askopenfilename(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("all files", "*.*"),
                                                      ("Text files", "*.txt*")))

    return file_path

def background_animation():
    while not stop_conversation.is_set():
        natural_head_movement()
        random_blink()

# def write_docstrings():
    # test

def write_documentation(code):
    response = client.completions.create(
        model=model_selected,
        max_tokens=200,
        prompt= custom_prompt + f"{code}",
        stream=streaming
    )

    documentation = response.choices[0].text
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Code Documentation {timestamp}.txt"
    with open(filename, "w") as file:
        file.write(documentation)

    file.close()

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        word_list = file.read().splitlines()
        return word_list

def generate_key(words):
    random_word = random.choice(words) + random.choice(words) + random.choice(words)
    return random_word

if __name__ == '__main__':
    st.title("Ohbot AI")
    st.write("Welcome!")

    ohbot.reset()
    animation_thread = threading.Thread(target=background_animation)
    animation_thread.start()

    words = read_file("words.txt")
    train_from_dataset()
    user_input = st.text_input("You: ")
    if user_input:
        if user_input.lower() == "what is this":
            captured_photo = take_image()
            identify_image(captured_photo)
        elif user_input.lower() == "documentation":
            file_path = choose_file()
            code = read_file(file_path)
            write_documentation(code)
        #elif user_input.lower() == "docstrings":
        elif user_input.lower() == "unit tests":
            file_path = choose_file()
            code = read_file(file_path)
            generate_unit_tests(code)
        elif user_input.lower() == "exit":
            stop_conversation.set()
            shutdown()
            exit(0)
        fetched_response = get_response(user_input)
        st.write(f"Ohbot: {fetched_response}")
        ohbot_text_to_speech(fetched_response)
    animation_thread.join()
    shutdown()
