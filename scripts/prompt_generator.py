import os
import json
import time
import random

def load_prompts(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            prompts = json.load(file)
    except FileNotFoundError:
        prompts = []

    return prompts

def save_prompts(json_file_path, prompts):
    try:
        with open(json_file_path, 'w') as file:
            json.dump(prompts, file)
    except Exception as e:
        print(f"Error writing prompts to {json_file_path}: {e}")

def generate_sentence(theme):
    sentence_templates = {
        "gothic": "In the eerie moonlight, {subject} stood alone, surrounded by {adjective} shadows.",
        "artsy": "Brush strokes of {color} paint adorned the canvas, creating an {emotion} masterpiece.",
        "tragic": "Amidst the pouring rain, {character} wept, his/her tears blending with the drops.",
        "happy": "Under the warm sun, {name} smiled, embracing the joyous {occasion}.",
        "everything": "In a world where {fantasy_element} coexists with {real_world_element}, {event} unfolded."
    }

    subject = random.choice(["the castle", "the forest", "the city", "the astronaut", "the dragon"])
    adjective = random.choice(["ominous", "enchanted", "majestic", "futuristic", "medieval"])
    color = random.choice(["vibrant", "pastel", "bold", "subtle", "expressive"])
    emotion = random.choice(["whimsical", "nostalgic", "uplifting", "serene", "ecstatic"])
    character = random.choice(["he", "she", "they"])
    name = random.choice(["Alice", "Bob", "Ella", "Leo", "Sophia"])
    occasion = random.choice(["birthday", "wedding", "graduation", "celebration", "reunion"])
    fantasy_element = random.choice(["magic", "dragons", "aliens", "mythical creatures", "time travel"])
    real_world_element = random.choice(["technology", "nature", "history", "science", "culture"])
    event = random.choice(["an unexpected meeting", "a grand adventure", "a tragic incident", "a joyful celebration", "a mysterious discovery"])

    sentence_template = sentence_templates[theme]
    sentence = sentence_template.format(subject=subject, adjective=adjective, color=color, emotion=emotion,
                                        character=character, name=name, occasion=occasion,
                                        fantasy_element=fantasy_element, real_world_element=real_world_element, event=event)

    return sentence

def main():
    json_file_path = 'prompts.json'
    
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        # If not, create an empty JSON file
        with open(json_file_path, 'w') as file:
            json.dump([], file)

    existing_prompts = load_prompts(json_file_path)
    themes = ["gothic", "artsy", "tragic", "happy", "everything"]

    while True:
        for theme in themes:
            new_sentence = generate_sentence(theme)
            print(f"Generated sentence: {new_sentence}")

            existing_prompts.append(new_sentence)
            save_prompts(json_file_path, existing_prompts)

            time.sleep(1)

if __name__ == "__main__":
    main()
