import sys
import os

def main():
    print("SDXL-Turbo Model Card")
    print("1. Text-to-image")
    print("2. Image-to-image")

    choice = input("Select an operation (1 or 2): ")

    if choice == "1":
        text_to_image_prompt()
    elif choice == "2":
        image_to_image_prompt()
    else:
        print("Invalid choice. Exiting.")
        sys.exit()

def text_to_image_prompt():
    print("Using SDXL-Turbo for Text-to-image:")
    print("Make sure to install the required packages using:")
    print("pip install diffusers transformers accelerate --upgrade")
    print()

    print("Sample prompt:")
    prompt = input("Enter a text prompt: ")

    text_to_image_code = f"""
from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
pipe.to("cpu")
prompt = "{prompt}"
image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
output_directory = 'output'
os.makedirs(output_directory, exist_ok=True)
image.save(os.path.join(output_directory, 'output.jpg'))
    """

    print()
    print("Generated code snippet:")
    print(text_to_image_code)

    exec(text_to_image_code)

def image_to_image_prompt():
    print("Using SDXL-Turbo for Image-to-image:")
    print("Make sure to install the required packages using:")
    print("pip install diffusers transformers accelerate --upgrade")
    print()

    print("Sample prompt:")
    prompt = input("Enter a text prompt: ")

    image_to_image_code = f"""
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image
import torch
from PIL import Image
pipe = AutoPipelineForImage2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
pipe.to("cpu")
image_path = "input/input.jpg"  
init_image = load_image(image_path).resize((512, 512))
prompt = "{prompt}"
image = pipe(prompt, image=init_image, num_inference_steps=2, strength=0.5, guidance_scale=0.0).images[0]
output_directory = 'output'
os.makedirs(output_directory, exist_ok=True)
image.save(os.path.join(output_directory, 'output.jpg'))
    """

    print()
    print("Generated code snippet:")
    print(image_to_image_code)

    exec(image_to_image_code)

if __name__ == "__main__":
    main()