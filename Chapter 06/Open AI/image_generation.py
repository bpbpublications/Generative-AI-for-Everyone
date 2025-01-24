from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

response = client.images.generate(
  model="dall-e-2",
  prompt="A person studying Generative AI",
  size="1024x1024",
  quality="standard",
  style = 'vivid',
  n=1,
)
print(response.data[0].url)

