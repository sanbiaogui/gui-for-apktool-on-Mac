import tkinter as tk
from tkinter import ttk
from gui.decode_panel import DecodePanel
from gui.build_panel import BuildPanel
from gui.smali_search import SmaliSearchPanel
from gui.signer_panel import SignerPanel
from gui.edit_panel import EditPanel


class ApktoolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Apktool GUI 工具")
        self.geometry("600x400")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # 反编译面板
        decode_frame = ttk.Frame(notebook)
        DecodePanel(decode_frame)
        notebook.add(decode_frame, text="反编译")

        # 重编译面板
        build_frame = ttk.Frame(notebook)
        BuildPanel(build_frame)
        notebook.add(build_frame, text="重编译")

        # Smali 搜索面板
        search_frame = ttk.Frame(notebook)
        SmaliSearchPanel(search_frame)
        notebook.add(search_frame, text="Smali 搜索")

        #签名器面板
        sign_frame = ttk.Frame(notebook)
        SignerPanel(sign_frame)
        notebook.add(sign_frame, text="APK 签名")

        #自动删除广告模块规则
        edit_frame = ttk.Frame(notebook)
        EditPanel(edit_frame)
        notebook.add(edit_frame, text="关键词删改")



if __name__ == "__main__":
    app = ApktoolApp()
    app.mainloop()
