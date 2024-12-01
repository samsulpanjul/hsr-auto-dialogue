import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller, Listener, Key
import threading
import time
import random
import pyautogui
pyautogui.useImageNotFoundException(False)

keyboard = Controller()
running = False
use_random_delay = False
delay = 500
min_delay = 100
max_delay = 1000


def press_space():
    global running, use_random_delay, delay, min_delay, max_delay
    while running:
        next_button = pyautogui.locateCenterOnScreen('./images/nextbutton.png', grayscale=True, confidence=0.8)
        if next_button is not None:
            pyautogui.click(next_button)
        keyboard.press(' ')
        keyboard.release(' ')
        if use_random_delay:
            current_delay = random.randint(min_delay, max_delay) / 1000
        else:
            current_delay = delay / 1000
        time.sleep(current_delay)

def toggle_start_stop():
    global running
    if running:
        running = False
        status_label.config(text="Status: Stopped", fg="red")
    else:
        running = True
        threading.Thread(target=press_space, daemon=True).start()
        status_label.config(text="Status: Running", fg="green")

def on_press(key):
    if key == Key.caps_lock:
        toggle_start_stop()

def update_delay():
    global delay, min_delay, max_delay
    try:
        delay = int(delay_entry.get())
        min_delay = int(min_delay_entry.get())
        max_delay = int(max_delay_entry.get())
        if min_delay > max_delay:
            raise ValueError("Min delay must be less than or equal to max delay.")
        messagebox.showinfo("Success", "Delay updated successfully!")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def toggle_random_delay():
    global use_random_delay
    use_random_delay = random_delay_var.get()

root = tk.Tk()
root.title("HSR Auto")
root.geometry("400x400")

tk.Label(root, text="HSR Auto", font=("Arial", 14)).pack(pady=10)

status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Arial", 12))
status_label.pack(pady=10)

tk.Label(root, text="Delay (ms):", font=("Arial", 10)).pack(pady=5)
delay_entry = tk.Entry(root)
delay_entry.insert(0, "500")
delay_entry.pack(pady=5)

random_delay_var = tk.BooleanVar()
random_delay_checkbox = tk.Checkbutton(root, text="Use Random Delay", variable=random_delay_var, command=toggle_random_delay)
random_delay_checkbox.pack(pady=5)

tk.Label(root, text="Min Delay (ms):", font=("Arial", 10)).pack(pady=5)
min_delay_entry = tk.Entry(root)
min_delay_entry.insert(0, "100")
min_delay_entry.pack(pady=5)

tk.Label(root, text="Max Delay (ms):", font=("Arial", 10)).pack(pady=5)
max_delay_entry = tk.Entry(root)
max_delay_entry.insert(0, "1000")
max_delay_entry.pack(pady=5)

update_button = tk.Button(root, text="Update Delay", command=update_delay, bg="blue", fg="white")
update_button.pack(pady=10)

tk.Label(root, text="Press 'CapsLock' to Start/Stop", font=("Arial", 10)).pack(pady=10)

listener = Listener(on_press=on_press)
listener.start()

root.mainloop()

listener.stop()
