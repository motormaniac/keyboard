import csv
import sqlite3
from pathlib import Path
from typing import Optional

OUTPUT_DB = Path(__file__).with_name("keystroke_table.db")
OUTPUT_CSV = Path(__file__).with_name("keystrokes_export.csv")


def init_db() -> None:
    with sqlite3.connect(OUTPUT_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS keystrokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                dt_seconds REAL,
                hold_seconds REAL
            )
            """
        )

        # Migrate older schemas that enforced NOT NULL on duration columns.
        columns = {
            row[1]: {"type": row[2], "notnull": row[3], "pk": row[5]}
            for row in conn.execute("PRAGMA table_info(keystrokes)")
        }
        needs_rebuild = False
        if "dt_seconds" in columns and columns["dt_seconds"]["notnull"] == 1:
            needs_rebuild = True
        if "hold_seconds" in columns and columns["hold_seconds"]["notnull"] == 1:
            needs_rebuild = True

        if needs_rebuild:
            conn.execute(
                """
                CREATE TABLE keystrokes_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    dt_seconds REAL,
                    hold_seconds REAL
                )
                """
            )
            conn.execute(
                """
                INSERT INTO keystrokes_new (id, key, dt_seconds, hold_seconds)
                SELECT id, key, dt_seconds, hold_seconds
                FROM keystrokes
                """
            )
            conn.execute("DROP TABLE keystrokes")
            conn.execute("ALTER TABLE keystrokes_new RENAME TO keystrokes")
            conn.execute(
                "UPDATE sqlite_sequence SET seq = (SELECT COALESCE(MAX(id), 0) FROM keystrokes) WHERE name = 'keystrokes'"
            )

def append_db_row(
    key_string: str,
    dt_seconds: Optional[float],
    hold_seconds: Optional[float] = None,
) -> int:
    with sqlite3.connect(OUTPUT_DB) as conn:
        cursor = conn.execute(
            "INSERT INTO keystrokes (key, dt_seconds, hold_seconds) VALUES (?, ?, ?)",
            (key_string, dt_seconds, hold_seconds),
        )
        return int(cursor.lastrowid)


def update_hold_seconds(row_id: int, hold_seconds: Optional[float]) -> None:
    with sqlite3.connect(OUTPUT_DB) as conn:
        conn.execute(
            "UPDATE keystrokes SET hold_seconds = ? WHERE id = ?",
            (hold_seconds, row_id),
        )


def export_view_to_csv(csv_path: str | Path) -> Path:
    """Export keystrokes table rows to a CSV file and return its path."""
    out_path = Path(csv_path)
    with sqlite3.connect(OUTPUT_DB) as conn:
        rows = conn.execute(
            "SELECT id, key, dt_seconds, hold_seconds FROM keystrokes ORDER BY id"
        ).fetchall()

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "key", "dt_seconds", "hold_seconds"])
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