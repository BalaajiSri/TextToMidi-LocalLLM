# Chords-Notes MIDI Generator

## Overview
This project is designed to generate MIDI files based on textual descriptions of musical compositions. It uses a sophisticated AI model to interpret musical themes or emotions and outputs detailed text representations of musical compositions, including chords and melody notes.

## Features
- **Text to Music Conversion**: Converts detailed text descriptions into structured musical data.
- **MIDI File Creation**: Generates MIDI files for both chords and melody notes.
- **Customizable Music Styles**: Supports customization of music styles through text prompts.

## Requirements
- Python 3.x
- midiutil
- ollama 
- re (Regular Expression module)

## Setup
1. Clone the repository:
    git clone "https://github.com/BalaajiSri/TextToMidi-LocalLLM.git"
2. Install the required Python packages:
    pip install midiutil ollama
3. Serve Ollama (pull LLAMA3 from the website).

## Usage
1. Run the Jupyter Notebook `Chords-Notes(MIDI)-generator.ipynb`.
2. Modify the `Actual_prompt` in the notebook to change the style or theme of the music.
3. Execute the notebook cells to generate the MIDI files.

## Files
- **Chords-Notes(MIDI)-generator.ipynb**: Main notebook containing the logic for generating MIDI files.
- **notes.mid**: MIDI file containing the melody notes. (Will be generated once we run all the cells)
- **chords.mid**: MIDI file containing the chords. (Will be generated once we run all the cells)

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
