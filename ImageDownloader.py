#!/usr/bin/env python3
# ============================================================
# Dark Aesthetic Image Downloader GUI
# DuckDuckGo + Bing (Stable, No Google)
# ============================================================

import os
import threading
import hashlib
import requests
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from duckduckgo_search import DDGS

# ---------------- THEME ----------------
BG_COLOR   = "#0f172a"
FG_COLOR   = "#e5e7eb"
ACCENT     = "#38bdf8"
ENTRY_BG   = "#020617"

HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 10

# ---------------- IMAGE SAVE ----------------
def save_image(url, folder):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return False

        ext = os.path.splitext(urlparse(url).path)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            ext = ".jpg"

        name = hashlib.md5(url.encode()).hexdigest() + ext
        with open(os.path.join(folder, name), "wb") as f:
            f.write(r.content)
        return True
    except:
        return False

# ---------------- SEARCH ----------------
def duck_search(query, limit):
    with DDGS() as ddgs:
        return [r["image"] for r in ddgs.images(query, max_results=limit)]

def bing_search(query, limit):
    with DDGS() as ddgs:
        return [r["image"] for r in ddgs.images(query, region="us-en", max_results=limit)]

# ---------------- GUI APP ----------------
class ImageDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Downloader")
        self.root.geometry("780x420")
        self.root.configure(bg=BG_COLOR)

        self.setup_style()
        self.build_ui()

    # ---------- STYLE ----------
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "TButton",
            background="#1e293b",
            foreground="white",
            padding=8
        )

        style.configure(
            "TCombobox",
            fieldbackground=ENTRY_BG,
            background=ENTRY_BG,
            foreground=FG_COLOR,
            arrowcolor=FG_COLOR,
            padding=5
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", ENTRY_BG)],
            foreground=[("readonly", FG_COLOR)],
            background=[("readonly", ENTRY_BG)]
        )

        style.configure(
            "TProgressbar",
            troughcolor=ENTRY_BG,
            background=ACCENT
        )

        # 🔥 Dropdown list styling (THIS fixes ugly dropdown)
        self.root.option_add("*TCombobox*Listbox.background", ENTRY_BG)
        self.root.option_add("*TCombobox*Listbox.foreground", FG_COLOR)
        self.root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.root.option_add("*TCombobox*Listbox.selectForeground", ENTRY_BG)
        self.root.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))

    # ---------- ROW ----------
    def row(self, parent, text):
        row = tk.Frame(parent, bg=BG_COLOR)
        row.pack(fill="x", pady=8)

        tk.Label(
            row,
            text=text,
            width=16,
            anchor="w",
            bg=BG_COLOR,
            fg=FG_COLOR,
            font=("Segoe UI", 10)
        ).pack(side="left")

        return row

    # ---------- UI ----------
    def build_ui(self):
        frame = tk.Frame(self.root, bg=BG_COLOR, padx=30, pady=25)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Image Downloader",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=ACCENT
        ).pack(pady=(0, 25))

        # Keywords
        r = self.row(frame, "Search Keywords")
        self.keywords = tk.Entry(r, bg=ENTRY_BG, fg="white", insertbackground="white")
        self.keywords.pack(side="left", fill="x", expand=True)

        # Count
        r = self.row(frame, "Images Count")
        self.count = tk.Entry(r, bg=ENTRY_BG, fg="white", insertbackground="white")
        self.count.insert(0, "10")
        self.count.pack(side="left", fill="x", expand=True)

        # Engine
        r = self.row(frame, "Search Engine")
        self.engine = ttk.Combobox(
            r,
            values=["duck", "bing", "all"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.engine.set("all")
        self.engine.pack(side="left", fill="x", expand=True)

        # Output
        r = self.row(frame, "Output Folder")
        self.output = tk.Entry(r, bg=ENTRY_BG, fg="white", insertbackground="white")
        self.output.insert(0, "./images")
        self.output.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(r, text="Browse", command=self.browse).pack(side="left")

        # Progress
        self.progress = ttk.Progressbar(frame)
        self.progress.pack(fill="x", pady=(20, 6))

        # Status
        self.status = tk.Label(
            frame,
            text="Ready",
            bg=BG_COLOR,
            fg="#22c55e",
            anchor="w"
        )
        self.status.pack(fill="x")

        # Button
        ttk.Button(
            frame,
            text="⬇ Download Images",
            command=self.start
        ).pack(pady=18)

    # ---------- ACTIONS ----------
    def browse(self):
        path = filedialog.askdirectory()
        if path:
            self.output.delete(0, tk.END)
            self.output.insert(0, path)

    def start(self):
        threading.Thread(target=self.download, daemon=True).start()

    def download(self):
        query = self.keywords.get().strip()
        if not query:
            messagebox.showerror("Error", "Enter search keywords")
            return

        try:
            count = int(self.count.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid image count")
            return

        engine = self.engine.get()
        out_dir = os.path.join(self.output.get(), query.replace(" ", "_"))
        os.makedirs(out_dir, exist_ok=True)

        self.status.config(text="Searching images...", fg="#facc15")
        self.progress["value"] = 0

        urls = []
        if engine in ["duck", "all"]:
            urls.extend(duck_search(query, count))
        if engine in ["bing", "all"]:
            urls.extend(bing_search(query, count))

        urls = list(dict.fromkeys(urls))[:count]
        total = len(urls)

        if total == 0:
            self.status.config(text="No images found", fg="#ef4444")
            return

        saved = 0
        for i, url in enumerate(urls, 1):
            if save_image(url, out_dir):
                saved += 1
            self.progress["value"] = (i / total) * 100

        self.status.config(
            text=f"Done: {saved}/{total} images saved",
            fg="#22c55e"
        )

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    ImageDownloaderApp(root)
    root.mainloop()
