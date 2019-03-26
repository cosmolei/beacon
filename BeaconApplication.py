import tkinter as tk
from tkinter import ttk
from beacon_autoexam import fileOperation
from beacon_autoexam import ExamRobot
import configparser
import tkinter.messagebox
from PIL import Image, ImageTk

LARGE_FONT = ("Verdana", 12)

class Application(tk.Tk):
    '''多页面测试程序界面与逻辑分离'''

    # 登陆状态
    login_status = 0

    def __init__(self):
        super().__init__()

        # self.iconbitmap(default="red.png")
        self.geometry("400x400+300+100")
        self.wm_title("灯塔在线自助答题")
        self.iconbitmap("ico.ico")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # 设置菜单栏
        menubar = tk.Menu(self)
        fmenu1 = tk.Menu(self)
        fmenu1.add_command(label='党员', command=lambda: self.show_party_frame(PartyPage))
        fmenu1.add_command(label='群众', command=lambda: self.show_frame(PeoplePage))

        fmenu2 = tk.Menu(self)
        fmenu2.add_command(label='党员', command=lambda: self.show_party_frame(PartySettingPage))
        fmenu2.add_command(label='群众', command=lambda: self.show_frame(PeopleSettingPage))
        fmenu2.add_command(label='设置', command=lambda: self.show_frame(SettingsPage))

        menubar.add_cascade(label='答题', menu=fmenu1)
        menubar.add_cascade(label='管理', menu=fmenu2)
        self['menu'] = menubar

        self.frames = {}
        for F in (MainPage, PeoplePage, PartyPage, PartySettingPage, PeopleSettingPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 四个页面的位置都是 grid(row=0, column=0), 位置重叠，只有最上面的可见！！

        self.show_frame(MainPage)



    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # 切换，提升当前 tk.Frame z轴顺序（使可见）！！此语句是本程序的点睛之处

    def show_party_frame(self, cont):
        if self.login_status == 0 :
            self.login_pop()
        else:
            frame = self.frames[cont]
            frame.tkraise()

    def login_pop(self):
        def inputint():
            if entry1.get() == 'admin' and entry2.get() == '123456':
                print("登陆成功")
                self.setLoginStatus(1)
                pop.destroy()
            else:
                tkinter.messagebox.showinfo(title='提示', message='用户名或密码错误，登陆失败!')

        def inputclear():
            pop.destroy()

        pop = tk.Tk()  # 弹出框框名
        pop.title('系统账号登陆')
        pop.geometry('270x100+350+150')  # 设置弹出框的大小 w x h

        label1 = tk.Label(pop, text="账号").grid(row=0)
        label2 = tk.Label(pop, text="密码").grid(row=1)

        entry1 = tk.Entry(pop)
        entry1.grid(row=0, column=1)

        entry2 = tk.Entry(pop)
        entry2.grid(row=1, column=1)

        btn1 = tk.Button(pop, text='登陆', command=inputint)  # 按下此按钮(Input), 触发inputint函数
        btn2 = tk.Button(pop, text='取消', command=inputclear)  # 按下此按钮(Clear), 触发inputclear函数

        # 按钮定位
        btn1.grid(row=3, column=0)
        btn2.grid(row=3, column=1)

        # 上述完成之后, 开始真正弹出弹出框
        pop.mainloop()

    def setLoginStatus(self, value):
        self.login_status = value

class MainPage(tk.Frame):
    '''主页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="灯塔自助答题系统", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        load = Image.open('da.png')
        render = ImageTk.PhotoImage(load)

        img = tk.Label(self, image=render)
        img.image = render
        img.pack()


class PeoplePage(tk.Frame):
    '''群众答题页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="群众答题", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        lb = tk.Listbox(self,height=3)
        self.peopleList = fileOperation.readPeopleList()
        for item in self.peopleList:
            lb.insert(tk.END, item)
        lb.pack()
        button = ttk.Button(self, text="刷新用户", command=lambda: self.refreshPeople(lb)).pack()
        button1 = ttk.Button(self, text="开始答题", command=lambda: self.startExam(logText, self.peopleList)).pack()

        logText = tk.Text(self, width=350, height=15)
        logText.pack()
    def refreshPeople(self, lb):
        lb.delete(0,lb.size())
        self.peopleList = fileOperation.readPeopleList()
        for item in self.peopleList:
            lb.insert(tk.END, item)

    def reveal_log(self, logText, message):
        logText.insert(tk.END, message + '\n')

    def startExam(self, logText, peopleList):
        print("开始群众答题")
        ExamRobot.people_exam(self, logText, peopleList)

class PartyPage(tk.Frame):
    '''党员答题页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="这是党员答题页", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        lb = tk.Listbox(self, height=3)
        self.partyMemberList = fileOperation.readPartyMemberList()
        for item in self.partyMemberList:
            lb.insert(tk.END, item[0])
        lb.pack()
        button = ttk.Button(self, text="刷新用户", command=lambda: self.refreshPeople(lb)).pack()
        button1 = ttk.Button(self, text="开始答题", command=lambda: self.startExam(logText, self.partyMemberList)).pack()

        logText = tk.Text(self, width=350, height=15)
        logText.pack()
    def refreshPeople(self, lb):
        lb.delete(0,lb.size())
        self.partyMemberList = fileOperation.readPartyMemberList()
        for item in self.partyMemberList:
            lb.insert(tk.END, item[0])

    def reveal_log(self, logText, message):
        logText.insert(tk.END, message + '\n')

    def startExam(self, logText, partyMemberList):
        print("开始党员答题")
        ExamRobot.party_exam(self, logText, partyMemberList)

class PartySettingPage(tk.Frame):
    '''党员用户设置页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        tree = ttk.Treeview(self, height=5, show="headings")
        tree["columns"] = ("姓名", "账号", "密码")
        tree.column("姓名", width=100)
        tree.column("账号", width=100)
        tree.column("密码", width=100)
        tree.heading("姓名", text="姓名")
        tree.heading("账号", text="账号")
        tree.heading("密码", text="密码")
        partyMemberList = fileOperation.readPartyMemberList()
        for i in range(0, len(partyMemberList)):
            tree.insert("", i, values=(partyMemberList[i][0],partyMemberList[i][1],partyMemberList[i][2]))

        def edit_before(event):
            item = tree.selection()[0]
            self.edit_partymember(tree, item)

        tree.bind("<Double-1>", edit_before)

        add_button = ttk.Button(self, text="添加", command=lambda: self.add_partymember(tree))
        add_button.pack(padx=10, pady=10)

        tree.pack()

    def add_partymember(self, tree):
        """
        使用tkinter弹出输入框输入数字, 具有确定输入和清除功能, 可在函数内直接调用num(文本框的值)使用
        """

        def inputint():
            tree.insert("", len(tree.get_children()), values=(entry1.get(), entry2.get(), entry3.get()))
            fileOperation.addPartyMember(entry1.get() + '+++' + entry2.get() + '+++' + entry3.get())
            pop.destroy()

        def inputclear():
            pop.destroy()

        pop = tk.Tk()  # 弹出框框名
        pop.title('添加党员账号')
        pop.geometry('270x120+350+150')  # 设置弹出框的大小 w x h

        label1 = tk.Label(pop, text="姓名").grid(row=0)
        label2 = tk.Label(pop, text="账号").grid(row=1)
        label3 = tk.Label(pop, text="密码").grid(row=2)

        entry1 = tk.Entry(pop)
        entry1.grid(row=0, column=1)

        entry2 = tk.Entry(pop)
        entry2.grid(row=1, column=1)

        entry3 = tk.Entry(pop)
        entry3.grid(row=2, column=1)

        btn1 = tk.Button(pop, text='保存', command=inputint)  # 按下此按钮(Input), 触发inputint函数
        btn2 = tk.Button(pop, text='取消', command=inputclear)  # 按下此按钮(Clear), 触发inputclear函数

        # 按钮定位
        btn1.grid(row=3, column=0)
        btn2.grid(row=3, column=1)

        # 上述完成之后, 开始真正弹出弹出框
        pop.mainloop()

    def edit_partymember(self,tree, item):
        def inputint():
            oldMember = tree.item(item, "values")[0] + '+++' + tree.item(item, "values")[1] + '+++' + tree.item(item, "values")[2]
            tree.set(item, 0, entry1.get())
            tree.set(item, 1, entry2.get())
            tree.set(item, 2, entry3.get())
            fileOperation.modPartyMember(oldMember, entry1.get() + '+++' + entry2.get() + '+++' +entry3.get())
            pop.destroy()

        def inputclear():
            delValue = tree.item(item, "values")[0] + '+++' + tree.item(item, "values")[1] + '+++' + tree.item(item, "values")[2]
            tree.delete(item)
            fileOperation.delPartyMember(delValue)
            pop.destroy()

        pop = tk.Tk()  # 弹出框框名
        pop.title('添加群众账号')
        pop.geometry('270x120+350+150')  # 设置弹出框的大小 w x h

        label1 = tk.Label(pop, text="姓名").grid(row=0)
        label2 = tk.Label(pop, text="账号").grid(row=1)
        label3 = tk.Label(pop, text="密码").grid(row=2)

        entry1 = tk.Entry(pop)
        entry1.insert(tk.END, tree.item(item, "values")[0])
        entry1.grid(row=0, column=1)

        entry2 = tk.Entry(pop)
        entry2.insert(tk.END, tree.item(item, "values")[1])
        entry2.grid(row=1, column=1)

        entry3 = tk.Entry(pop)
        entry3.insert(tk.END, tree.item(item, "values")[1])
        entry3.grid(row=2, column=1)

        btn1 = tk.Button(pop, text='修改', command=inputint)  # 按下此按钮(Input), 触发inputint函数
        btn2 = tk.Button(pop, text='删除', command=inputclear)  # 按下此按钮(Clear), 触发inputclear函数

        # 按钮定位
        btn1.grid(row=3, column=0)
        btn2.grid(row=3, column=1)

        # 上述完成之后, 开始真正弹出弹出框
        pop.mainloop()

class PeopleSettingPage(tk.Frame):
    '''群众用户设置页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        tree = ttk.Treeview(self, height=5, show="headings")
        tree["columns"] = ("账号")
        tree.column("账号", width=200)
        tree.heading("账号", text="账号")
        peopleList = fileOperation.readPeopleList()
        for i in range(0, len(peopleList)):
            tree.insert("", i, values=(peopleList[i]))

        def edit_before(event):
            item = tree.selection()[0]
            self.edit_people(tree, item)

        tree.bind("<Double-1>", edit_before)

        add_button = ttk.Button(self, text="添加", command=lambda:self.add_people(tree))
        add_button.pack(padx=10,pady=10)

        tree.pack()

    def add_people(self, tree):
        """
        使用tkinter弹出输入框输入数字, 具有确定输入和清除功能, 可在函数内直接调用num(文本框的值)使用
        """

        def inputint():
            tree.insert("", len(tree.get_children()), values=(entry1.get()))
            fileOperation.addPeople(entry1.get())
            pop.destroy()

        def inputclear():
            pop.destroy()

        pop = tk.Tk()  # 弹出框框名
        pop.title('添加群众账号')
        pop.geometry('270x60+350+150')  # 设置弹出框的大小 w x h

        var = tk.StringVar()  # 这即是输入框中的内容
        var.set('Content of var')  # 通过var.get()/var.set() 来 获取/设置var的值
        entry1 = tk.Entry(pop, textvariable=var)  # 设置"文本变量"为var
        entry1.pack()  # 将entry"打上去"
        btn1 = tk.Button(pop, text='保存', command=inputint)  # 按下此按钮(Input), 触发inputint函数
        btn2 = tk.Button(pop, text='取消', command=inputclear)  # 按下此按钮(Clear), 触发inputclear函数

        # 按钮定位
        btn2.pack(side='right')
        btn1.pack(side='right')

        # 上述完成之后, 开始真正弹出弹出框
        pop.mainloop()

    def edit_people(self,tree, item):
        def inputint():
            oldPeople = tree.item(item, "values")[0]
            tree.set(item, 0, entry1.get())
            fileOperation.modPeople(oldPeople, entry1.get())
            pop.destroy()

        def inputclear():
            delValue = tree.item(item, "values")[0]
            tree.delete(item)
            fileOperation.delPeople(delValue)
            pop.destroy()

        pop = tk.Tk()  # 弹出框框名
        pop.title('添加群众账号')
        pop.geometry('270x60+350+150')  # 设置弹出框的大小 w x h

        entry1 = tk.Entry(pop)
        entry1.insert(tk.END, tree.item(item, "values")[0])
        entry1.pack()

        btn1 = tk.Button(pop, text='修改', command=inputint)  # 按下此按钮(Input), 触发inputint函数
        btn2 = tk.Button(pop, text='删除', command=inputclear)  # 按下此按钮(Clear), 触发inputclear函数

        # 按钮定位
        btn2.pack(side='right')
        btn1.pack(side='right')

        # 上述完成之后, 开始真正弹出弹出框
        pop.mainloop()


class SettingsPage(tk.Frame):
    '''全局设置页'''

    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="登录链接")
        label.grid(row=0)

        label1 = tk.Label(self, text="答题链接")
        label1.grid(row=1)

        label2 = tk.Label(self, text="登出链接")
        label2.grid(row=2)

        label3 = tk.Label(self, text="题库链接")
        label3.grid(row=3)

        label4 = tk.Label(self, text="题库详细")
        label4.grid(row=4)

        label5 = tk.Label(self, text="浏览器")
        label5.grid(row=5)

        label6 = tk.Label(self, text="尝试登陆次数")
        label6.grid(row=6)

        label7 = tk.Label(self, text="答题间隔")
        label7.grid(row=7)

        label8 = tk.Label(self, text="超时")
        label8.grid(row=8)

        # 读取settings
        config = configparser.ConfigParser()
        config.read("settings.conf")
        login_url = config.get("default", "login_url")
        lightTower_url = config.get("default", "lightTower_url")
        logout_url = config.get("default", "logout_url")
        tk_url = config.get("default", "tk_url")
        tkdetail_url = config.get("default", "tkdetail_url")
        browser = config.get("config", "browser")
        wrong_time = config.getint("config", "wrong_time")
        answer_long = config.getint("config", "answer_long")
        overdure = config.getint("config", "overdure")

        entry = tk.Entry(self)
        entry.insert(tk.END, login_url)
        entry.grid(row=0, column=1)
        entry1 = tk.Entry(self)
        entry1.insert(tk.END, lightTower_url)
        entry1.grid(row=1, column=1)
        entry2 = tk.Entry(self)
        entry2.insert(tk.END, logout_url)
        entry2.grid(row=2, column=1)
        entry3 = tk.Entry(self)
        entry3.insert(tk.END, tk_url)
        entry3.grid(row=3, column=1)
        entry4 = tk.Entry(self)
        entry4.insert(tk.END, tkdetail_url)
        entry4.grid(row=4, column=1)
        entry5 = tk.Entry(self)
        entry5.insert(tk.END, browser)
        entry5.grid(row=5, column=1)
        entry6 = tk.Entry(self)
        entry6.insert(tk.END, wrong_time)
        entry6.grid(row=6, column=1)
        entry7 = tk.Entry(self)
        entry7.insert(tk.END, answer_long)
        entry7.grid(row=7, column=1)
        entry8 = tk.Entry(self)
        entry8.insert(tk.END, overdure)
        entry8.grid(row=8, column=1)

        def savesettings():
            config = configparser.ConfigParser()
            config.read("settings.conf")
            config.set('default', 'login_url', entry.get())
            config.set('default', 'lightTower_url', entry1.get())
            config.set('default', 'logout_url', entry2.get())
            config.set('default', 'tk_url', entry3.get())
            config.set('default', 'tkdetail_url', entry4.get())
            config.set('config', 'browser', entry5.get())
            config.set('config', 'wrong_time', entry6.get())
            config.set('config', 'answer_long', entry7.get())
            config.set('config', 'overdure', entry8.get())
            with open("settings.conf", 'w') as fw:  # 循环写入
                config.write(fw)



        btn1 = tk.Button(self, text='保存', command=savesettings)  # 按下此按钮(Input), 触发inputint函数

        # 按钮定位
        btn1.grid(row=9, column=1)




if __name__ == '__main__':
    # 实例化Application
    app = Application()

    # 主消息循环:
    app.mainloop()