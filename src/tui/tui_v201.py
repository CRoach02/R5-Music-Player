# Imports
from textual.app import App, ComposeResult
from textual.widgets import Static, Label
from logic import controller_v1

class DisplayData():
    def createTable():
        ROWS = []
        header = ("#", "Title", "Artist", "Duration")
        content = controller_v1.MediaHandler.get_audio_files()

class MusicApp(App):
    pass