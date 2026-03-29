import subprocess
import vlc
import time
import os
import sys
from pathlib import Path

class EnvControl():
    def setup_audio_env() -> None:
        """Ensure audio works over SSH."""
        os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"


    def get_bluetooth_sink() -> None:
        """Find the first available Bluetooth audio sink."""
        result = subprocess.run(
            ["pactl", "list", "short", "sinks"],
            capture_output=True,
            text=True
        )

        for line in result.stdout.splitlines():
            if "bluez_output" in line:
                return line.split()[1]

        return None


    def set_audio_sink(sink) -> None:
        """Set the default audio sink."""
        subprocess.run(["pactl", "set-default-sink", sink])



class MediaHandler():
    def get_audio_files(path):
        """
        Return a list of audio files from a file or directory.
        
        **Needs to be refactored to make better use of Path objects
            instead of os.path strings.
        """
        AUDIO_EXTENSIONS = (".mp3", ".wav", ".flac", ".m4a")

        if os.path.isfile(path):
            return [path]

        elif os.path.isdir(path):
            # Creates list of files in directory
            files = []
            for file in os.listdir(path):
                if file.lower().endswith(AUDIO_EXTENSIONS):
                    files.append(os.path.join(path, file))
            return sorted(files)

        else:
            print("Invalid path")
            return []

    def get_audio_files2(path):
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
            return sorted(files)

        else:
            print("Invalid path")
            return []

    def play_files(file_list):
        """Play a list of audio files sequentially."""

        if not file_list:
            raise Exception("File list is empty.") 
        
        for file in file_list:
            print(f"Now playing: {file}")

            player = vlc.MediaPlayer(file)
            player.play()

            time.sleep(1)
            while player.is_playing():
                time.sleep(1)


    

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 v1.py <file_or_directory>")
        sys.exit(1)

    EnvControl.setup_audio_env()

    sink = EnvControl.get_bluetooth_sink()
    if sink:
        EnvControl.set_audio_sink(sink)
    else:
        print("No Bluetooth sink found")

    path = sys.argv[1] # Gets the path (first argument) declared when running the file
    files = MediaHandler.get_audio_files2(path)

    if files:
        MediaHandler.play_files(files)
    else:
        print("No audio files found")
    filenames = [Path(f).name for f in files] # Gets the raw file name, removing the directory path
    print(filenames)

if __name__ == "__main__":
    main()
