# src/player/player.py
import vlc
import asyncio
from pathlib import Path

class AsyncPlayer:
    """Simple async VLC player."""

    def __init__(self):
        self.current_player = None

    async def play_files_async(self, file_list):
        """Play files asynchronously. Cancelling stops playback immediately."""
        for file in file_list:
            filename = Path(file).name
            print(f"Now playing: {filename}")

            # Stop previous player if any
            if self.current_player and self.current_player.is_playing():
                self.current_player.stop()

            # Start new player
            self.current_player = vlc.MediaPlayer(str(file))
            self.current_player.play()

            try:
                while self.current_player.is_playing():
                    await asyncio.sleep(0)
            except asyncio.CancelledError:
                if self.current_player:
                    self.current_player.stop()
                raise

    def stop(self):
        """Stop playback immediately."""
        if self.current_player and self.current_player.is_playing():
            self.current_player.stop()

async_player = AsyncPlayer()