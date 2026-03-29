from pathlib import Path

def get_audio_files(path):
        """
        Return a list of audio files from a file or directory using pathlib.
        """
        AUDIO_EXTENSIONS = (".mp3", ".wav", ".flac", ".m4a")
        p = Path(path)  # Convert input to a Path object

        if p.is_file():
            return [p] if p.suffix.lower() in AUDIO_EXTENSIONS else []

        elif p.is_dir():
            # List all files in the directory matching audio extensions
            files = [f for f in p.iterdir() if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS]
            return files

        else:
            print("Invalid path")
            return []