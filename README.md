# Embed WAV into AAF for Pro Tools (Planck  MCL SoundPostOne)

This script embeds WAV files into AAF files with proper metadata for Film Post workflows (24fps, 01:00:00:00 start timecode), compatible with Pro Tools. To be integrated with the mainPlanck App

## How to Use

1. Place your `.wav` files into the `input/` folder.
2. Install the required Python package: pip install -r requirements.txt
3. Run the script: python main.py
4. The AAF files will be generated into the `output/` folder.

## Notes
- Timeline frame rate is fixed at **24fps**.
- Start timecode is **01:00:00:00** (standard for film).
- Media is **embedded** (not linked).
- AAF filenames are automatically generated based on WAV name and date.

Built by Randy, Deeeplabs Pte. Ltd.
