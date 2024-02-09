import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

def main():
    root = tk.Tk()
    root.title("SDXL-Turbo Model Card")

    style = ttk.Style()
    style.theme_use("clam") 

    label = ttk.Label(root, text="Select an operation:")
    label.pack(pady=10)

    button_text_to_image = ttk.Button(root, text="Text-to-image", command=text_to_image_prompt)
    button_text_to_image.pack(pady=5)

    button_image_to_image = ttk.Button(root, text="Image-to-image", command=image_to_image_prompt)
    button_image_to_image.pack(pady=5)

    root.mainloop()


def text_to_image_prompt():
    prompt = simple_prompt_dialog("Enter a text prompt")

    if not prompt:
        messagebox.showwarning("Invalid Input", "Prompt cannot be empty.")
        return

    generate_and_execute_text_to_image_code(prompt)

def image_to_image_prompt():
    prompt = simple_prompt_dialog("Enter a text prompt")

    if not prompt:
        messagebox.showwarning("Invalid Input", "Prompt cannot be empty.")
        return

    generate_and_execute_image_to_image_code(prompt)

def simple_prompt_dialog(prompt_text):
    prompt_dialog = tk.Tk()
    prompt_dialog.title(prompt_text)

    label = tk.Label(prompt_dialog, text=prompt_text)
    label.pack(pady=10)

    entry = tk.Entry(prompt_dialog)
    entry.pack(pady=10)

    submit_button = tk.Button(prompt_dialog, text="Submit", command=lambda: prompt_dialog.destroy())
    submit_button.pack(pady=10)

    prompt_dialog.mainloop()

    return entry.get()

def generate_and_execute_text_to_image_code(prompt):
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

    execute_code_and_show_result(text_to_image_code)

def generate_and_execute_image_to_image_code(prompt):
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

    execute_code_and_show_result(image_to_image_code)

def simple_prompt_dialog(prompt_text):
    prompt_dialog = tk.Toplevel()
    prompt_dialog.title(prompt_text)

    label = tk.Label(prompt_dialog, text=prompt_text)
    label.pack(pady=10)

    entry = tk.Entry(prompt_dialog)
    entry.pack(pady=10)

    def submit():
        # Set the entry value as a result before destroying the dialog
        prompt_dialog.result = entry.get()
        prompt_dialog.destroy()

    submit_button = tk.Button(prompt_dialog, text="Submit", command=submit)
    submit_button.pack(pady=10)

    prompt_dialog.wait_window()

    return prompt_dialog.result if hasattr(prompt_dialog, 'result') else None

def execute_code_and_show_result(code):
    print("Generated code snippet:")
    print(code)

    try:
        # Execute the code using exec
        exec(code)
        print("Code executed successfully.")
        messagebox.showinfo("Success", "Operation completed successfully!")
    except Exception as e:
        # Display an error message if an exception occurs
        print(f"An error occurred: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
