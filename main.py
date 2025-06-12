import sys
import os
import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller, Listener, Key
import threading
import time
import random
import pyautogui
import pygetwindow as gw
pyautogui.useImageNotFoundException(False)

keyboard = Controller()
running = False
use_random_delay = False
delay = 100
min_delay = 100
max_delay = 500

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def click(position):
    hold_time = random.uniform(0.05, 0.1)
    pyautogui.moveTo(position)
    pyautogui.mouseDown()
    time.sleep(hold_time)
    pyautogui.mouseUp()

icon = resource_path('./images/firefly.ico')
next_button_img = resource_path('./images/nextbutton.png')
dialog_img = resource_path('./images/dialog.png')
close_img = resource_path('./images/x.png')

def press_space():
    global running, use_random_delay, delay, min_delay, max_delay
    while running:
        next_button = pyautogui.locateCenterOnScreen(next_button_img, grayscale=True, confidence=0.8)
        dialog = pyautogui.locateOnScreen(dialog_img, grayscale=True, confidence=0.8)
        close = pyautogui.locateCenterOnScreen(close_img, grayscale=True, confidence=0.8)
        if next_button is not None:
            click(next_button)
        if dialog is not None:
            click(dialog)
        if close is not None:
            click(close)
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
        hsr_windows = gw.getWindowsWithTitle("Honkai: Star Rail")
        if hsr_windows:
            hsr_windows[0].activate()
        else:
            print("Honkai: Star Rail not found!")
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
root.iconbitmap(icon)
root.title("HSR Auto")
root.geometry("400x400")

tk.Label(root, text="HSR Auto", font=("Arial", 14)).pack(pady=10)

status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Arial", 12))
status_label.pack(pady=10)

tk.Label(root, text="Delay (ms):", font=("Arial", 10)).pack(pady=5)
delay_entry = tk.Entry(root)
delay_entry.insert(0, "100")
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
max_delay_entry.insert(0, "500")
max_delay_entry.pack(pady=5)

update_button = tk.Button(root, text="Update Delay", command=update_delay, bg="blue", fg="white")
update_button.pack(pady=10)

tk.Label(root, text="Press 'CapsLock' to Start/Stop", font=("Arial", 10)).pack(pady=10)

listener = Listener(on_press=on_press)
listener.start()

root.mainloop()

listener.stop()
