import sys
sys.path.append(".")

import tkinter as tk
from pysrc import keymap

square_size = 50
padding = 10
offset = padding

root = tk.Tk()
root.geometry("600x400")
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.place(x=0, y=0)


def grid_to_real(y:int, x:int) -> tuple[int, int]:
    real_x = offset + (x) * (square_size + padding) + square_size//2
    real_y = offset + (4-y) * (square_size + padding) + square_size//2
    return (real_x, real_y)

def draw_rect(x:int, y:int) -> None:
    canvas.create_rectangle(x-square_size*0.5, y-square_size*0.5,
        x+square_size*0.5, y+square_size*0.5)

from colorsys import hsv_to_rgb

def hsb_to_hex(h:float, s:float, b:float) -> str:
    """
    h, s, b are in range 0–1
    returns HEX string like "#AABBCC"
    """
    r, g, b = hsv_to_rgb(h, s, b)
    return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))

class KeyDisplay:
    def __init__(self, keycode:str) -> None:
        self.keycode = keycode
        
    def draw(self) -> None:
        real_x, real_y = self.get_real_pos()
        draw_rect(real_x, real_y)
        canvas.create_text(real_x, real_y, text=self.keycode)
    def get_pos(self) -> tuple[int, int]:
        row = int(self.keycode[0])
        col = int(self.keycode[1])
        return (row, col)
    def get_real_pos(self) -> tuple[int, int]:
        row, col = self.get_pos()
        return grid_to_real(row, col)
    def check_hover(self, mouse_x:int, mouse_y:int) -> bool:
        real_x, real_y = self.get_real_pos()
        if (real_x - square_size*0.5 <= mouse_x <= real_x + square_size*0.5) and \
           (real_y - square_size*0.5 <= mouse_y <= real_y + square_size*0.5):
            return True

def draw_weight(key1:KeyDisplay, key2:KeyDisplay, show_text:bool = False) -> None:
    weight = keymap.calc_key_distance(key1.keycode, key2.keycode)
    fill_color = hsb_to_hex(0, 1.0, keymap.normalize_distance(weight))
    key1_x, key1_y = key1.get_real_pos()
    key2_x, key2_y = key2.get_real_pos()
    canvas.create_line(*key1.get_real_pos(), *key2.get_real_pos(),fill=fill_color, width=2)
    if show_text:
        # write the weight number in text at the midpoint
        canvas.create_text((key1_x + key2_x)//2, (key1_y + key2_y)//2, text=str(weight), fill="black")

key_display_list: list[KeyDisplay] = []

for key in keymap.key_list:
    if key[2] == "1":
        continue
    key_display = KeyDisplay(key)
    key_display.draw()
    key_display_list.append(key_display)

def draw_all_weights() -> None:
    for i, key1 in enumerate(key_display_list):
        for i, key2 in enumerate(key_display_list, i):
            draw_weight(key1, key2)

def update_loop(delay:int = 1000) -> None:
    global key_display_list
    canvas.delete("all")
    target_key = key_display_list[0]
    for key in key_display_list:
        key.draw()

    for key in key_display_list:
        if key.keycode == target_key.keycode:
            continue
        draw_weight(target_key, key)
    
    # rotate the list
    key_display_list = key_display_list[1:] + [key_display_list[0]]
    
    root.after(delay, lambda: update_loop(delay))

# draw_all_weights()
update_loop()

root.mainloop()
