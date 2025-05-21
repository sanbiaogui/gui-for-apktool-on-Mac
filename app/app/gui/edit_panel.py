import os
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

class EditPanel:
    def __init__(self, master):
        self.master = master
        self.base_dir = tk.StringVar()
        self.file_keyword = tk.StringVar()
        self.smali_keyword = tk.StringVar()
        self.replace_text = tk.StringVar()

        # GUI布局
        tk.Label(master, text="选择APK解包后的根目录:").pack()
        tk.Entry(master, textvariable=self.base_dir, width=60).pack()
        tk.Button(master, text="浏览目录", command=self.browse_folder).pack(pady=5)

        tk.Label(master, text="文件名关键词（匹配并删除）:").pack()
        tk.Entry(master, textvariable=self.file_keyword, width=40).pack()

        tk.Label(master, text="Smali代码关键词（查找并删改）:").pack()
        tk.Entry(master, textvariable=self.smali_keyword, width=40).pack()

        tk.Label(master, text="替换为（可留空表示删除）:").pack()
        tk.Entry(master, textvariable=self.replace_text, width=40).pack()

        tk.Button(master, text="删除匹配文件", command=self.delete_files, bg="#e74c3c", fg="white").pack(pady=5)
        tk.Button(master, text="修改 Smali 内容", command=self.edit_smali, bg="#2980b9", fg="white").pack(pady=5)

        self.output = tk.Label(master, text="", fg="gray", wraplength=500)
        self.output.pack()

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.base_dir.set(path)

    def delete_files(self):
        base = self.base_dir.get()
        keyword = self.file_keyword.get()
        if not base or not keyword:
            messagebox.showerror("错误", "请输入根目录和文件关键词。")
            return

        count = 0
        for root, dirs, files in os.walk(base):
            for file in files:
                if keyword in file:
                    full_path = os.path.join(root, file)
                    try:
                        os.remove(full_path)
                        count += 1
                    except Exception as e:
                        print(f"删除失败: {full_path} - {e}")
        self.output.config(text=f"已删除 {count} 个匹配文件。")

    def edit_smali(self):
        base = self.base_dir.get()
        keyword = self.smali_keyword.get()
        replacement = self.replace_text.get()

        if not base or not keyword:
            messagebox.showerror("错误", "请输入根目录和 Smali 关键词。")
            return

        count = 0
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.endswith(".smali"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        if keyword in content:
                            new_content = content.replace(keyword, replacement)
                            with open(full_path, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            count += 1
                    except Exception as e:
                        print(f"修改失败: {full_path} - {e}")

        self.output.config(text=f"已处理 {count} 个 Smali 文件。")
