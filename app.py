import os
import wave
import datetime
import aaf2

# Configuration
input_folder = "input"
output_folder = "output"

# Find WAV files in input folder
wav_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".wav")]

if not wav_files:
    raise FileNotFoundError("❌ No WAV files found in 'input/' folder.")

for wav_filename in wav_files:
    input_wav_path = os.path.join(input_folder, wav_filename)

    # 1. Extract WAV properties
    with wave.open(input_wav_path, "rb") as wav_file:
        channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        sample_width = wav_file.getsampwidth()
        bit_depth = sample_width * 8
        num_samples = wav_file.getnframes()
        duration_seconds = num_samples / sample_rate

    # 2. Prepare AAF output filename
    base_name = os.path.splitext(wav_filename)[0]
    today = datetime.datetime.now().strftime("%d%m%Y")
    output_aaf_name = f"{base_name}_{today}.aaf"
    output_aaf_path = os.path.join(output_folder, output_aaf_name)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # 3. AAF Parameters
    edit_rate = 24  # 24 fps
    start_timecode_frame = edit_rate * 60 * 60  # 01:00:00:00 = 86400 frames at 24 fps

    # 4. Create AAF file
    with aaf2.open(output_aaf_path, "w") as f:
        # Create MasterMob (audio clip)
        master_mob = f.create.MasterMob(name=base_name)
        f.content.mobs.append(master_mob)

        # Embed the WAV essence
        essence_slot = master_mob.import_audio_essence(input_wav_path, sample_rate)
        essence_slot['PhysicalTrackNumber'].value = 1

        # Create CompositionMob (timeline)
        comp_mob = f.create.CompositionMob(name=f"{base_name}_Timeline")
        f.content.mobs.append(comp_mob)

        # Create sound track
        timeline_slot = comp_mob.create_sound_slot(edit_rate=edit_rate)
        timeline_slot.name = "Audio Track 1"
        timeline_slot.origin = start_timecode_frame  # start at 01:00:00:00

        # Add SourceClip
        sequence = timeline_slot.segment
        source_clip = master_mob.create_source_clip(
            slot_id=essence_slot.slot_id,
            length=essence_slot.segment.length
        )
        sequence.components.append(source_clip)

    print(f"✅ Generated: {output_aaf_path}")
