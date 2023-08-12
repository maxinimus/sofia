# Important

Poe seems to have made it impossible to use the reverse engineered POE API.

# POE Chat Assistant

An assistant that allows you to chat with POE bots using text or voice input. Built using a reverse-engineered POE API client.

## Features

- Get help for all available commands using the `help()` command
- Record audio input using your microphone using the `record()` command
- Set the duration of audio recordings using the `duration(<seconds>)` command
- Switch between different POE bot models using the `model(<codename>)` command
- Toggle text-to-speech for bot responses using the `tts(<true/false>)` command
- Clear the chat history with the current bot using `clear()` command
- Exit the assistant using the `exit()` command

## Usage

1. Obtain a POE API token by logging into Poe.com and getting the value of the `p-b` cookie, as described here [Reversed engineered Poe API](https://github.com/ading2210/poe-api).
3. Create a `.env` file and place the acquired token in the `TOKEN` field as such
```.env
TOKEN = '...'
```
2. Install requirements: `pip install -r requirements.txt`
3. Add your POE API token to the .env file as `TOKEN = '<your-token-here>'`
4. Run the script: `python main.py`
5. Use the commands to control the assistant.

## Notes

- The default bot model is `SophiaAssistantBot`
- The default recording duration is `5` seconds
- Chat history is saved to `response.txt`
- The reverse-engineered POE API is not officially supported. Use responsibly and observe rate limits to avoid account bans.

# 