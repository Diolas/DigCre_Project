import mido

def save_midi(notes, filename="captured_midi.mid"):
    """Save raw MIDI data to a file."""
    # Create a new MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Add MIDI events to the track
    for note in notes:
        # Assume `note` is a dictionary with 'note', 'velocity', 'start_time', 'duration'
        start_time = int(note['start_time'] * 480)  # Convert seconds to ticks (assuming 480 ticks per beat)
        duration = int(note['duration'] * 480)
        
        # Add note on and note off events
        track.append(mido.Message('note_on', note=note['note'], velocity=note['velocity'], time=start_time))
        track.append(mido.Message('note_off', note=note['note'], velocity=0, time=start_time + duration))
    
    # Save the MIDI file
    mid.save(filename)
    print(f"MIDI data saved to {filename}")

def replay_midi(filename="captured_midi.mid"):
    """Replay a saved MIDI file."""
    try:
        mid = mido.MidiFile(filename)
        for msg in mid.play():
            print(msg)  # Send this message to a MIDI output device for actual playback
    except FileNotFoundError:
        print(f"MIDI file {filename} not found!")
