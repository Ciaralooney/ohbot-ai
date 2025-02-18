from ohbot import ohbot
import ollama

# Starting up Ohbot
ohbot.reset()
ohbot.init()

def ohbot_speak(text):
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

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        # Closing down ohbot
        ohbot.reset()
        ohbot.close()
        break
    fetched_response = get_response(user_input)
    print(f"Ohbot: {fetched_response}")
    ohbot_speak(fetched_response)

# If the program closes unexpectedly ohbot should still shut down properly
ohbot.reset()
ohbot.close()
