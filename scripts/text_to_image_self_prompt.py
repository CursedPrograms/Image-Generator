import os
import json
import time

def text_to_image_prompt(prompt):
    print("Using SDXL-Turbo for Text-to-image:")
    print("Make sure to install the required packages using:")
    print("pip install diffusers transformers accelerate --upgrade")
    print()

    print("Sample prompt:")
    print(f"Enter a text prompt: {prompt}")

    output_directory = 'output/generated_images'
    os.makedirs(output_directory, exist_ok=True)

    # Use a counter to create a unique filename
    counter = 1
    output_filename = f'output_{counter}.jpg'
    while os.path.exists(os.path.join(output_directory, output_filename)):
        counter += 1
        output_filename = f'output_{counter}.jpg'

    text_to_image_code = f"""
from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
pipe.to("cpu")
prompt = "{prompt}"
image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
output_directory = 'output/generated_images'
os.makedirs(output_directory, exist_ok=True)
image.save(os.path.join(output_directory, '{output_filename}'))
    """

    print()
    print("Generated code snippet:")
    print(text_to_image_code)

    exec(text_to_image_code)

def main():
    json_file_path = 'prompts.json'

    while True:
        try:
            with open(json_file_path, 'r') as file:
                prompts = json.load(file)
        except FileNotFoundError:
            prompts = []

        if prompts:
            for prompt in prompts:
                text_to_image_prompt(prompt)
        else:
            print(f"No prompts found in {json_file_path}")

        time.sleep(60) 

if __name__ == "__main__":
    main()
