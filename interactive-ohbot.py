from ohbot import ohbot
import ollama

# Starting up Ohbot
ohbot.reset()
ohbot.init()

def ohbot_speak(text):
    ohbot.say(text)

def get_response(prompt):
    response = ollama.chat(
        model="llama3",
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
        break
    fetched_response = get_response(user_input)
    print(f"Ohbot: {fetched_response}")
    ohbot_speak(fetched_response)

ohbot.close()
