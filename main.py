import os
from dotenv import load_dotenv
from chatbot import Chatbot

load_dotenv()

def main():
    token = os.getenv("TOKEN")
    chatbot = Chatbot(token)
    
    print("""Hello! I'm your personal chatbot assistant. You can ask me anything and I'll do my best to help you out.\n\n
Here are some commands you can use:
- tts(value): Sets text-to-speech output to true or false. Enter 'true' or 'false' as the value.
- record(): Records audio for a specified duration and converts it to text. No input needed.
- clear(): Clears the chat history of the current bot. No input needed.
- exit(): Exits the chatbot program. No input needed.
- duration(seconds): Sets the duration of the recording in seconds. Enter the number of seconds as the input.
- model(name): Sets the chatbot to use a different poe bot. Enter the name of the model as the input.
- mp3(): Imports an mp3 file called sound.mp3 and converts it to variable [mp3], which can be used in the prompt. 
\n\n
To get more information on these commands, just type 'help()' and I'll provide you with more details.\n\n
What can I help you with today?""")

    while True:
        message = input("\033[91mYou: \033[0m")

        if message.lower() == "exit()":
            break

        if message.lower() == "help()":
            chatbot.help()

        if message.lower() == "clear()":
            chatbot.clear()
            continue

        if message.lower() == "mp3":
            chatbot.import_mp3()
            continue

        if message.startswith("tts"):
            chatbot.set_tts(message)
            continue

        if message.lower() == "record()":
            chatbot.record_message()
            continue

        if message.startswith("duration"):
            chatbot.set_duration(message)
            continue

        if message.startswith("model"):
            chatbot.set_model(message)
            continue

        chatbot.process_message(message)

    print("Exiting")


if __name__ == "__main__":
    main()
