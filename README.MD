# DEMO:
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>

# README

This script records audio from your microphone and sends it to the [Whisper AI](https://whisper.ai/) to transcribe it into text. Then it uses [DeepL](https://www.deepl.com/) to translate the text from English to Japanese, and finally, it calls the [VoiceVox Engine](https://github.com/Hiroshiba/voicevox_engine) to generate speech from the translated Japanese text and plays it back.

## Requirements

- Python 3
- [Whisper AI](https://openai.com/research/whisper) installed on your machine, `pip install git+https://github.com/openai/whisper.git`
- [DeepL API key](https://www.deepl.com/pro/change-plan/api)
- [VoiceVox Engine Docker image](https://hub.docker.com/r/voicevox/voicevox_engine) running in a Docker container. You can pull the image by running `docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest` and start the container by running `docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest` command.

## Usage

1. Clone this repository and navigate to the directory.
2. Install the required Python packages by running `pip install -r requirements.txt` command.
3. Start the VoiceVox Engine Docker container by running `docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest` command.
4. Run the script by running `python main.py` command.
5. Press the `r` key on your keyboard to start and stop recording. When you stop recording, the script will transcribe the audio, translate the text, and generate speech in Japanese from the translated text.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
