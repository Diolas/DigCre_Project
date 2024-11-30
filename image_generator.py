import requests
import io
import base64
from PIL import Image
import time

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}

def generate_image(prompt, filename):
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 25
        }
    }

    for attempt in range(5):  # Retry up to 5 times because of time out 
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            if "images" in response_data:
                image_data = response_data["images"][0]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))

                # Resize to portrait style 
                image = image.resize((512, 1024), Image.ANTIALIAS)
                image.save(filename)
                print(f"Image saved as '{filename}'")
            else:
                print("Unexpected response format.")
            break

        elif response.status_code == 503:
            print("Model is loading, waiting before retrying...")
            time.sleep(60)

        else:
            print(f"Failed to generate image. Status code: {response.status_code}")
            print("Response:", response.json())
            break
