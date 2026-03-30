# src/tui/tui_v201.py
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button
from textual.containers import Horizontal
from src.player.player_v2 import async_player
from src.player.player import get_audio_files
from src.media import reader
from pathlib import Path
import sys
import asyncio

class DisplayData:
    def __init__(self):
        self.content = []

    def load_content(self, path: str):
        self.content = reader.get_audio_files(path)

    def create_table_rows(self):
        rows = [("#", "Title", "Artist", "Duration", "Location")]
        for idx, f in enumerate(self.content):
            rows.append((
                idx,
                Path(f).name,
                f"Dummy Artist {idx+1}",
                "2:00",
                Path(f).resolve().parent
            ))
        return rows

class MusicApp(App):
    def __init__(self, data: DisplayData):
        super().__init__()
        self.data = data
        self.current_task = None  # Tracks the async playback task

    def compose(self) -> ComposeResult:
        yield DataTable(id="music_table")

    def on_mount(self) -> None:
        table = self.query_one("#music_table", DataTable)
        rows = self.data.create_table_rows()
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])
        table.cursor_type = "row"

    async def on_key(self, event):
        table = self.query_one("#music_table", DataTable)
        row_index = table.cursor_row

        match event.key:
            case "enter":
                if row_index is None:
                    return

                file_path = self.data.content[row_index]

                # Stop current song if playing
                if self.current_task and not self.current_task.done():
                    self.current_task.cancel()
                    try:
                        await self.current_task
                    except asyncio.CancelledError:
                        print("Previous song stopped.")

                # Start new song
                self.current_task = asyncio.create_task(
                    async_player.play_files_async([file_path])
                )

            case "s":  # Stop the current song
                if self.current_task and not self.current_task.done():
                    self.current_task.cancel()
                    try:
                        await self.current_task
                    except asyncio.CancelledError:
                        print("Song stopped by user.")
                else:
                    async_player.stop()  # In case task already finished

            case "q":
                # Quit the app
                if self.current_task and not self.current_task.done():
                    self.current_task.cancel()
                exit()

    
def main():
    data = DisplayData()
    data.load_content(sys.argv[1])
    app = MusicApp(data)
    app.run()


if __name__ == "__main__":
    main()