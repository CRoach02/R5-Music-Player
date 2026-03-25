import subprocess
import vlc
import time
import os
import sys


def setup_audio_env():
    """Ensure audio works over SSH."""
    os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"


def get_bluetooth_sink():
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


def set_audio_sink(sink):
    """Set the default audio sink."""
    subprocess.run(["pactl", "set-default-sink", sink])


def get_audio_files(path):
    """Return a list of audio files from a file or directory."""
    AUDIO_EXTENSIONS = (".mp3", ".wav", ".flac", ".m4a")

    if os.path.isfile(path):
        return [path]

    elif os.path.isdir(path):
        files = []
        for file in os.listdir(path):
            if file.lower().endswith(AUDIO_EXTENSIONS):
                files.append(os.path.join(path, file))
        return sorted(files)

    else:
        print("Invalid path")
        return []


def play_files(file_list):
    """Play a list of audio files sequentially."""
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

    setup_audio_env()

    sink = get_bluetooth_sink()
    if sink:
        set_audio_sink(sink)
    else:
        print("No Bluetooth sink found")

    path = sys.argv[1]
    files = get_audio_files(path)

    if files:
        play_files(files)
    else:
        print("No audio files found")


# yt-dlp usage:
# yt-dlp -x --audio-format mp3 --js-runtimes node --sleep-interval 2 --max-sleep-interval 5 "youtube link"

if __name__ == "__main__":
    main()