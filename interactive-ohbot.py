from ohbot import ohbot
import ollama
import speech_recognition as sr
from pocketsphinx import LiveSpeech


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
    # Using the microphone and converting it to text
    with sr.Microphone() as source:
        print("Start talking...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_sphinx(audio)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Sorry, Can you repeat that?")

if __name__ == '__main__':
    # Starting up Ohbot
    ohbot.reset()

    recognizer = sr.Recognizer()
    speech_to_text()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            # Closing down ohbot
            ohbot.reset()
            ohbot.close()
            break
        fetched_response = get_response(user_input)
        print(f"Ohbot: {fetched_response}")
        ohbot_text_to_speech(fetched_response)

    # If the program closes unexpectedly ohbot should still shut down properly
    ohbot.reset()
    ohbot.close()
