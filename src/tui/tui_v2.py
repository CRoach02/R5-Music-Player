# Imports
from textual.app import App, ComposeResult
from textual.widgets import Static, Label

class HelloApp(App):
    def compose(self):
        self.static1 = Static("[bold red]Hello world!\n" \
                                "Static widgets fill the size of the screen")
        self.static2 = Static("Test Static")
        yield self.static1
        yield self.static2
        self.label = Label("Test Label\n" \
                            "Label widgets fit the size of the content")
        yield self.label

    def on_mount(self):
        # Controls widget operations upon mounting widget to tui

        # Styling the Static widget
        self.static1.styles.background = "blue"
        self.static1.styles.border = ("solid", "white")
        self.static1.styles.text_align = "center"
        self.static1.styles.padding = 1, 1
        self.static1.styles.margin = 4, 4

        # Styling the Label widget
        self.label.styles.background = "darkgreen"
        self.label.styles.border = ("double", "black")
        self.label.styles.text_align = "right"
        self.label.styles.padding = 1, 1
        self.label.styles.margin = 2, 4

    def on_key(self, event):
        # Handles events like pygame 
        match event.key:
            case "q":
                exit()

if __name__ == "__main__":
    app = HelloApp()
    app.run()