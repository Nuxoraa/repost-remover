import os
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

import pyautogui
import keyboard
import win32api
import win32con

CONFIDENCE = 0.95
SCROLL_AMOUNT = -500
SEARCH_REGION = None

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_path()
IMAGE_FILE = os.path.join(BASE_DIR, "icon.png")

if not os.path.exists(IMAGE_FILE):
    messagebox.showerror("Ошибка", "Файл icon.png не найден рядом с программой!")
    sys.exit()

running = False
lock = threading.Lock()

def precise_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def run_loop():
    global running
    while True:
        if running:
            try:
                location = pyautogui.locateCenterOnScreen(
                    IMAGE_FILE,
                    confidence=CONFIDENCE,
                    region=SEARCH_REGION
                )

                if location:
                    x, y = location
                    verify = pyautogui.locateCenterOnScreen(
                        IMAGE_FILE,
                        confidence=CONFIDENCE,
                        region=(x-50, y-50, 100, 100)
                    )

                    if verify:
                        precise_click(x, y)
                        screen_width, screen_height = pyautogui.size()
                        win32api.SetCursorPos((screen_width // 2, screen_height // 2))
                        pyautogui.scroll(SCROLL_AMOUNT)
                        time.sleep(0.6)
                else:
                    time.sleep(0.2)

            except Exception as e:
                print("Ошибка:", e)
                time.sleep(0.5)
        else:
            time.sleep(0.2)

def toggle():
    global running
    with lock:
        running = not running
        if running:
            status_label.config(text="Статус: Включено", fg="#00ff66")
            toggle_btn.config(text="Выключить")
        else:
            status_label.config(text="Статус: Выключено", fg="#ff4444")
            toggle_btn.config(text="Включить")

root = tk.Tk()
root.title("Repost Tool")
root.geometry("420x230")
root.resizable(False, False)
root.configure(bg="#121212")

title_label = tk.Label(
    root,
    text="Repost Automation",
    font=("Segoe UI", 18, "bold"),
    bg="#121212",
    fg="white"
)
title_label.pack(pady=15)

status_label = tk.Label(
    root,
    text="Статус: Выключено",
    font=("Segoe UI", 12),
    bg="#121212",
    fg="#ff4444"
)
status_label.pack(pady=15)

toggle_btn = tk.Button(
    root,
    text="Включить",
    width=18,
    height=2,
    bg="#2962ff",
    fg="white",
    activebackground="#0039cb",
    relief="flat",
    command=toggle
)
toggle_btn.pack()

info_label = tk.Label(
    root,
    text="F2 — Включить / Выключить",
    font=("Segoe UI", 9),
    bg="#121212",
    fg="gray"
)
info_label.pack(pady=15)

threading.Thread(target=run_loop, daemon=True).start()
keyboard.add_hotkey("F2", toggle)

root.mainloop()
