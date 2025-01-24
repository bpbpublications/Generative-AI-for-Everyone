from openai import OpenAI
from dotenv import load_dotenv
from pytube import YouTube
import os
import soundfile as sf
import sounddevice as sd
import io


load_dotenv()
content =" This book is all about Generative AI"
client = OpenAI()
res =client.audio.speech.create(model='tts-1',voice='fable',input=content)

buffer = io.BytesIO()
for chunk in res.iter_bytes(chunk_size=4096):
  buffer.write(chunk)
buffer.seek(0)

with sf.SoundFile(buffer, 'r') as sound_file:
  data = sound_file.read(dtype='int16')
  sd.play(data, sound_file.samplerate)
  sd.wait()