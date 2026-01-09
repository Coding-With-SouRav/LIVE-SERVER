import sys
import webview
import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ctypes 

# ---------------- RESOURCE PATH ---------------- #
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

HTML_FILE = None
WINDOW_SIZE = (900, 600)
WEBVIEW_TITLE = "Live HTML UI"

# ---------------- DEVICE GEOMETRIES ---------------- #
DEVICE_PRESETS = {
    "Android Small (360x640)": (360, 640),
    "Android Medium (412x732)": (412, 732),
    "Android Large (480x800)": (480, 800),
    "Android Tablet (600x960)": (600, 960),
    "Android Full HD (1080x1920)": (360, 640),

    "iPhone SE (375x667)": (375, 667),
    "iPhone 14 (390x844)": (390, 844),
    "iPhone 14 Pro Max (430x932)": (430, 932),
    "iPad Mini (768x1024)": (768, 1024),
    "iPad Pro (1024x1366)": (1024, 1366),
}

# ---------------- LIVE RELOAD ---------------- #
class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if HTML_FILE and event.src_path == HTML_FILE:
            time.sleep(0.2)
            if webview.windows:
                webview.windows[0].evaluate_js("location.reload();")

def start_watcher():
    observer = Observer()
    observer.schedule(
        ReloadHandler(),
        path=os.path.dirname(HTML_FILE),
        recursive=False
    )
    observer.start()

# ---------------- CLOSE CONFIRM ---------------- #
def on_webview_close():
    return messagebox.askyesno(
        "Exit Confirmation",
        "Are you sure you want to close the Live Preview?"
    )

# ---------------- WINDOWS RESIZE CONTROL ---------------- #
user32 = ctypes.windll.user32
GWL_STYLE = -16
WS_THICKFRAME = 0x00040000

def get_hwnd_by_title(title, timeout=5):
    """Wait until the window exists and return HWND"""
    end = time.time() + timeout
    while time.time() < end:
        hwnd = user32.FindWindowW(None, title)
        if hwnd:
            return hwnd
        time.sleep(0.1)
    return None

def set_resizable(hwnd, enable):
    style = user32.GetWindowLongW(hwnd, GWL_STYLE)
    if enable:
        style |= WS_THICKFRAME
    else:
        style &= ~WS_THICKFRAME

    user32.SetWindowLongW(hwnd, GWL_STYLE, style)
    user32.SetWindowPos(
        hwnd, None, 0, 0, 0, 0,
        0x0027  # FRAMECHANGED | NO_MOVE | NO_SIZE | NO_ZORDER
    )

def ctrl_resize_listener():
    hwnd = get_hwnd_by_title(WEBVIEW_TITLE)
    if not hwnd:
        return

    ctrl_down = False

    while True:
        time.sleep(0.05)
        is_ctrl = user32.GetAsyncKeyState(0x11) & 0x8000  # VK_CONTROL

        if is_ctrl and not ctrl_down:
            ctrl_down = True
            set_resizable(hwnd, True)

        elif not is_ctrl and ctrl_down:
            ctrl_down = False
            set_resizable(hwnd, False)

# ---------------- TTKBOOTSTRAP UI ---------------- #
def open_selector():
    global HTML_FILE, WINDOW_SIZE

    root = tb.Window(
        title="Live HTML Preview",
        themename="superhero",
        size=(420, 340),
        resizable=(False, False)
    )

    file_var = tk.StringVar()
    device_var = tk.StringVar(value=list(DEVICE_PRESETS.keys())[0])

    def browse_file():
        file = filedialog.askopenfilename(
            filetypes=[("HTML Files", "*.html")]
        )
        if file:
            file_var.set(file)

    def open_webview():
        global HTML_FILE, WINDOW_SIZE

        if not file_var.get():
            messagebox.showerror("Error", "Please select an HTML file")
            return

        HTML_FILE = os.path.abspath(file_var.get())
        WINDOW_SIZE = DEVICE_PRESETS[device_var.get()]

        root.destroy()
        threading.Thread(target=start_watcher, daemon=True).start()

        webview.create_window(
            title=WEBVIEW_TITLE,
            url=f"file:///{HTML_FILE}",
            width=WINDOW_SIZE[0],
            height=WINDOW_SIZE[1],
            on_top=True,
            confirm_close=on_webview_close,
            resizable=False
        )

        threading.Thread(
            target=ctrl_resize_listener,
            daemon=True
        ).start()

        webview.start()

    container = tb.Frame(root, padding=20)
    container.pack(fill=BOTH, expand=True)

    tb.Label(container, text="HTML File",
             font=("Segoe UI", 11, "bold")).pack(anchor=W)

    tb.Entry(container, textvariable=file_var,
             bootstyle="secondary").pack(fill=X, pady=6)

    tb.Button(container, text="Browse HTML",
              command=browse_file,
              bootstyle=INFO).pack(pady=6, fill=X)

    tb.Label(container, text="Device Preview Size",
             font=("Segoe UI", 11, "bold")).pack(anchor=W, pady=(18, 5))

    tb.OptionMenu(container, device_var,
                  device_var.get(),
                  *DEVICE_PRESETS.keys(),
                  bootstyle="secondary").pack(fill=X)

    tb.Button(container, text="Launch Live Preview",
              command=open_webview,
              bootstyle=SUCCESS).pack(pady=28, fill=X)

    root.mainloop()

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    open_selector()
