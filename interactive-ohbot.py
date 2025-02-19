from ohbot import ohbot
import ollama
import speech_recognition as sr
from movement import *
from pocketsphinx import LiveSpeech

stop_conversation = threading.Event()

def ohbot_text_to_speech(text):
    ohbot.say(text)

def get_response(prompt):
    response = ollama.chat(
        model="new-phi",  # custom AI, if you haven't set one up use llama3
        # model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response["message"]["content"]

def speech_to_text():
    # This is a work in progress
    # Using the microphone and converting it to text
    with sr.Microphone() as source:
        print("Start talking...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_sphinx(audio)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Sorry, Can you repeat that?")

def background_animation():
    while not stop_conversation.is_set():
        natural_head_movement()
        random_blink()

if __name__ == '__main__':
    # Starting up Ohbot
    ohbot.reset()
    # Starting normal ohbot movement
    animation_thread = threading.Thread(target=background_animation)
    animation_thread.start()

    recognizer = sr.Recognizer()
    # speech_to_text()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            stop_conversation.set()
            # Closing down ohbot
            shutdown()
            break
        fetched_response = get_response(user_input)
        print(f"Ohbot: {fetched_response}")
        ohbot_text_to_speech(fetched_response)

    # Stopping ohbots movements
    animation_thread.join()

    # If the program closes unexpectedly ohbot should still shut down properly
    shutdown()
