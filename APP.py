from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from ttkbootstrap import Style
import tkinter.ttk as ttk
import Handler


# 封装 tkinter
class APP:
    def __init__(self):
        # 保存选中索引
        self.index = None

        # ttkbootstrap 风格美化
        style = Style(theme='sandstone')
        self.root = style.master
        self.root.title('Markdown Translator')

        # 获得窗口框架，设置对齐方式和窗口尺寸
        buttonFrame = Frame(self.root)
        buttonFrame.pack()

        ttk.Button(buttonFrame, text='文件', width=12, command=self.open).grid(row=1, column=1, padx=15, pady=20)
        ttk.Button(buttonFrame, text='修复', width=12, command=self.deal).grid(row=1, column=2, padx=15, pady=20)
        ttk.Button(buttonFrame, text='删除', width=12, command=self.delete).grid(row=1, column=3, padx=15, pady=20)
        ttk.Button(buttonFrame, text='清空', width=12, command=self.clear).grid(row=1, column=4, padx=15, pady=20)

        # 列表框架
        listFrame = Frame(self.root)
        listFrame.pack()

        # 设置滚动条
        sb = ttk.Scrollbar(listFrame)
        sb.pack(side=RIGHT, fill=BOTH)

        # 列表盒绑定鼠标按键
        self.listBox = Listbox(listFrame, yscrollcommand=sb.set, width=90, height=15, font=('Consolas', 10))
        self.listBox.bind('<ButtonRelease-1>', self.update)
        self.listBox.pack()

        sb.config(command=self.listBox.yview)

        # 进度条
        self.prog = ttk.Progressbar(self.root, length=200)

    # 设置窗口居中
    def center(self):
        width = 800
        height = 360

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int(screen_width / 2 - width / 2)
        y = int(screen_height / 2 - height / 2)
        size = '{}x{}+{}+{}'.format(width, height, x, y)

        self.root.geometry(size)

    # 开启消息循环
    def loop(self):
        self.root.mainloop()

    # 点击打开文件后进行处理
    def open(self):
        # 限制可选择的文件类型
        namelist = askopenfilenames(filetypes=[('Markdown', '*.md')])
        oldList = self.listBox.get(0, END)

        for name in namelist:
            # 检查是否重复
            if name not in oldList:
                self.listBox.insert(0, name)
                self.listBox.activate(0)

    # 批处理函数
    def deal(self):
        index = 0
        maxLength = 0

        # 设置进度条
        size = self.listBox.size()
        self.prog.pack(pady=10)
        
        for mkfile in self.listBox.get(0, END):
            # 修正过的部分不进行修正
            if mkfile[-10:] != '(Finished)':
                handler = Handler.Handler(mkfile)
                maxLength = max(maxLength, len(mkfile))

                # 进行修正
                handler.fix_path()
                handler.fix_bolder()
                handler.fix_outline()
                handler.fix_math()
                handler.write()

                self.listBox.delete(index)
                self.listBox.insert(index, mkfile + ' ' * (maxLength - len(mkfile) + 8) + '(Finished)')

            self.prog['value'] += 100 / size
            self.root.update()
            index += 1

        self.prog['value'] = 0
        self.prog.forget()

    # 删除选中的项
    def delete(self):
        if self.index is not None and askyesno('提示', f'是否要删除 "{self.listBox.get(self.index)}" ？'):
            self.listBox.delete(self.index)
            self.index = None

    # 删除所有项
    def clear(self):
        if askyesno('提示', f'是否要删除所有项？'):
            self.listBox.delete(0, END)
            self.index = None

    # 获得当前锚定的项
    def update(self, event):
        if self.listBox.get(ANCHOR) != '':
            self.index = self.listBox.curselection()[0]

