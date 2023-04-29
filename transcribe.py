import openai
from key import api_key


API_KEY = api_key
model_id = 'whisper-1'

media_file_path = 'audio.mp3'
media_file = open(media_file_path, 'rb')

response = openai.Audio.transcribe(
    api_key=API_KEY,
    model=model_id,
    file=media_file
)
print(response['text'])