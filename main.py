from midi_extract import extract_midi_features, segment_midi_data
from prompt_generator import generate_prompt
from image_generator import generate_image

def midi_to_images():
    # Step 1: Extract raw MIDI data
    notes = extract_midi_features()
    if notes is None:
        print("No MIDI data captured.")
        return
    
    # Step 2: Segment the data into sections and calculate features
    sections = segment_midi_data(notes)

    # Step 3: Generate prompt and image for each section
    for i, features in enumerate(sections):
        # Generate a prompt based on the section's features
        prompt = generate_prompt(features)
        print(f"Generated prompt for section {i+1}: {prompt}")
        
        # Generate an image for this section with a unique filename
        generate_image(prompt, f"section_{i+1}.png")

if __name__ == "__main__":
    midi_to_images()
