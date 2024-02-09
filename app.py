from flask import Flask, render_template, request, url_for
import os
import webbrowser
import shutil  # Import the shutil module for file operations

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')


def copy_newest_images(output_directory, target_directory, num_images=10):
    # Get the list of generated images sorted by modification time
    generated_images = sorted(os.listdir(output_directory), key=lambda f: os.path.getmtime(os.path.join(output_directory, f)))

    # Ensure the target directory exists
    os.makedirs(target_directory, exist_ok=True)

    # Copy the 10 newest images to the target directory
    for image in generated_images[-num_images:]:
        source_path = os.path.join(output_directory, image)
        target_path = os.path.join(target_directory, image)
        shutil.copyfile(source_path, target_path)

@app.route('/text_to_image', methods=['POST'])
def text_to_image():
    prompt = request.form.get('prompt')
    output_directory = 'output/generated_images'
    os.makedirs(output_directory, exist_ok=True)

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

    print("Generated code snippet:")
    print(text_to_image_code)

    exec(text_to_image_code)

    # Copy the 10 newest images to the static/generated_images folder
    copy_newest_images(output_directory, 'static/generated_images', num_images=10)

    return render_template('index.html', result_image=output_filename)

@app.route('/image_to_image', methods=['POST'])
def image_to_image():
    prompt = request.form.get('prompt')
    output_directory = 'output/generated_images'
    os.makedirs(output_directory, exist_ok=True)

    counter = 1
    output_filename = f'output_{counter}.jpg'
    while os.path.exists(os.path.join(output_directory, output_filename)):
        counter += 1
        output_filename = f'output_{counter}.jpg'

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
output_directory = 'output/generated_images'
os.makedirs(output_directory, exist_ok=True)
image.save(os.path.join(output_directory, '{output_filename}'))
    """

    print("Generated code snippet:")
    print(image_to_image_code)

    exec(image_to_image_code)

    # Copy the 10 newest images to the static/generated_images folder
    copy_newest_images(output_directory, 'static/generated_images', num_images=10)

    return render_template('index.html', result_image=output_filename)

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True, use_reloader=False)
