import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class SignerPanel:
    def __init__(self, master):
        self.master = master
        self.apk_path = tk.StringVar()
        self.keystore_path = tk.StringVar()
        self.alias = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(master, text="选择 APK 文件:").pack()
        tk.Entry(master, textvariable=self.apk_path, width=60).pack()
        tk.Button(master, text="浏览 APK", command=self.browse_apk).pack(pady=5)

        tk.Label(master, text="选择 Keystore 文件:").pack()
        tk.Entry(master, textvariable=self.keystore_path, width=60).pack()
        tk.Button(master, text="浏览 Keystore", command=self.browse_keystore).pack(pady=5)

        tk.Label(master, text="Keystore 别名 (Alias):").pack()
        tk.Entry(master, textvariable=self.alias, width=40).pack()

        tk.Label(master, text="Keystore 密码:").pack()
        tk.Entry(master, textvariable=self.password, show="*", width=40).pack()

        tk.Button(master, text="签名 APK", command=self.sign_apk, bg="#9b59b6", fg="white").pack(pady=10)
        self.output = tk.Label(master, text="", fg="gray", wraplength=500)
        self.output.pack()

    def browse_apk(self):
        path = filedialog.askopenfilename(filetypes=[("APK 文件", "*.apk")])
        if path:
            self.apk_path.set(path)

    def browse_keystore(self):
        path = filedialog.askopenfilename(filetypes=[("Keystore", "*.keystore *.jks")])
        if path:
            self.keystore_path.set(path)

    def sign_apk(self):
        apk = self.apk_path.get()
        keystore = self.keystore_path.get()
        alias = self.alias.get()
        password = self.password.get()

        if not apk or not keystore or not alias or not password:
            messagebox.showerror("错误", "请填写所有信息。")
            return

        cmd = [
            "jarsigner",
            "-keystore", keystore,
            "-storepass", password,
            apk,
            alias
        ]

        try:
            subprocess.run(cmd, check=True)
            self.output.config(text="签名成功！APK 已签名。")
        except subprocess.CalledProcessError as e:
            self.output.config(text=f"签名失败：{e}")
