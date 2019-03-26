import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class Application(tk.Tk):
    '''
    多页面测试程序
        界面与逻辑分离
    '''

    def __init__(self):
        super().__init__()

        self.wm_title("多页面测试程序")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 四个页面的位置都是 grid(row=0, column=0), 位置重叠，只有最上面的可见！！

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # 切换，提升当前 tk.Frame z轴顺序（使可见）！！此语句是本程序的点睛之处


class StartPage(tk.Frame):
    '''主页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="这里是主页", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="去到第一页", command=lambda: root.show_frame(PageOne)).pack()
        button2 = ttk.Button(self, text="去到第二页", command=lambda: root.show_frame(PageTwo)).pack()
        button3 = ttk.Button(self, text="去到绘图页", command=lambda: root.show_frame(PageThree)).pack()


class PageOne(tk.Frame):
    '''第一页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="这是第一页", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="回到主页", command=lambda: root.show_frame(StartPage)).pack()
        button2 = ttk.Button(self, text="去到第二页", command=lambda: root.show_frame(PageTwo)).pack()


class PageTwo(tk.Frame):
    '''第二页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="这是第二页", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="回到主页", command=lambda: root.show_frame(StartPage)).pack()
        button2 = ttk.Button(self, text="去到第一页", command=lambda: root.show_frame(PageOne)).pack()


class PageThree(tk.Frame):
    '''第三页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        tk.Label(self, text="这是绘图页", font=LARGE_FONT).pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="回到主页", command=lambda: root.show_frame(StartPage)).pack()

        fig = Figure(figsize=(5, 5), dpi=100)
        a = fig.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    # 实例化Application
    app = Application()

    # 主消息循环:
    app.mainloop()