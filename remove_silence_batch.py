import os
import argparse
from pydub import AudioSegment, silence

def remove_silence_from_file(
    input_path, output_path,
    min_silence_len=500,
    silence_thresh=-40,
    keep_silence=100
):
    """
    Removes silence from a single WAV file and saves the output.
    
    Args:
        input_path (str): Path to the input .wav file.
        output_path (str): Path to save the output .wav file.
        min_silence_len (int): Minimum length (ms) of silence to detect.
        silence_thresh (float): Silence threshold in dBFS.
        keep_silence (int): Duration (ms) of silence to retain before/after non-silent segments.
    """
    audio = AudioSegment.from_wav(input_path)

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
    parser = argparse.ArgumentParser(description="""
    Batch remove silence from WAV files in a directory.
    
    Example:
        python remove_silence_batch.py --dir_to_remove ./input --output_dir ./output --min_silence_len 500 --silence_thresh -40 --keep_silence 100
    """)
    parser.add_argument("--dir_to_remove", required=True, help="Directory containing input .wav files.")
    parser.add_argument("--output_dir", required=True, help="Directory to save output .wav files.")
    parser.add_argument("--min_silence_len", type=int, default=500, help="Minimum silence length (ms) to consider.")
    parser.add_argument("--silence_thresh", type=float, default=-40.0, help="Silence threshold in dBFS.")
    parser.add_argument("--keep_silence", type=int, default=100, help="Milliseconds of silence to keep before/after speech.")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    for fname in os.listdir(args.dir_to_remove):
        if fname.lower().endswith(".wav"):
            input_path = os.path.join(args.dir_to_remove, fname)
            output_path = os.path.join(args.output_dir, fname)

            remove_silence_from_file(
                input_path,
                output_path,
                min_silence_len=args.min_silence_len,
                silence_thresh=args.silence_thresh,
                keep_silence=args.keep_silence
            )

if __name__ == "__main__":
    main()
