import threading
from cv2 import VideoCapture, imwrite
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
import httpx
from dotenv import load_dotenv

load_dotenv()

# Creates HTTP client with not verification
web_client = httpx.Client(verify=False)
'''
client = OpenAI(
    base_url = os.getenv("url"),
    key = os.getenv("OPENAI_API_KEY"),
    http_client = web_client)
    '''

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.getenv("url"),
    http_client=web_client)


stop_conversation = threading.Event()

def ohbot_text_to_speech(text):
    ohbot.say(text)

def get_response(prompt):
    response = client.chat.completions.create(
        model="llama-3-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response["message"]["content"]

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

def identify_image(image):
    response = client.chat.completions.create(
        model="llama-3-8b-instruct",
        messages=[{
            "role": "user",
            "content": "What is the object I am holding?",
            "images": [image]
        }],
    )

    text = response["message"]["content"].strip()
    print(f"Ohbot: {text}")
    ohbot_text_to_speech(text)

def generate_unit_tests(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    response = client.chat.completions.create(
        model="llama-3-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": f"Generate unit tests for the following code:\n\n{code}"
            }
        ],
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