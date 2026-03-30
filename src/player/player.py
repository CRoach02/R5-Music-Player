import vlc
import os
import time
from pathlib import Path
import asyncio

class AsyncPlayer:
     def __inti__(self):
          self.player = None

async def play_files_async(self, file_list):
    """Play a list of audio files sequentially."""
    for file in file_list:
        
        filename = Path(file).name  # Gets the raw file name, removing the directory path
        print(f"Now playing: {filename}")

        self.player = vlc.MediaPlayer(str(file))
        self.player.play()

        await asyncio.sleep(0.1)
        try:
            while self.player.is_playing():
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
             self.player.stop()
             raise
        
        self.player = None

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
        
async_player = AsyncPlayer()