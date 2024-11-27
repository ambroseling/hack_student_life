import inference
import os
from inference.models.paligemma.paligemma import PaliGemma
from dotenv import load_dotenv
load_dotenv(".env.dev")
pg = PaliGemma("paligemma-3b-mix-224", api_key=os.getenv("ROBOFLOW_API_KEY"))


from PIL import Image

image = Image.open("image.jpeg") # Change to your image

prompt = "Where is the event happening?"

result = pg.predict(image,prompt)

print(result)