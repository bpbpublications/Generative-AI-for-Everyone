from PIL import Image 
import numpy as np     
from openai import OpenAI  
from dotenv import load_dotenv 
load_dotenv()
image = Image.open(r"C:\Users\vaishnavi\huggingface-repo\Open AI\GenAI_Image.jpg").convert('RGB') 
image.save('./GenAI_Image.png')
image = Image.open(r"C:\Users\vaishnavi\huggingface-repo\Open AI\GenAI_Image.png").convert('RGB') 
image_array = np.array(image) 
image_array[100 : 200, 100 : 200] = (0, 0, 0) 
image = Image.fromarray(image_array) 
image.save("masked.png") 
Image.open('./masked.png').convert('RGBA').save('./masked1.png')
img=open('GenAI_Image.png','rb')
img_mask=open('masked1.png','rb')

client=OpenAI()
res=client.images.edit(image=img, mask=img_mask,
                prompt='A cat  containing big red moon',n=1,size='1024x1024')
print(res.data[0].url)
