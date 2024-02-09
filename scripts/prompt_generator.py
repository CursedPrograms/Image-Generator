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

    subject = random.choice(["the castle", "the forest", "the city", "the astronaut", "the dragon", "the ocean", "the mountain", "the time traveler", "the wizard", "the detective", "the robot", "the pirate", "the alien", "the superhero", "the vampire"])
    adjective = random.choice(["ominous", "enchanted", "majestic", "futuristic", "medieval", "whimsical", "mysterious", "celestial", "ethereal", "timeless", "mythical", "steampunk", "luminous", "galactic", "cryptic"])
    color = random.choice(["vibrant", "pastel", "bold", "subtle", "expressive", "neon", "earthy", "muted", "rich", "mellow", "vivid", "soft", "warm", "cool", "playful", "sophisticated", "monochromatic", "grayscale", "fiery", "calm"])
    emotion = random.choice(["whimsical", "nostalgic", "uplifting", "serene", "ecstatic", "thoughtful", "inspiring", "tranquil", "joyful", "melancholic", "energetic", "peaceful", "hopeful", "adventurous", "dreamy", "reflective", "amused", "grateful", "determined", "content"])
    character = random.choice(["he", "she", "they"])
    name = random.choice(["Alice", "Bob", "Ella", "Leo", "Sophia"])
    occasion = random.choice(["birthday", "wedding", "graduation", "celebration", "reunion", "anniversary", "promotion", "retirement", "engagement", "baby shower", "housewarming", "farewell", "victory party", "achievement", "milestone", "success", "holiday", "commencement", "awards ceremony", "family gathering"])
    fantasy_element = random.choice(["magic", "dragons", "aliens", "mythical creatures", "time travel", "wizards", "elves", "fairies", "unicorns", "parallel dimensions", "enchanted realms", "sorcery", "extraterrestrial civilizations", "mystical artifacts", "prophecies", "ghosts", "shape-shifters", "teleportation", "portals"])
    real_world_element = random.choice(["technology", "nature", "history", "science", "culture", "architecture", "art", "music", "literature", "geography", "astronomy", "medicine", "politics", "economics", "sports", "environment", "philosophy", "language", "mathematics", "psychology"])
    event = random.choice(["an unexpected meeting", "a grand adventure", "a tragic incident", "a joyful celebration", "a mysterious discovery", "a thrilling escape", "an epic journey", "a heartwarming reunion", "a scientific breakthrough", "a cultural festival", "a daring rescue", "a romantic encounter", "a cosmic phenomenon", "a historical moment", "a technological innovation", "a surprising revelation", "a peaceful retreat", "a suspenseful mission", "a challenging quest", "an artistic masterpiece"])

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
