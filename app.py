from midiutil import MIDIFile
import ollama
import re

def generate_music_prompt(instruction, style):
    return instruction + style

def extract_chords_and_notes(text):
    chords_pattern = r"chords = \[(.*?)\]"
    notes_pattern = r"notes = \[(.*?)\]"
    chords_match = re.search(chords_pattern, text)
    notes_match = re.search(notes_pattern, text)
    chords = eval('[' + chords_match.group(1) + ']') if chords_match else []
    notes = eval('[' + notes_match.group(1) + ']') if notes_match else []
    return chords, notes

def note_to_midi(note):
    note_mapping = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
        'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }
    octave = int(note[-1])
    pitch = note_mapping[note[:-1]] + (octave + 1) * 12
    return pitch

def chord_to_notes(chord):
    note_mapping = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
        'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }
    chord_intervals = {
        'maj': [0, 4, 7], 'min': [0, 3, 7], '7': [0, 4, 7, 10],
        'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10], 'dim': [0, 3, 6],
        'dim7': [0, 3, 6, 9], 'aug': [0, 4, 8], 'm7b5': [0, 3, 6, 10],
        'sus2': [0, 2, 7], 'sus4': [0, 5, 7], '6': [0, 4, 7, 9],
        'm6': [0, 3, 7, 9], '9': [0, 4, 7, 10, 14], 'maj9': [0, 4, 7, 11, 14],
        'm9': [0, 3, 7, 10, 14], 'add9': [0, 4, 7, 14], 'add2': [0, 2, 4, 7],
        'add4': [0, 4, 5, 7], '11': [0, 4, 7, 10, 14, 17],
        '13': [0, 4, 7, 10, 14, 17, 21]
    }
    root = ''.join([char for char in chord if char.isalpha() or char == '#'])
    chord_type = chord[len(root):]
    if chord_type == '':
        chord_type = 'maj'
    chord_type_mapping = {
        'maj': 'maj', 'maj7': 'maj7', 'm7': 'm7', 'min7': 'm7', '7': '7',
        'm': 'min', 'min': 'min', 'dim': 'dim', 'dim7': 'dim7', 'aug': 'aug',
        'm7b5': 'm7b5', 'sus2': 'sus2', 'sus4': 'sus4', '6': '6', 'm6': 'm6',
        '9': '9', 'maj9': 'maj9', 'm9': 'm9', 'add9': 'add9', 'add2': 'add2',
        'add4': 'add4', '11': '11', '13': '13'
    }
    if chord_type not in chord_type_mapping:
        raise ValueError(f"Unsupported chord type: {chord_type}")
    chord_type = chord_type_mapping[chord_type]
    root_pitch = note_mapping[root]
    pitches = [(root_pitch + interval + 12 * 4) for interval in chord_intervals[chord_type]]
    return pitches

def main():
    Instruction_Prompt = "You are a sophisticated music composer AI. When provided with a musical theme or emotion, your task is to generate a detailed text representation of a musical composition. Please structure your output as follows: 1. Chords should be listed with their name and the time in beats when they are played, 2.Use the format: chords = [('chord name', time in beats)] ,3.Melody notes should be indicated with the note name, octave, and the time in beats. Use the format: notes = [('note name and octave', time in beats)] For example: chords = [('Cmaj7, 0), (Dm7, 2.5), ('Esus', 3), ('Fmaj7#11', 35)] notes = [('C#4', 2.5), ('D4', 3), ('F4', 4)] Your goal is to create expressive, dynamic, and emotionally resonant music. Avoid simple ascending and descending scales or robotic timing. Be creative. Ensure that the melodies are nuanced and suitable for a singer, capturing the essence and depth of the given theme or emotion. Now"
    Actual_prompt = "Make a jazz cinematic sample music"
    prompt = generate_music_prompt(Instruction_Prompt, Actual_prompt)
    response = ollama.chat(model='llama3', messages=[{'role': 'user','content': prompt,}])
    r1 = response['message']['content']
    #print(r1)
    chords, notes = extract_chords_and_notes(r1)
    midi = MIDIFile(1)
    track = 0
    time = 0
    midi.addTrackName(track, time, "Sample Track")
    midi.addTempo(track, time, 120)

    for chord, chord_time in chords:
        chord_notes = chord_to_notes(chord)
        for note in chord_notes:
            midi.addNote(track, 0, note, chord_time, 1, 100)

    for note, note_time in notes:
        midi_note = note_to_midi(note)
        midi.addNote(track, 0, midi_note, note_time, 1, 100)

    with open("output.mid", "wb") as output_file:
        midi.writeFile(output_file)

if __name__ == "__main__":
    main()