import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class DecodePanel:
    def __init__(self, master):
        self.master = master
        self.apk_path = tk.StringVar()

        tk.Label(master, text="选择 APK 文件:").pack(pady=5)
        tk.Entry(master, textvariable=self.apk_path, width=60).pack()
        tk.Button(master, text="浏览", command=self.browse_apk).pack()

        tk.Button(master, text="开始反编译", command=self.decode_apk, bg="#3498db", fg="white").pack(pady=10)
        self.output = tk.Label(master, text="", wraplength=500, fg="gray")
        self.output.pack(pady=5)

    def browse_apk(self):
        file_path = filedialog.askopenfilename(filetypes=[("APK 文件", "*.apk")])
        if file_path:
            self.apk_path.set(file_path)

    def decode_apk(self):
        apk = self.apk_path.get()
        if not apk:
            messagebox.showerror("错误", "请先选择 APK 文件。")
            return

        output_dir = os.path.splitext(os.path.basename(apk))[0]
        cmd = ["apktool", "d", apk, "-o", output_dir]
        try:
            subprocess.run(cmd, check=True)
            self.output.config(text=f"反编译完成，输出目录：{output_dir}")
        except subprocess.CalledProcessError as e:
            self.output.config(text=f"反编译失败：{e}")
