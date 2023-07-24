import os
import torch
import poe
import logging
import sounddevice as sd
import soundfile as sf
from transformers import pipeline, SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
from utils import print_in_green, print_in_red, split_text_into_chunks, sound2text, save_sound, text2sound, record_sound

class Chatbot:
    def __init__(self, token):
        poe.logger.setLevel(logging.INFO)
        self.client = poe.Client(token)

        self.model_name = "SophiaAssistantBot"
        self.input_duration = 5  # Set the desired recording duration
        self.token = token
        self.whisper = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-medium",
            chunk_length_s=30,
            device="cuda" if torch.cuda.is_available() else "cpu",
        )
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embeddings = torch.tensor(self.embeddings_dataset[7306]["xvector"]).unsqueeze(0)

        self.tts = False

    # print a list of commands that can be used
    def help(self):
        print("Here are the available commands:")
        print("- tts(): Sets text-to-speech output to true or false")
        print("- record(): Records audio for a specified duration and converts it to text")
        print("- clear(): Clears the chat history of the current bot")
        print("- exit(): Exits the chatbot program")
        print("- duration(): Sets the duration of the recording in seconds")
        print("- model(): Sets the chatbot to use a different model from poe.com")
        print()
        print("For example, to set the recording duration to 10 seconds, you would enter 'duration(10)'.")
        print("To exit the chatbot program, you would enter 'exit()'.")
    
    # clear the history of the current bot
    def clear(self):
        client.send_chat_break(model_name)

    # set the tts to either true or false (false by default)
    def set_tts(self, message):
        tts = message.split("tts")[1].strip()[1:-1]

        if tts.lower() == 'true':
            self.tts = True
        elif tts.lower() == 'false':
            self.tts = False
        else:
            print("the value must be either true or false, like 'tts(true)'")

    # get the text from the recording
    def record_message(self):
        recording, fs = record_sound(self.input_duration)
        if recording is not None and fs is not None:
            save_sound(recording, fs, "sound.mp3")
            sound2text_output = sound2text("sound.mp3", self.whisper)
            if sound2text_output is not None:
                message = sound2text_output["text"]
                self.process_message(message)

    # change the recording duration
    def set_duration(self, message):
        try:
            self.input_duration = int(message.split("duration")[1].strip()[1:-1])
            print("Duration set to: " + str(self.input_duration))
        except ValueError:
            print("Duration must be an integer")

    # set the model to a new one
    def set_model(self, message):
        self.model_name = message.split("model")[1].strip()[1:-1]
        if self.model_name == "":
            self.model_name = "capybara"
        elif self.model_name == "gpt3":
            self.model_name = "chinchilla"
        elif self.model_name == "sage":
            self.model_name = "capybara"
        print("Model set to: " + self.model_name)

    def process_message(self, message):
        if "[code]" in message:
            from input import code
            message = message.replace("[code]", code)
        if "[readme]" in message:
            from input import readme
            message = message.replace("[readme]", readme)

        # check if sound.mp3 exists
        if os.path.exists('sound.mp3'):
            sound2text_output = sound2text('sound.mp3', self.whisper)
            text = sound2text_output['text']

        response_text = ""  # Variable to store the chatbot response

        print("AI: ", end="", flush=True)
        for chunk in self.client.send_message(self.model_name, message, with_chat_break=False):
            response_text += chunk["text_new"]
            print_in_green(chunk["text_new"])
        print()

        if self.tts:
            # play the response
            text2sound(response_text, self.speaker_embeddings, self.processor, self.vocoder, self.model)
            
            with open("response.txt", "a") as file:
                file.write('User: ' + message)
                file.write("\n")
                file.write('AI: ' + response_text)
                file.write("\n")
                # Save the response to the file
