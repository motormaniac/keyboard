import time
from typing import Optional

from pynput import keyboard
from keystroke_db import OUTPUT_DB, append_db_row, init_db, update_hold_seconds


IDLE_RESET_SECONDS = 1.0 # if the person doesn't type for this long, reset the timer to 0 for the next keypress
DEBUG = True

last_key_time: float | None = None
pressed_modifiers: set[str] = set()
active_presses: dict[str, tuple[float, int]] = {}


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
    global last_key_time

    try:
        update_modifier_state_on_press(key)

        token = key_token(key)
        # Ignore key-repeat press events while key is still held down.
        if token in active_presses:
            return None

        now = time.perf_counter()
        if last_key_time is None:
            delta: Optional[float] = None
        else:
            elapsed = now - last_key_time
            delta = None if elapsed > IDLE_RESET_SECONDS else elapsed

        key_string = normalize_key(key)
        row_id = append_db_row(key_string, delta, None)
        active_presses[token] = (now, row_id)
        if DEBUG:
            dt_display = "null" if delta is None else f"{delta:.6f}"
            print(f"{key_string:>12} | dt={dt_display} | hold=null")

        last_key_time = now

        # Quit when Ctrl+Shift+Alt+F12 is pressed.
        if (
            key == keyboard.Key.f12
            and "ctrl" in pressed_modifiers
            and "shift" in pressed_modifiers
            and "alt" in pressed_modifiers
        ):
            print("Ctrl+Shift+Alt+F12 detected. Stopping listener.")
            return False

        return None
    except Exception as e:
        print(f"Error processing key press: {e}")

def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
    try:
        token = key_token(key)
        press_info = active_presses.pop(token, None)
        if press_info is not None:
            press_time, row_id = press_info
            hold_seconds = max(0.0, time.perf_counter() - press_time)
            update_hold_seconds(row_id, hold_seconds)
            if DEBUG:
                key_string = normalize_key(key)
                print(f"{key_string:>12} | hold={hold_seconds:.6f}")

        update_modifier_state_on_release(key)
    except Exception as e:
        print(f"Error processing key release: {e}")


def main() -> None:
    init_db()
    print("Listening for key presses. Press Ctrl+Shift+Alt+F12 to quit.")
    print(f"Saving table to: {OUTPUT_DB} (table: keystrokes)")
    if DEBUG:
        print("Columns: key, dt_seconds, hold_seconds")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
