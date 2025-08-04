import time
from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from threading import Thread

keyboard_controller = KeyboardController()
mouse_controller = MouseController()

# Global flag
running = False

# Map input strings to keys
def get_input_key(key_str):
    key_str = key_str.lower()
    
    # Mouse support
    if key_str in ['left', 'right', 'middle']:
        return getattr(Button, key_str)

    # Arrow keys and special keys
    special_keys = {
        'space': Key.space,
        'enter': Key.enter,
        'tab': Key.tab,
        'esc': Key.esc,
        'shift': Key.shift,
        'ctrl': Key.ctrl,
        'alt': Key.alt,
        'up': Key.up,
        'down': Key.down,
        'left_arrow': Key.left,
        'right_arrow': Key.right,
        'left': Key.left,
        'right': Key.right,
        'f1': Key.f1,
        'f2': Key.f2,
        'f3': Key.f3,
        'f4': Key.f4,
        'f5': Key.f5,
        'f6': Key.f6,
        'f7': Key.f7,
        'f8': Key.f8,
        'f9': Key.f9,
        'f10': Key.f10,
    }

    return special_keys.get(key_str, key_str)  # Default to literal key if not special

# Simulate press and release
def hold_input(input_key, duration):
    if isinstance(input_key, Button):
        mouse_controller.press(input_key)
        time.sleep(duration)
        mouse_controller.release(input_key)
    else:
        keyboard_controller.press(input_key)
        time.sleep(duration)
        keyboard_controller.release(input_key)

# Click loop
def run_loop(k1, t1, k2, t2):
    global running
    while running:
        hold_input(k1, t1)
        hold_input(k2, t2)

# Setup input from user
def get_user_config():
    print("Supported keys: letters, numbers, 'space', 'enter', 'left', 'right', 'up', 'down', 'left_arrow', 'right_arrow', 'esc', 'f1'..'f12'")
    k1_str = input("Enter FIRST key to press: ")
    t1 = float(input("How long to hold it (in seconds)? "))

    k2_str = input("Enter SECOND key to press: ")
    t2 = float(input("How long to hold it (in seconds)? "))

    stop_key_str = input("Enter STOP key (to break loop): ")

    k1 = get_input_key(k1_str)
    k2 = get_input_key(k2_str)
    stop_key = get_input_key(stop_key_str)

    return k1, t1, k2, t2, stop_key

# Stop on key press
def on_press(key):
    global running
    if key == stop_key:
        running = False
        print("Loop stopped by user.")
        return False

# Main
if __name__ == "__main__":
    k1, t1, k2, t2, stop_key = get_user_config()
    running = True
    Thread(target=run_loop, args=(k1, t1, k2, t2)).start()
    print("Auto loop started. Press your stop key to exit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
