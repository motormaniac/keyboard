from pathlib import Path
import sqlite3

PATH_TO_DB = Path.Path(__file__).with_name("keystroke_table.db")

with sqlite3.connect(PATH_TO_DB) as conn:
  cur = conn.cursor()
  cur.execute("SELECT id, key, press_ts, release_ts FROM keystrokes ORDER")
  