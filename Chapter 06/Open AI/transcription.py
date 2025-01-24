from openai import OpenAI
from dotenv import load_dotenv
from pytube import YouTube
import os

# for transcriptions
file = YouTube(str("https://www.youtube.com/watch?v=rwF-X5STYks")) 
video_file = file.streams.filter(only_audio=True).first() 
video_out = video_file.download(output_path='./') 
base, ext = os.path.splitext(video_out) 
mp3_file = base + '.mp3'
os.rename(video_out, mp3_file) 


load_dotenv()
client = OpenAI()
file = 'Generative AI explained in 2 minutes.mp3'
with open(file,'rb') as file_audio:
    transcript=client.audio.transcriptions.create(model='whisper-1',file=file_audio)
    # translation=client.audio.translations.create(model='whisper-1',file=file_audio)
print (transcript.text)

