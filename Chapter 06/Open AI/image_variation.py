from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
img =open('GenAI_Image.png','rb')
response = client.images.create_variation(
  image=img,
  size="1024x1024",
  n=1,
)
print(response.data[0].url)
