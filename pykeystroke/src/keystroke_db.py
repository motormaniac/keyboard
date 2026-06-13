import csv
import sqlite3
from pathlib import Path

OUTPUT_DB = Path(__file__).with_name("keystroke_table.db")
OUTPUT_CSV = Path(__file__).with_name("keystroke_table.csv")


def init_db() -> None:
    with sqlite3.connect(OUTPUT_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS keystrokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                press_ts REAL NOT NULL,
                release_ts REAL
            )
            """
        )


def append_db_row(key_string: str, press_ts: float, release_ts: float | None = None) -> int:
    with sqlite3.connect(OUTPUT_DB) as conn:
        cursor = conn.execute(
            "INSERT INTO keystrokes (key, press_ts, release_ts) VALUES (?, ?, ?)",
            (key_string, press_ts, release_ts),
        )
        return int(cursor.lastrowid)


def update_release_ts(row_id: int, release_ts: float | None) -> None:
    with sqlite3.connect(OUTPUT_DB) as conn:
        conn.execute(
            "UPDATE keystrokes SET release_ts = ? WHERE id = ?",
            (release_ts, row_id),
        )


def export_view_to_csv(csv_path: str | Path) -> Path:
    """Export keystrokes table rows to a CSV file and return its path."""
    out_path = Path(csv_path)
    with sqlite3.connect(OUTPUT_DB) as conn:
        rows = conn.execute(
            "SELECT id, key, press_ts, release_ts FROM keystrokes ORDER BY id"
        ).fetchall()

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "key", "press_ts", "release_ts"])
        writer.writerows(rows)

    return out_path


def reset_database() -> None:
    """Clear all keystroke rows and reset id numbering."""
    with sqlite3.connect(OUTPUT_DB) as conn:
        conn.execute("DELETE FROM keystrokes")
        conn.execute("DELETE FROM sqlite_sequence WHERE name = 'keystrokes'")


def main() -> None:
    init_db()
    while True:
        command = input("Enter command ('reset', 'export', or 'exit'): ").strip().lower()

        if command == "reset":
            confirm = input("This will clear all keystroke data and reset the database. Type 'yes' to confirm: ")
            if confirm == "yes":
                reset_database()
                print("Database reset complete.")
            continue

        if command == "export":
            out_path_input = input(
                f"Enter output CSV path (leave blank for default: {OUTPUT_CSV}): "
            ).strip()
            out_path = Path(out_path_input) if out_path_input else OUTPUT_CSV
            exported = export_view_to_csv(out_path)
            print(f"Exported CSV to: {exported}")
            continue
        
        if command == "exit":
            print("Exiting.")
            return

        print(f"Unknown command: {command}")
        print("Valid commands: reset, export, exit")

if __name__ == "__main__":
    main()