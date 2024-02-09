import sys
import os
from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image

cache_directory = 'cache'
os.makedirs(cache_directory, exist_ok=True)

# Check if the cache directory is empty
if not os.listdir(cache_directory):
    print("Downloading the SDXL-Turbo model. This might take some time...")
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16", cache_dir=cache_directory)
    pipe.to("cpu")
    print("Model downloaded successfully.")
else:
    print("SDXL-Turbo model already exists in the cache directory.")

def main():
    while True:
        print("SDXL-Turbo Model Card")
        print("1. Text-to-image")
        print("2. Image-to-image")
        print("3. Exit")

        choice = input("Select an operation (1, 2, or 3 to exit): ")

        if choice == "1":
            text_to_image_prompt()
        elif choice == "2":
            image_to_image_prompt()
        elif choice == "3":
            print("Exiting program.")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def text_to_image_prompt():
    print("Using SDXL-Turbo for Text-to-image:")
    print("Make sure to install the required packages using:")
    print("pip install diffusers transformers accelerate --upgrade")
    print()

    print("Sample prompt:")
    prompt = input("Enter a text prompt: ")

    output_directory = 'output/generated_images'
    os.makedirs(output_directory, exist_ok=True)

    # Use a counter to create a unique filename
    counter = 1
    output_filename = f'output_{counter}.jpg'
    while os.path.exists(os.path.join(output_directory, output_filename)):
        counter += 1
        output_filename = f'output_{counter}.jpg'

    text_to_image_code = f"""
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

def image_to_image_prompt():
    print("Using SDXL-Turbo for Image-to-image:")
    print("Make sure to install the required packages using:")
    print("pip install diffusers transformers accelerate --upgrade")
    print()

    print("Sample prompt:")
    prompt = input("Enter a text prompt: ")

    output_directory = 'output/generated_images'
    os.makedirs(output_directory, exist_ok=True)

    # Use a counter to create a unique filename
    counter = 1
    output_filename = f'output_{counter}.jpg'
    while os.path.exists(os.path.join(output_directory, output_filename)):
        counter += 1
        output_filename = f'output_{counter}.jpg'


    image_to_image_code = f"""
image_path = "input/input.jpg"  
init_image = load_image(image_path).resize((512, 512))
prompt = "{prompt}"
image = pipe(prompt, image=init_image, num_inference_steps=2, strength=0.5, guidance_scale=0.0).images[0]
output_directory = 'output/generated_images'
os.makedirs(output_directory, exist_ok=True)
image.save(os.path.join(output_directory, '{output_filename}'))
    """

    print()
    print("Generated code snippet:")
    print(image_to_image_code)

    exec(image_to_image_code)

if __name__ == "__main__":
    main()
