import os
import argparse
from pydub import AudioSegment, silence

def remove_silence_from_file(input_path, output_path, min_silence_len=500, silence_thresh_offset=14, keep_silence=100):
    audio = AudioSegment.from_wav(input_path)
    silence_thresh = audio.dBFS - silence_thresh_offset

    nonsilent_chunks = silence.split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )

    if not nonsilent_chunks:
        print(f"[Skipped] No non-silent chunks detected in {input_path}")
        return

    processed_audio = AudioSegment.empty()
    for chunk in nonsilent_chunks:
        processed_audio += chunk

    processed_audio.export(output_path, format="wav")
    print(f"[Done] Processed: {os.path.basename(input_path)}")


def main():
    parser = argparse.ArgumentParser(description="Remove silence from WAV files in a directory.")
    parser.add_argument("--dir_to_remove", required=True, help="Directory containing input .wav files.")
    parser.add_argument("--output_dir", required=True, help="Directory to save output .wav files.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for fname in os.listdir(args.dir_to_remove):
        if fname.lower().endswith(".wav"):
            input_path = os.path.join(args.dir_to_remove, fname)
            output_path = os.path.join(args.output_dir, fname)
            remove_silence_from_file(input_path, output_path)

if __name__ == "__main__":
    main()
