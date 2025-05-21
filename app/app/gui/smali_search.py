import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

class SmaliSearchPanel:
    def __init__(self, master):
        self.master = master
        self.search_dir = tk.StringVar()
        self.keyword = tk.StringVar()

        # 路径选择
        tk.Label(master, text="选择 smali 根目录:").pack()
        tk.Entry(master, textvariable=self.search_dir, width=60).pack()
        tk.Button(master, text="浏览", command=self.browse_dir).pack(pady=5)

        # 关键词输入
        tk.Label(master, text="搜索关键词:").pack()
        tk.Entry(master, textvariable=self.keyword, width=40).pack()
        tk.Button(master, text="开始搜索", command=self.search_smali, bg="#f1c40f").pack(pady=5)

        # 搜索结果
        self.result_box = scrolledtext.ScrolledText(master, height=15, wrap=tk.WORD)
        self.result_box.pack(padx=10, pady=5, fill="both", expand=True)

    def browse_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.search_dir.set(dir_path)

    def search_smali(self):
        base_dir = self.search_dir.get()
        keyword = self.keyword.get().strip()
        self.result_box.delete(1.0, tk.END)

        if not base_dir or not os.path.isdir(base_dir):
            messagebox.showerror("错误", "请选择有效的 smali 目录。")
            return
        if not keyword:
            messagebox.showerror("错误", "请输入搜索关键词。")
            return

        matches = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".smali"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            for i, line in enumerate(f, start=1):
                                if keyword in line:
                                    matches.append((file_path, i, line.strip()))
                    except Exception as e:
                        continue

        if not matches:
            self.result_box.insert(tk.END, "没有找到匹配内容。\n")
            return

        for path, line_num, content in matches:
            self.result_box.insert(tk.END, f"{path} [第 {line_num} 行]: {content}\n", "link")
            self.result_box.insert(tk.END, "\n")

        # 点击打开文件（可选）
        def on_click(event):
            index = self.result_box.index("@%s,%s" % (event.x, event.y))
            line = self.result_box.get(index + " linestart", index + " lineend")
            path = line.split(" [第")[0].strip()
            if os.path.exists(path):
                os.system(f"open '{path}'")  # 使用系统默认编辑器打开

        self.result_box.tag_config("link", foreground="blue", underline=True)
        self.result_box.tag_bind("link", "<Button-1>", on_click)
