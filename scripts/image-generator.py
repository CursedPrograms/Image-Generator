from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image
import torch
from PIL import Image
import os
import sys
import subprocess

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
    print("pip install diffusers transformers accelerate torch==1.10.0 Pillow==8.2.0 --upgrade")
    print()

    print("Sample prompt:")
    prompt = input("Enter a text prompt: ")

    text_to_image_code = f"""
from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image
import os

pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", variant="fp16")
pipe.to("cpu")

prompt = "{prompt}"

image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

# Ensure the 'output' directory exists
os.makedirs("output", exist_ok=True)

image.save("output/output.jpg")
main()
    """

    print()
    print("Generated code snippet:")
    print(text_to_image_code)

    exec(text_to_image_code)

def image_to_image_prompt():
    print("Using SDXL-Turbo for Image-to-image:")
    print("Make sure to install the required packages using:")
    print("pip install diffusers transformers accelerate torch==1.10.0 Pillow==8.2.0 --upgrade")
    print()

    print("Sample prompt:")
    prompt = input("Enter a text prompt: ")

    input_folder = "input"
    input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    if not input_files:
        print("No images found in the 'input' folder. Exiting.")
        sys.exit()

    image_path = os.path.join(input_folder, input_files[0])

    init_image = load_image(image_path).resize((512, 512))

    image_to_image_code = f"""
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image
import torch
from PIL import Image
import os

pipe = AutoPipelineForImage2Image.from_pretrained("stabilityai/sdxl-turbo", variant="fp16")
pipe.to("cpu")

# Use the first image in the 'input' folder
init_image = load_image("{image_path}").resize((512, 512))

prompt = "{prompt}"

image = pipe(prompt, image=init_image, num_inference_steps=2, strength=0.5, guidance_scale=0.0).images[0]

os.makedirs("output", exist_ok=True)

image.save("output/output.jpg")
main()
    """

    print()
    print("Generated code snippet:")
    print(image_to_image_code)

    exec(image_to_image_code)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    main_script_path = os.path.join(script_dir, "..", "main.py")
    
    subprocess.run(["python", main_script_path])
