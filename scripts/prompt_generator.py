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
        "gothic": [
            "Bathed in haunting moonlight, {subject} lingered in solitude, ensnared by {adjective} shadows.",
            "In the eerie glow of the moon, {subject} cast a lonely silhouette, enveloped by {adjective} shadows.",
            "Silhouetted against the haunting moon, {subject} stood solitary, encircled by {adjective} shadows.",
            "{subject}, illuminated by the ghostly moonlight, stood in isolation amidst {adjective} shadows.",
            "Whispers echoed in the eerie moonlit night as {subject} navigated through the labyrinth of {adjective} shadows."
        ],
        "artsy": [
            "Splashes of {color} danced on the canvas, giving birth to an {emotion} symphony of colors.",
            "With each stroke of the brush, the {color} paint on the canvas whispered tales of an {emotion} journey.",
            "In the quiet studio, {color} hues converged, crafting an {emotion} masterpiece on the awaiting canvas.",
            "The {color} palette came alive as the artist poured {emotion} into every stroke, creating a vibrant tapestry.",
            "Amidst the tranquil atmosphere, the {color} paint on the canvas unveiled an {emotion} narrative, captivating all who beheld it."
        ],
        "tragic": [
            "In the dim candlelight, {character}'s heart shattered, echoing in the silence of despair.",
            "Lost in the cold night, {character} mourned, their sorrow echoing through the empty streets.",
            "As the storm raged outside, {character} clung to memories, drowning in the tempest of grief.",
            "{character} stood alone in the desolate landscape, a figure of sorrow against the backdrop of despair.",
            "Beneath the flickering streetlamp, {character} whispered words of longing, lost in the tragedy of love."
        ],
        "happy": [
            "Beside the blooming flowers, {name} laughed, filling the air with infectious happiness.",
            "In the midst of laughter and music, {name} danced, celebrating the {occasion} with pure joy.",
            "With every step in the soft sand, {name} felt the warmth of happiness during this {occasion}.",
            "{name}'s heart swelled with happiness, surrounded by friends and family in this moment of {occasion}.",
            "Beneath the clear sky, {name} reveled in the happiness of the {occasion}, creating memories to cherish forever."
        ],
        "everything": "In a world where {fantasy_element} coexists with {real_world_element}, {event} unfolded."
    }

    subjects = ["the castle", "the forest", "the city", "the astronaut", "the dragon", "the abandoned mansion"]
    adjectives = ["ominous", "enchanted", "majestic", "futuristic", "medieval", "desolate"]
    colors = ["vibrant", "pastel", "bold", "subtle", "expressive", "monochromatic"]
    emotions = ["whimsical", "nostalgic", "uplifting", "serene", "ecstatic", "melancholic"]
    characters = ["he", "she", "they", "the mysterious stranger", "the lost soul"]
    names = ["Alice", "Bob", "Ella", "Leo", "Sophia", "Max"]
    occasions = ["birthday", "wedding", "graduation", "celebration", "reunion", "anniversary"]
    fantasy_elements = ["magic", "dragons", "aliens", "mythical creatures", "time travel", "enchanted artifacts"]
    real_world_elements = ["technology", "nature", "history", "science", "culture", "ancient traditions"]
    events = ["an unexpected meeting", "a grand adventure", "a tragic incident", "a joyful celebration", "a mysterious discovery", "a miraculous encounter"]

    subject = random.choice(subjects)
    adjective = random.choice(adjectives)
    color = random.choice(colors)
    emotion = random.choice(emotions)
    character = random.choice(characters)
    name = random.choice(names)
    occasion = random.choice(occasions)
    fantasy_element = random.choice(fantasy_elements)
    real_world_element = random.choice(real_world_elements)
    event = random.choice(events)

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
