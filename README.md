# POE Chat Assistant

An assistant that allows you to chat with POE bots using either text or voice.

## Features

- Record audio using your microphone and convert it to text using the Whisper ASR model.
- Send text or converted voice input to a POE bot using the POE API client.
- Receive responses from the POE bot and convert them to speech using Microsoft's SpeechT5 text-to-speech model.
- Save chat history to a text file.
- Set the duration of audio recordings.
- Switch between different POE bot models.
- Completely free as it uses a reverse engineered poe api. This can basically be used as an alternative to chat gpt api, which is not free.

## Usage

1. Install requirements: `pip install -r requirements.txt`
2. Find your POE API token - [instructions here](https://github.com/ading2210/poe-api)
3. Add the token to your .env file as `TOKEN = '...'`
4. Run the script: `python main.py`
5. To get a full list of controls, type `help()` 

## Notes
- The default POE bot model is "SophiaAssistantBot", which is a simple assistant bot. You can change this using the `model()` command. For example, `model(leocooks)`
- The default recording duration is 5 seconds. You can change this using the `duration()` command (find more info with `help()`
- Chat history is saved to `response.txt`
- By default, the tts is turned off, but you can turn it on by writing `tts(true)`
