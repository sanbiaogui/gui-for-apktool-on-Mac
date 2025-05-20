import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class BuildPanel:
    def __init__(self, master):
        self.master = master
        self.dir_path = tk.StringVar()

        tk.Label(master, text="选择反编译后的 APK 目录:").pack(pady=5)
        tk.Entry(master, textvariable=self.dir_path, width=60).pack()
        tk.Button(master, text="浏览", command=self.browse_dir).pack()

        tk.Button(master, text="开始重编译", command=self.build_apk, bg="#2ecc71", fg="white").pack(pady=10)
        self.output = tk.Label(master, text="", wraplength=500, fg="gray")
        self.output.pack(pady=5)

    def browse_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dir_path.set(dir_path)

    def build_apk(self):
        path = self.dir_path.get()
        if not path:
            messagebox.showerror("错误", "请先选择目录。")
            return

        cmd = ["apktool", "b", path]
        try:
            subprocess.run(cmd, check=True)
            self.output.config(text=f"重编译完成，输出在：{os.path.join(path, 'dist')}")
        except subprocess.CalledProcessError as e:
            self.output.config(text=f"重编译失败：{e}")
