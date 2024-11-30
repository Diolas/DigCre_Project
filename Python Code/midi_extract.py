import mido
import time

def extract_midi_features():
    available_ports = mido.get_input_names()
    if not available_ports:
        print("No MIDI input ports found. Please connect a MIDI device.")
        return None

    print("Available MIDI input ports:")
    for i, port in enumerate(available_ports):
        print(f"{i}: {port}")

    port_name = available_ports[0]
    print(f"\nUsing MIDI input port: {port_name}")

    # Capture MIDI data
    notes = []
    velocities = []
    start_time = time.time()
    last_note_time = time.time()
    note_times = []

    with mido.open_input(port_name) as inport:
        print("Listening for MIDI messages. Press Ctrl+C to stop.")
        try:
            for msg in inport:
                if time.time() - last_note_time > 5:
                    print("No activity detected. Stopping MIDI input.")
                    break

                if msg.type == 'note_on' and msg.velocity > 0:
                    last_note_time = time.time()
                    notes.append((msg.note, msg.velocity, last_note_time - start_time))
                    velocities.append(msg.velocity)
                    note_times.append(last_note_time - start_time)
                    print(f"Note ON: {msg.note}, Velocity: {msg.velocity}, Time: {msg.time}")

        except KeyboardInterrupt:
            print("\nStopped listening to MIDI input.")

    # Return captured data for further processing
    return notes

def segment_midi_data(notes, notes_per_section=8):
    sections = []
    current_section = {'notes': [], 'velocity_sum': 0, 'note_times': []}

    for i, (note, velocity, timestamp) in enumerate(notes):
        current_section['notes'].append(note)
        current_section['velocity_sum'] += velocity
        current_section['note_times'].append(timestamp)

        # Check if we've reached the desired section size
        if (i + 1) % notes_per_section == 0 or i == len(notes) - 1:
            # Calculate section features
            pitch_range = (min(current_section['notes']), max(current_section['notes']))
            avg_velocity = current_section['velocity_sum'] / len(current_section['notes'])
            tempo = len(current_section['note_times']) / (current_section['note_times'][-1] - current_section['note_times'][0]) if len(current_section['note_times']) > 1 else 0
            rhythm_complexity = sum(abs(current_section['note_times'][j] - current_section['note_times'][j - 1]) for j in range(1, len(current_section['note_times']))) / len(current_section['note_times']) if len(current_section['note_times']) > 1 else 0

            # Append section data
            sections.append({
                'pitch_range': pitch_range,
                'average_velocity': avg_velocity,
                'tempo': tempo,
                'rhythm_complexity': rhythm_complexity
            })

            # Reset for the next section
            current_section = {'notes': [], 'velocity_sum': 0, 'note_times': []}

    print("\nExtracted Sections Features:")
    for idx, section in enumerate(sections):
        print(f"Section {idx + 1}: {section}")

    return sections

# Running the process
if __name__ == "__main__":
    midi_data = extract_midi_features()
    if midi_data:
        segment_midi_data(midi_data)
