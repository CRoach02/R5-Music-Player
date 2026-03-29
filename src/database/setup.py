from pathlib import Path
import sqlite3

def run_setup():
    current_dir = Path(__file__).parent.resolve()

    for entry in current_dir.iterdir():
        if entry.is_file():
            print(f"{entry.name} is a file")
        elif entry.is_dir():
            print(f"{entry.name} is a directory")

    # CALL BELOW needs to be updated when music metadata is determined
    # with sqlite3.connect('music.db') as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS tracks (
    #             id TEXT UNIQUE PRIMARY KEY,
    #             title TEXT,
    #             artist TEXT,
    #             filepath TEXT UNIQUE,
    #             duration INTEGER,
    #             genre TEXT,       
                       
    #                    )
                       
    #                    """)

# music.db rough structure; changes will need to be made
#   based on tracked metadata (mutagen) and feature data (librosa)

#     tracks (
#         id INTEGER PRIMARY KEY,
#         title TEXT,
#         artist TEXT,
#         album TEXT,
#         filepath TEXT UNIQUE,
#         duration INTEGER
#     )

#     playlists (
#         id INTEGER PRIMARY KEY,
#         name TEXT UNIQUE
#     )

#     playlist_tracks (
#         playlist_id INTEGER,
#         track_id INTEGER,
#         position INTEGER,
#         PRIMARY KEY (playlist_id, track_id),
#         FOREIGN KEY (playlist_id) REFERENCES playlists(id),
#         FOREIGN KEY (track_id) REFERENCES tracks(id)
#     )