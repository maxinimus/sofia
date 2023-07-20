import poe
import logging
import os
from dotenv import load_dotenv
import torch
import sounddevice as sd
import soundfile as sf
from transformers import pipeline, SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
from input import code

load_dotenv()

model_name = 'SophiaAssistantBot'
input_duration = 5  # Set the desired recording duration

token = os.getenv("TOKEN")
poe.logger.setLevel(logging.INFO)
client = poe.Client(token)

def print_in_green(text):
    print("\033[92m{}\033[0m".format(text), end="", flush=True)  # Print text in green color

def print_in_red(text):
    print("\033[91m{}\033[0m".format(text), end="", flush=True)  # Print text in red color

def sound2text(soundFile):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    whisper = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-medium",
        chunk_length_s=30,
        device=device,
    )
    text = whisper(soundFile, max_new_tokens=1000)
    return text

def record_sound(duration):
    fs = 44100  # Sample rate
    try:
        # countdown(duration)
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        return recording, fs
    except KeyboardInterrupt:
        print("Recording stopped.")
        return None, None

def countdown(duration):
    for remaining in range(duration, 0, -1):
        print_in_red("\rRecording in progress... {:2d}".format(remaining))
        sd.sleep(1000)  # Wait for 1 second
    print_in_red("\rRecording in progress...  0")
    print()  # New line after the countdown

def save_sound(sound, fs, filename):
    sf.write(filename, sound, fs)
    print("Sound saved to", filename)

def text2sound(text):
    # Load the models and processor outside the function for efficiency
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    # set the speaker to be british


    # Split the input text into chunks of 500 characters or less
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    # Generate speech for each chunk
    speeches = []
    for chunk in chunks:
        inputs = processor(text=chunk, return_tensors="pt")

        # Load speaker embeddings (replace with your own method of obtaining speaker embeddings)
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        speeches.append(speech)

    # Concatenate the generated speeches
    speech = torch.cat(speeches)

    # Write the generated speech to a WAV file
    sf.write("speech.wav", speech.numpy(), samplerate=16000)

    # Play the generated speech
    sd.play(speech.numpy(), 16000)

    return speech

# Load Whisper ASR model
whisper = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-medium",
    chunk_length_s=30,
    device="cuda" if torch.cuda.is_available() else "cpu",
)

while True:
    message = input("\033[91mYou: \033[0m")

    if message.lower() == "record()":
        print("Recording started.")
        recording, fs = record_sound(input_duration)  # Set the desired recording duration
        if recording is not None and fs is not None:
            save_sound(recording, fs, "sound.mp3")
            sound2text_output = sound2text('sound.mp3')
            if sound2text_output is not None:
                message = sound2text_output['text']
            else:
                continue
        else:
            continue
    
    if message.lower() == 'clear()':
        client.send_chat_break(model_name)
        continue;

    if message.lower() == 'exit()':
        break
        
    if message.startswith("duration"):
        input_duration = int(message.split("duration")[1].strip()[1:-1])
        print("Duration set to: " + str(input_duration))
        continue;
    
    # check if the message is set_model(model_name)
    if message.startswith("model"):
        model_name = message.split("model")[1].strip()[1:-1]
        if model_name == "":
            model_name = "capybara"
        elif model_name == "gpt3":
            model_name = "chinchilla"
        elif model_name == "sage":
            model_name = "capybara"
        
        print("Model set to: " + model_name)
        # client.send_chat_break(model_name)
        try:
            messages = client.get_message_history(model_name)
        except:
            print("The model was not found")
            model_name = 'myjarvisbot'

        continue

    if "[code]" in message:
        message = message.replace("[code]", code)
    if "[readme]" in message:
        message = message.replace("[readme]", readme)

    # check if sound.mp3 exists
    if os.path.exists('sound.mp3'):
        sound2text_output = sound2text('sound.mp3')
        text = sound2text_output['text']

    response_text = ""  # Variable to store the chatbot response

    print("AI: ", end="", flush=True)
    for chunk in client.send_message(model_name, message, with_chat_break=False):
        response_text += chunk["text_new"]
        print_in_green(chunk["text_new"])
    
    # play the respons e
    text2sound(response_text)
    
    with open("response.txt", "a") as file:
        file.write('User: ' + message)
        file.write("\n")
        file.write('AI: ' + response_text) 
        file.write("\n")
        # Save the response to the file
    
    print()

print('Exiting')
