# Imports
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from src.player.player import AsyncPlayer, get_audio_files
from src.media import reader
from pathlib import Path
import sys
import asyncio

class DisplayData():
    def __init__(self):
        self.path = None
        self.content = None
        self.root_path = None

    def loadContent(self, path: str) -> None:
        self.path = path
        self.content = reader.get_audio_files(path)

    def createTable(self) -> list:
        ROWS = [("#", "Title", "Artist", "Duration", "Location")]
        # header = ("#", "Title", "Artist", "Duration")
        for idx, f in enumerate(self.content):
            ROWS.append((idx, 
                         Path(f).name, 
                         f"Dummy Artist {idx+1}", 
                         "2:00",
                         Path(f).resolve().parent))
        return ROWS

class MusicApp(App):
    def __init__(self, data: DisplayData):
        super().__init__()
        self.data = data
        self.current_task = None

    async def play_song(self, file_path):
        # stop existing song if any
        if self.current_task and not self.current_task.done():
            self.current_task.cancel()
            try:
                await asyncio.sleep(0) # allow cancellation
            except asyncio.CancelledError:
                print("Previous song cancelled.")

        self.current_task = asyncio.create_task(player.play_files_async([file_path]))
        await self.current_task

    def compose(self) -> ComposeResult:
        yield DataTable(id="music_table")

    def on_mount(self) -> None:
        table = self.query_one("#music_table", DataTable)
        rows = self.data.createTable()
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])
        table.cursor_type = "row"

    async def on_key(self, event):
        
        match event.key:
            case "enter":
                table = self.query_one("#music_table")
                row_index = table.cursor_row
                if row_index is not None:
                    file_path = self.data.content[row_index]

                    # Use the persistent async player instance
                    if self.current_task and not self.current_task.done():
                        self.current_task.cancel()
                        try:
                            await self.current_task
                        except asyncio.CancelledError:
                            print("Previous song cancelled.")

                    # Start new song async
                    self.current_task = asyncio.create_task(
                        # self.async_player.play_files_async([file_path])
                        async_player.play_files_async()
                    )
            case "q":
                exit()


def main():
    data = DisplayData()
    data.loadContent(sys.argv[1])
    app = MusicApp(data)
    app.run()

if __name__ == "__main__":
    main()