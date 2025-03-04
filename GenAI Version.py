import threading
from cv2 import VideoCapture, imwrite
from google.auth.transport import requests
from ohbot import ohbot
import dotenv
import speech_recognition as sr
from openai._client import OpenAI
from movement import *
from pocketsphinx import LiveSpeech
import tkinter as tk
from tkinter import filedialog
import os
import openai
import base64
import httpx
from dotenv import load_dotenv
from PIL import Image
import torch
from datasets import load_dataset
import requests

response = requests.get('https://cdn-lfs.hf.co/your-url', verify=False)

ds = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")

load_dotenv('.env', override=True)

http_client=httpx.Client(verify=False)

# Loading API key and URL for the AI
client = OpenAI(
    base_url=os.environ["url"],
    http_client=http_client,
    api_key=os.environ["DEV_GENAI_API_KEY"]
)

# Settings for our AI model
streaming = True
max_output_tokens = 200
custom = os.getenv("custom_ai")

available_models = ["llama-3-8b-instruct", "mixtral-8x7b-instruct-v01", "llamaguard-7b", "mistral-7b-instruct-v03", "phi-3-mini-128k-instruct",
                    "phi-3-5-moe-instruct", "llama-3-1-8b-instruct", "llama-3-2-3b-instruct",
                    "codellama-13b-instruct", "sqlcoder-7b-2", "codestral-22b-v0-1"]

# Selecting a model
model_selected = available_models[0]

stop_conversation = threading.Event()

def train_from_dataset():
    print("Training has began...")
    for example in ds['train']:
        prompt = example['prompt']
        response = get_response(prompt)
        print(f"Training Prompt: {prompt}\nTraining Response: {response}\n")
    print("Training has finished...")

def ohbot_text_to_speech(text):
    ohbot.say(text)

def get_response(prompt):
    response = client.completions.create(
        model=model_selected,
        max_tokens=max_output_tokens,
        prompt= custom + prompt,
        stream=streaming
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

def browse_file():
    file_path = filedialog.askopenfilename()
    return file_path

def create_gui():
    root = tk.Tk()
    root.title("Unit Test Generator")
    browse_button = tk.Button(root, text="Browse", command=browse_file)
    browse_button.pack(pady=20)
    root.mainloop()

def background_animation():
    while not stop_conversation.is_set():
        natural_head_movement()
        random_blink()

if __name__ == '__main__':
    ohbot.reset()
    animation_thread = threading.Thread(target=background_animation)
    animation_thread.start()

    train_from_dataset()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "what is this":
            captured_photo = take_image()
            identify_image(captured_photo)
        elif user_input.lower() == "unit tests":
            file_path = browse_file()
            generate_unit_tests(file_path)
        elif user_input.lower() == "exit":
            stop_conversation.set()
            shutdown()
            break
        fetched_response = get_response(user_input)
        print(f"Ohbot: {fetched_response}")
        ohbot_text_to_speech(fetched_response)
    animation_thread.join()
    shutdown()
