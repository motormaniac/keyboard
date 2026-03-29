import time

from pynput import keyboard
from winotify import Notification
from keystroke_db import OUTPUT_DB, append_db_row, init_db, update_release_ts


Debug = True

pressed_modifiers: set[str] = set()
active_presses: dict[str, int] = {}


def notify_canceled(reason: str) -> None:
    """Send a Windows toast when the logger is canceled."""
    try:
        toast = Notification(
            app_id="Keystroke Logger",
            title="Keystroke Logger Stopped",
            msg=f"Canceled: {reason}",
            duration="short",
        )
        toast.show()
    except Exception as e:
        print(f"Unable to send Windows notification: {e}")

def notify_started() -> None:
    """Send a Windows toast when the logger starts."""
    try:
        toast = Notification(
            app_id="Keystroke Logger",
            title="Keystroke Logger Started",
            msg="Press Ctrl+Shift+Alt+F12 to stop.",
            duration="short",
        )
        toast.show()
    except Exception as e:
        print(f"Unable to send Windows notification: {e}")

def key_token(key: keyboard.Key | keyboard.KeyCode) -> str:
    """Build a stable token so press/release for the same key can be matched.

    Prefer physical/location-oriented identity (scan code), then vk.
    """
    if isinstance(key, keyboard.KeyCode):
        scan = getattr(key, "scan", None)
        if scan is not None:
            return f"sc:{scan}"

        vk = getattr(key, "vk", None)
        if vk is not None:
            return f"vk:{vk}"

        return f"kc:{str(key)}"

    return f"k:{str(key)}"


def normalize_key(key: keyboard.Key | keyboard.KeyCode) -> str:
    # Keycodes
    if isinstance(key, keyboard.KeyCode):
        char = key.char
        if char is None:
            name = str(key)
            if name.startswith("KeyCode"):
                return name[8:].lower()  # Remove "KeyCode(" prefix
            return name.lower()

        # Control combinations can appear as non-printable bytes.
        if "ctrl" in pressed_modifiers and len(char) == 1 and ord(char) < 32:
            mapped = chr(ord(char) + 64)
            return mapped.lower()
        if char == "\n" or char == "\r":
            return "enter"
        if char == "\t":
            return "tab"
        if char.isprintable():
            return char.lower()
        return f"U+{ord(char):04X}"

    # Non keycode keys
    if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        return "ctrl"
    if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        return "shift"
    if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr):
        return "alt"
    if key == keyboard.Key.cmd:
        return "cmd"

    name = str(key)
    if name.startswith("Key."):
        return name[4:].lower()
    return name.lower()


def update_modifier_state_on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
    if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        pressed_modifiers.add("ctrl")
    elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        pressed_modifiers.add("shift")
    elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr):
        pressed_modifiers.add("alt")
    elif key == keyboard.Key.cmd:
        pressed_modifiers.add("cmd")


def update_modifier_state_on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
    if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        pressed_modifiers.discard("ctrl")
    elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        pressed_modifiers.discard("shift")
    elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr):
        pressed_modifiers.discard("alt")
    elif key == keyboard.Key.cmd:
        pressed_modifiers.discard("cmd")


def on_press(key: keyboard.Key | keyboard.KeyCode) -> bool | None:
    try:
        update_modifier_state_on_press(key)

        token = key_token(key)
        # Ignore key-repeat press events while key is still held down.
        if token in active_presses:
            return None

        press_ts = time.time()

        key_string = normalize_key(key)
        row_id = append_db_row(key_string, press_ts, None)
        active_presses[token] = row_id
        if Debug:
            print(f"{key_string:>12} | press_ts={press_ts:.6f} | release_ts=null")

        # Quit when Ctrl+Shift+Alt+F12 is pressed.
        if (
            key == keyboard.Key.f12
            and "ctrl" in pressed_modifiers
            and "shift" in pressed_modifiers
            and "alt" in pressed_modifiers
        ):
            print("Ctrl+Shift+Alt+F12 detected. Stopping listener.")
            notify_canceled("Ctrl+Shift+Alt+F12")
            return False

        return None
    except Exception as e:
        print(f"Error processing key press: {e}")

def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
    try:
        token = key_token(key)
        row_id = active_presses.pop(token, None)
        if row_id is not None:
            release_ts = time.time()
            update_release_ts(row_id, release_ts)
            if Debug:
                key_string = normalize_key(key)
                print(f"{key_string:>12} | release_ts={release_ts:.6f}")

        update_modifier_state_on_release(key)
    except Exception as e:
        print(f"Error processing key release: {e}")


def main(debug: bool = True) -> None:
    global Debug
    Debug = debug
    init_db()
    notify_started()
    print("Listening for key presses. Press Ctrl+Shift+Alt+F12 to quit.")
    if Debug:
        print(f"Saving table to: {OUTPUT_DB} (table: keystrokes)")
        print("Columns: key, press_ts, release_ts")
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        notify_canceled("KeyboardInterrupt")
        print("Keystroke logger interrupted.")

if __name__ == "__main__":
    main(debug=True)
