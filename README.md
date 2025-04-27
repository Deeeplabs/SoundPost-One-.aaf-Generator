# Embed WAV into AAF for Pro Tools (Planck MCL SoundPostOne)

This script embeds WAV files into AAF files with proper metadata for Film Post workflows (24fps, 01:00:00:00 start timecode), compatible with Pro Tools.
It is designed to be integrated with the main Planck App for automated sound post-production workflows.

## How to Use

1. Place your .wav files inside the input/ folder.
2. Install the required Python packages (only needed once):
   pip install -r requirements.txt
3. Run the script:
   python app.py
4. The processed .aaf files will be generated into the output/ folder automatically.


## How it Works

- The script automatically finds the latest WAV file in the input/ folder (based on file modified time).
- Only one latest WAV file is processed at a time.
- The output AAF file is named after the WAV file, with today's date appended (for example: Recording_27042025.aaf).


## Key Features

- Timeline frame rate is fixed at 24 fps (standard for Film Post Production).
- Start timecode is 01:00:00:00 to match film sync standards.
- Media is embedded inside the AAF (no external links).
- Audio properties (sample rate, bit depth, channels) are auto-detected from the WAV file.
- Audio is stored as uncompressed PCM and frame-wrapped for full Pro Tools compatibility.
- Simple folder structure: input/ for WAVs, output/ for generated AAFs.


## Important Notes for Users

- Ensure your .wav files are standard uncompressed PCM (e.g., 24-bit, 48kHz) for best compatibility.
- Only the latest modified WAV file in the input/ folder will be processed.
- Multiple WAVs should be processed one-by-one — delete or move old WAVs after processing.
- Generated AAFs will import directly into Pro Tools sessions with correct timecode and audio metadata.
- No manual edit of the AAF file is required after generation.
- This tool is intended to work as part of the Planck MCL SoundPostOne pipeline.


## Folder Structure

/input/    - Place your WAV files here
/output/   - AAF files will be generated here
app.py     - Main script
requirements.txt
README.txt


## License

This tool is part of the Planck MCL SoundPostOne project. Written by Deeeplabs Pte. Ltd.
