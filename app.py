import os
import wave
import math
import aaf2
from fractions import Fraction

# Configure input and output directories
input_folder = "input"
output_folder = "output"

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define the start timecode and frame rate for the Composition timeline
start_timecode_hours = 1  # 01:00:00:00 start
composition_fps = 24      # 24 fps timecode

for filename in os.listdir(input_folder):
    if not filename.lower().endswith(".wav"):
        continue  # skip non-WAV files
    input_path = os.path.join(input_folder, filename)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(output_folder, base_name + ".aaf")

    # Open the WAV file to read audio properties
    with wave.open(input_path, 'rb') as wav_file:
        channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        sample_width = wav_file.getsampwidth()  # in bytes per sample
        bit_depth = sample_width * 8
        num_frames = wav_file.getnframes()

    # Create a new AAF file and embed the WAV audio
    with aaf2.open(output_path, 'w') as f:
        # Create a Master Mob for the audio clip
        master_mob = f.create.MasterMob()
        master_mob.name = base_name
        f.content.mobs.append(master_mob)

        # Import the WAV as embedded audio
        master_slot = master_mob.import_audio_essence(input_path, composition_fps)

        # Find the associated SourceMob
        source_mob = None
        for mob in f.content.mobs:
            if mob is not master_mob and isinstance(mob, aaf2.mobs.SourceMob):
                source_mob = mob
                break

        # Safely access the descriptor
        desc = getattr(source_mob, "descriptor", None) if source_mob else None

        if desc:
            props = desc.properties()

            # Set Sample Rate
            if 'AudioSamplingRate' in props:
                props['AudioSamplingRate'].value = Fraction(sample_rate, 1)
            elif 'SampleRate' in props:
                props['SampleRate'].value = Fraction(sample_rate, 1)

            # Set Bit Depth
            if 'QuantizationBits' in props:
                props['QuantizationBits'].value = bit_depth

            # Set Channel Count
            if 'Channels' in props:
                props['Channels'].value = channels

            # Explicitly set Essence Compression to PCM
            if 'EssenceCompression' in props:
                try:
                    pcm_def = f.dictionary.lookup_codec_def("PCM")
                    props['EssenceCompression'].value = pcm_def.auid
                except Exception:
                    pass  # Safe to skip if lookup fails

            # Ensure frame-wrapped container format
            if 'ContainerFormat' in props:
                try:
                    container_def = f.dictionary.lookup_containerdef("AAF")
                    props['ContainerFormat'].value = container_def.auid
                except Exception:
                    pass

        # Create Composition Mob
        comp_mob = f.create.CompositionMob()
        comp_mob.name = f"{base_name}_Composition"
        comp_mob.usage = "Usage_TopLevel"
        f.content.mobs.append(comp_mob)

        # Create and add Timecode Track
        tc_slot = comp_mob.create_empty_sequence_slot(edit_rate=composition_fps, media_kind='timecode')

        tc_component = f.create.Timecode()
        tc_component.start = start_timecode_hours * 60 * 60 * composition_fps  # 86400 frames (1 hour at 24fps)
        tc_component.length = math.ceil(num_frames * composition_fps / sample_rate)

        tc_slot.segment.components.append(tc_component)

        # Create and add Audio Track
        audio_slot = comp_mob.create_sound_slot(edit_rate=composition_fps)
        comp_audio_clip = master_mob.create_source_clip(
            slot_id=master_slot.slot_id,
            length=master_slot.segment.length
        )
        audio_slot.segment = comp_audio_clip

    print(f"✅ Created AAF: {output_path}")
