import torch
import soundfile as sf
import sounddevice as sd

def print_in_green(text):
    print("\033[92m{}\033[0m".format(text), end="", flush=True)  # Print text in green color

def print_in_red(text):
    print("\033[91m{}\033[0m".format(text), end="", flush=True)  # Print text in red color

def sound2text(soundFile, whisper):
    text = whisper(soundFile, max_new_tokens=1000)
    return text

def save_sound(sound, fs, filename):
    sf.write(filename, sound, fs)
    print("Sound saved to", filename)

def split_text_into_chunks(text):
    # Split text into words
    words = text.split()

    # Create an empty list to store chunks
    chunks = []

    # Initialize a variable to keep track of the current chunk
    current_chunk = ""

    # Iterate through each word in the text
    for word in words:
        # If adding the current word to the chunk would make it longer than 500 characters,
        # add the current chunk to the list of chunks and start a new chunk with the current word
        if len(current_chunk + word) + 1 > 500:
            chunks.append(current_chunk)
            current_chunk = word
        # Otherwise, add the current word to the current chunk
        else:
            if current_chunk:
                current_chunk += " "
            current_chunk += word

    # Add the final chunk to the list of chunks
    chunks.append(current_chunk)

    return chunks

def split_text_into_chunks(text):
    # Split text into words
    words = text.split()

    # Create an empty list to store chunks
    chunks = []

    # Initialize a variable to keep track of the current chunk
    current_chunk = ""

    # Iterate through each word in the text
    for word in words:
        # If adding the current word to the chunk would make it longer than 500 characters,
        # add the current chunk to the list of chunks and start a new chunk with the current word
        if len(current_chunk + word) + 1 > 500:
            chunks.append(current_chunk)
            current_chunk = word
        # Otherwise, add the current word to the current chunk
        else:
            if current_chunk:
                current_chunk += " "
            current_chunk += word

    # Add the final chunk to the list of chunks
    chunks.append(current_chunk)

    return chunks

def text2sound(text, speaker_embeddings, processor, vocoder, model):
    # Split the input text into chunks of 500 characters or less
    chunks = split_text_into_chunks(text)

    speeches = []
    for chunk in chunks:
        inputs = processor(text=chunk, return_tensors="pt")

        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        speeches.append(speech)

    speech = torch.cat(speeches)
    # Write the generated speech to a WAV file
    sf.write("speech.wav", speech.numpy(), samplerate=16000)

    # Play the generated speech
    sd.play(speech.numpy(), 16000)

    return speech

# record the speech from user
def record_sound(duration):
    fs = 44100
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        countdown(duration)
        sd.wait()  # Wait until recording is finished
        return recording, fs
    except KeyboardInterrupt:
        print("Recording stopped.")
        return None, None

# count down to the end of the recording
def countdown(duration):
    for remaining in range(duration, 0, -1):
        print_in_red("\rRecording in progress... {:2d}".format(remaining))
        sd.sleep(1000)  # Wait for 1 second
    print_in_red("\rRecording in progress...  0")
    print()  # New line after the countdown

# import mp3 file
def mp3_input(whisper):
    try:
        sound2text_output = sound2text("input.mp3", whisper)
    except IndexError:
        return -1

    if sound2text_output is not None:
        mp3 = sound2text_output["text"]
        return mp3

    return None
