import os
from dotenv import load_dotenv
from chatbot import Chatbot

load_dotenv()

class Main:
    def __init__(self):
        self.mp3 = ""

    def main(self, mp3 = ""):
        token = os.getenv("TOKEN")
        print('creating bot')
        chatbot = Chatbot(token)
        print('bot created')
        
        print("""Hello! I'm your personal chatbot assistant. You can ask me anything and I'll do my best to help you out.\n\n
    Here are some commands you can use:
    - tts(value): Sets text-to-speech output to true or false. Enter 'true' or 'false' as the value.
    - record(): Records audio for a specified duration and converts it to text. No input needed.
    - clear(): Clears the chat history of the current bot. No input needed.
    - exit(): Exits the chatbot program. No input needed.
    - duration(seconds): Sets the duration of the recording in seconds. Enter the number of seconds as the input.
    - model(name): Sets the chatbot to use a different poe bot. Enter the name of the model as the input.
    - mp3(): Imports an mp3 file called 'input.mp3' and converts it to variable [mp3], which can be used in the prompt. 
    \n
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

            if message.lower() == "mp3()":
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

            code = chatbot.process_message(message)
            if code == -1:
                return -1

        return 0


if __name__ == "__main__":
    print("Starting chatbot...")
    main_class = Main()
    while True:
        print("Calling main function")
        code = main_class.main(main_class.mp3)
        if code == 0:
            break

        if code == -1:
            print("Restart?")
            yn = input("Y/N: ")
            if yn.lower() == "n":
                break
