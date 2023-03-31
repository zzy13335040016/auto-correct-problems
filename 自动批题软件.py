import tkinter
import tkinter.ttk
import tkinter.messagebox
import time
import os
import cv2
import pykeyboard
import threading
import keyboard
import random
import ctypes
from aip import AipOcr
import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Key, Controller
from math import *
import requests
k = Controller()  # 设置控制键盘的变量

# 2023.2.25 23:00 未完成：删除小题、代码编辑、截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能、批题代码、小题增减保存 搜索普通设置函数、设置普通设置函数
# 2023.2.26 10:07 弄好：小题增加保存相关代码
#           10:43 弄好：小题删减保存相关代码 未完成：代码/坐标编辑、截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能、批题代码 搜索普通设置函数、设置普通设置函数
#           11:24 弄好：坐标编辑窗口 未完成：代码编辑、截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能、批题代码、坐标保存 搜索普通设置函数、设置普通设置函数
# 2023.3.3  20:00 弄好：搜索普通设置函数、设置普通设置函数 未完成：代码编辑、截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能、批题代码、坐标保存
# 2023.3.17 24:00 弄好：设置窗口（未加判断） 未完成：截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能、批题代码、坐标保存、代码编辑保存
# 2023.3.18 12:41 弄好：1模式下批题函数，批题函数入口 未完成：截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能、2模式下的批题代码、坐标保存、代码编辑保存
# 2023.3.11 01:01 弄好：1模式下批题函数的详细代码、坐标保存、代码编辑保存 未完成：截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能、2模式下的批题代码
# 2023.3.23 18:37 弄好：2模式下批题函数的详细代码 未完成：截屏处理、自动模式与辅助模式切换判断、开始批题函数、设置功能
#           20:46 弄好：修改一些bug，发现一个问题：eval函数只能执行单行代码，考虑：制作ui界面或存在一个文件夹中来调用，第二种在没有python环境的电脑上运行很困难，考虑第一种方法
# 2023.3.25 23:33 弄好：上述bug，创建一个简单于python的语言、窗口dpi适配 未完成：截屏处理、自动模式与辅助模式切换判断设置功能，下一步将继续改进批题函数，没加":"的代码正常，而不是放在分支里
# 2023.3.31 18:42 准备做：扩展功能、更新功能


# 以下是检查更新功能函数的代码



# 定义其他函数
def expand():  # 扩展函数,去github获取文件
    tk_expand = tkinter.Toplevel()  # 此版本没有此功能，仅创建一个窗口，1.x.x.x版本更新扩展
    tk_expand.title('扩展(实验性)')
    tk_expand_label = tkinter.Label(
        tk_expand, text='此版本暂无扩展,请等待1.x.x.x版本发布', font=('等线', 15))
    tk_expand_label.grid(row=0, column=0)
    tk_expand_button = tkinter.ttk.Button(
        tk_expand, text='关闭', command=tk_expand.destroy)
    tk_expand_button.grid(row=1, column=0)

def get_list():  # 将软件设置从文件读取到列表中
    global f, i, a, f2_t_subframe, l, b, tk, set_list, tk_frame1, tk_frame2, tk_frame3, f1_score1, f1_score2, f2_counter,\
        f2_score_label, f2_t_del, f2_subframe_list, f2_t_label, f2_t_com, f2_t_com_b, f2_t_jp_com, f2_t_jp_com_b,\
        f2_button_add, f3_cb1, f3_cb1_, f3_b, f2_counter
    try:
        os.popen("md set").read()
        f = open("set\common.ini", "r", encoding='utf-8')
        for i in f.read().split("\n"):
            if len(i.split(':')) == 2:
                set_list.append(i.split(':'))
        f.close()
    except:
        try:
            f = open("set\common.ini", "w", encoding='utf-8')
            f.close()
        except:
            a = tkinter.messagebox.askyesno(
                "提示", "请使用管理员权限启动此软件！\n点击\"是\"打开帮助文档，点击\"否\"关闭软件")
            if a:
                os.popen("如何启用管理员权限.txt")
                tk.destroy()
            else:
                tk.destroy()


def open_help_txt():  # 打开帮助文档
    os.popen('帮助.docx')


def save_list():  # 将软件设置从列表保存到文件中，一更改设置就执行一次此函数
    try:
        os.popen("md set").read()
        f = open('set\common.ini', 'w', encoding='utf-8')
        for i in set_list:
            f.write(':'.join(i)+"\n")
        f = open('set\jp_set.ini', 'w', encoding='utf-8')
        for i in f2_t_jp_com:
            f.write('-'.join([','.join(i[0]), ','.join(i[1])])+'\n')  # 存储截屏参数
        f.close()
    except:
        tkinter.messagebox.showinfo('提示', '暂无权限保存设置，请使用管理员权限启动此软件')


def plus_topic():  # 增加小题，小题的labelframe等控件都用列表来动态保存
    global f2_counter
    f2_t_subframe = tkinter.LabelFrame(tk_frame2, bd=0)
    f2_t_subframe.grid(column=f2_counter, row=0)
    f2_subframe_list.append(f2_t_subframe)
    l = tkinter.ttk.Label(
        f2_subframe_list[f2_counter], text="第%s题" % (f2_counter+1))
    l.grid(row=0, column=0)
    f2_t_label.append(l)
    f2_t_com.append("ans=\"abc\":score+=1\n\"abc\" in ans:score+=1")
    l = tkinter.Label(f2_subframe_list[f2_counter], text='此小题分数:0', fg='red')
    l.grid(row=0, column=1)
    f2_score_label.append('')
    b = tkinter.ttk.Button(f2_subframe_list[f2_counter], text='编辑代码和截屏范围')
    b.bind('<1>', command_edit)
    b.grid(row=1, column=0, columnspan=2)
    f2_t_jp_com_b.append(b)
    f2_t_jp_com.append([['0', '0'], ['0', '0']])
    b = tkinter.ttk.Button(f2_subframe_list[f2_counter], text="-")
    b.grid(row=2, column=0, columnspan=2)
    f2_t_del.append(b)
    tk.update()
    f2_counter += 1
    change_command()


def del_topic(e):  # 删除小题，由于技术原因，需要重新读取与构建
    global f2_counter, f2_t_del, f2_subframe_list, f2_t_label, f2_t_com, f2_t_com_b, f2_score_label, f2_t_jp_com, f2_t_jp_com_b
    del_button = e.widget
    name = del_button['text']
    index = f2_t_del.index(del_button)
    f2_subframe_list[index].destroy()
    f2_subframe_list.pop(index)
    f2_t_label.pop(index)
    f2_t_com.pop(index)
    f2_score_label.pop(index)
    f2_t_jp_com.pop(index)
    f2_t_jp_com_b.pop(index)
    f2_t_del.pop(index)
    change_command()  # 将删减后的的列表保存到文件中，再重新读取与构建
    for i in range(len(f2_subframe_list)):  # 循环遍历任意一个列表，将f2内所有的控件全部删除
        f2_subframe_list[i].destroy()
    f2_score_label = []  # 题目（第一题、第二题等）label的列表
    f2_t_del = []  # 删除按钮列表
    f2_subframe_list = []  # frame2中的frame的列表
    f2_t_label = []  # 题目label列表
    f2_t_com = []  # 命令存放列表
    f2_t_com_b = []  # 命令按钮列表
    f2_t_jp_com = []  # 截屏数据列表（二维）
    f2_t_jp_com_b = []  # 截屏按钮列表
    f2_counter = 0
    f = open("set\command_set.ini", "r", encoding='utf-8')  # 重新构建f2
    f1 = f.read()
    f1 = f1.split('\n————\n')[:-1]
    for i in range(len(f1)):
        f2_t_subframe = tkinter.LabelFrame(tk_frame2, bd=0)
        f2_t_subframe.grid(column=i, row=0)
        f2_subframe_list.append(f2_t_subframe)
        f2_counter += 1
    for i in range(len(f1)):
        l = tkinter.ttk.Label(f2_subframe_list[i], text="第%s题" % (i+1))
        l.grid(row=0, column=0)
        f2_t_label.append(l)
        f2_t_com.append(f1[i])
        l = tkinter.Label(f2_subframe_list[i], text='此小题分数:0', fg='red')
        l.grid(row=0, column=1)
        f2_score_label.append(l)
        b = tkinter.ttk.Button(f2_subframe_list[i], text='编辑代码和截屏范围')
        b.grid(row=1, column=0, columnspan=2)
        f2_t_jp_com_b.append(b)
        f2_t_jp_com.append([[0, 0], [0, 0]])
        b = tkinter.ttk.Button(f2_subframe_list[i], text="-")
        b.bind("<1>", del_topic)
        b.grid(row=2, column=0, columnspan=2)
        f2_t_del.append(b)
    f.close()


def change_command():  # 将每个小题的command列表和截屏设置保存到本地的一个设置文件中
    f = open('set\command_set.ini', 'w', encoding='utf-8')
    print(f2_t_com)
    f.write("\n————\n".join(f2_t_com))
    f.write("\n————\n")
    f.close()
    f = open('set\jp_set.ini', 'w', encoding='utf-8')
    for i in f2_t_jp_com:
        f.write('-'.join([','.join(i[0]), ','.join(i[1])])+'\n')  # 存储截屏参数
        # 这有问题（2023.3.23 23:52）
    f.close()


def command_edit(e):  # 命令修改窗口(需将截屏窗口改进)
    global e_  # 存放小题下标
    global tk_edit, tk_edit_jp_entry1_1_1, tk_edit_jp_entry1_1_2, tk_edit_jp_entry1_2_1, tk_edit_jp_entry1_2_2, tk_edit_command_text
    global tk_edit_save_button
    e_ = f2_t_jp_com_b.index(e.widget)
    tk_edit = tkinter.Toplevel(tk)
    # 告诉操作系统使用程序自身的dpi适配
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 获取屏幕的缩放因子
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # 设置程序缩放
    tk_edit.tk.call('tk', 'scaling', ScaleFactor/75)

    tk_edit.resizable(False, False)
    tk_edit.title('设置第%s题的代码和截屏参数' % (e_+1))
    tk_edit_frame1 = tkinter.LabelFrame(tk_edit, bd=0)
    tk_edit_frame1.grid(row=0, column=0)
    tk_edit_jp_tip_label = tkinter.ttk.Label(
        tk_edit_frame1, text='输入要截屏的区域的位置\n软件采用两点确定一个平面,请使用微信截图等软件确定坐标')
    tk_edit_jp_tip_label.grid(row=0, column=0)
    tk_edit_jp_tip_button = tkinter.ttk.Button(
        tk_edit_frame1, text='需要帮助？', command=open_jp_help_txt)
    tk_edit_jp_tip_button.grid(row=0, column=1)
    tk_edit_frame1_x = tkinter.LabelFrame(tk_edit_frame1, bd=0)
    tk_edit_frame1_x.grid(row=1, column=0, columnspan=2)
    tk_edit_frame1_1 = tkinter.LabelFrame(tk_edit_frame1_x, text="左上角:")
    tk_edit_frame1_1.grid(row=0, column=0)
    tk_edit_jp_label1_1_1 = tkinter.ttk.Label(tk_edit_frame1_1, text='X:')
    tk_edit_jp_label1_1_1.grid(row=0, column=0)
    tk_edit_jp_entry1_1_1 = tkinter.ttk.Entry(tk_edit_frame1_1)
    tk_edit_jp_entry1_1_1.grid(row=0, column=1)
    tk_edit_jp_label1_1_2 = tkinter.ttk.Label(tk_edit_frame1_1, text='Y:')
    tk_edit_jp_label1_1_2.grid(row=1, column=0)
    tk_edit_jp_entry1_1_2 = tkinter.ttk.Entry(tk_edit_frame1_1)
    tk_edit_jp_entry1_1_2.grid(row=1, column=1)

    tk_edit_frame1_2 = tkinter.LabelFrame(tk_edit_frame1_x, text="右下角:")
    tk_edit_frame1_2.grid(row=0, column=1)
    tk_edit_jp_label1_2_1 = tkinter.ttk.Label(tk_edit_frame1_2, text='X:')
    tk_edit_jp_label1_2_1.grid(row=0, column=0)
    tk_edit_jp_entry1_2_1 = tkinter.ttk.Entry(tk_edit_frame1_2)
    tk_edit_jp_entry1_2_1.grid(row=0, column=1)
    tk_edit_jp_label1_2_2 = tkinter.ttk.Label(tk_edit_frame1_2, text='Y:')
    tk_edit_jp_label1_2_2.grid(row=1, column=0)
    tk_edit_jp_entry1_2_2 = tkinter.ttk.Entry(tk_edit_frame1_2)
    tk_edit_jp_entry1_2_2.grid(row=1, column=1)

    # 填充原来截屏的数据
    tk_edit_jp_entry1_1_1.insert(0, f2_t_jp_com[e_][0][0])
    tk_edit_jp_entry1_1_2.insert(0, f2_t_jp_com[e_][0][1])
    tk_edit_jp_entry1_2_1.insert(0, f2_t_jp_com[e_][1][0])
    tk_edit_jp_entry1_2_2.insert(0, f2_t_jp_com[e_][1][1])

    tk_edit_frame2 = tkinter.LabelFrame(tk_edit, bd=0)
    tk_edit_frame2.grid(row=1, column=0)
    tk_edit_command_tip_label = tkinter.ttk.Label(
        tk_edit_frame2, text='代码编辑区\n在此区域编辑python代码\n可用变量:score为分数,默认为0 ans为图片识别后此小题的文本')
    tk_edit_command_tip_label.grid(row=0, column=0)
    tk_edit_command_text_frame = tkinter.LabelFrame(tk_edit_frame2, bd=0)
    tk_edit_command_text_frame.grid(row=1, column=0)
    tk_edit_command_text = tkinter.Text(tk_edit_command_text_frame)
    scroll = tkinter.Scrollbar(tk_edit_command_text_frame)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    scroll.config(command=tk_edit_command_text.yview)
    tk_edit_command_text.pack()
    tk_edit_command_text.config(yscrollcommand=scroll.set)
    tk_edit_save_button = tkinter.ttk.Button(
        tk_edit, text='保存', command=tk_edit_save)
    tk_edit_save_button.grid(row=2, column=0)

    tk_edit_command_text.insert('1.0', f2_t_com[e_])


def tk_edit_save():  # 保存更改的内容
    global tk_edit, tk_edit_jp_entry1_1_1, tk_edit_jp_entry1_1_2, tk_edit_jp_entry1_2_1, tk_edit_jp_entry1_2_2, tk_edit_command_text
    f2_t_jp_com[e_][0][0] = tk_edit_jp_entry1_1_1.get()
    f2_t_jp_com[e_][0][1] = tk_edit_jp_entry1_1_2.get()
    f2_t_jp_com[e_][1][0] = tk_edit_jp_entry1_2_1.get()
    f2_t_jp_com[e_][1][1] = tk_edit_jp_entry1_2_2.get()

    f2_t_com[e_] = '\n'.join(tk_edit_command_text.get(
        '1.0', tkinter.END).split('\n')[:-1])

    tk_edit_save_button['text'] = '已保存'
    tk.update()
    for i in range(100):
        tk.update()
        time.sleep(0.01)
    tk_edit_save_button['text'] = '保存'
    change_command()


def open_jp_help_txt():  # 打开截屏帮助文件
    os.popen('截屏帮助.docx')


def search_list(mode, key_value):  # 搜索设置列表，1、3为给键返回值，2、4为给值返回键，3、4为模糊搜索
    return_value = []
    for i in range(len(set_list)):
        if mode == 1:
            if key_value == set_list[i][0]:
                return_value.append(set_list[i][1])
        if mode == 2:
            if key_value == set_list[i][1]:
                return_value.append(set_list[i][0])
        if mode == 3:
            if key_value in set_list[i][0]:
                return_value.append([set_list[i][0], set_list[i][1]])
        if mode == 4:
            if key_value in set_list[i][1]:
                return_value.append([set_list[i][0], set_list[i][1]])
    if len(return_value) == 1:
        return return_value[0]
    else:
        return return_value


def set_list(mode, key, value):
    for i in range(len(set_list)):
        if mode == 1:
            if set_list[i][0] == key:
                set_list[i][1] = value
                return 0
        if mode == 2:
            if set_list[i][1] == key:
                set_list[i][0] = value
                return 0
    raise "DatabaseNotFoundError:数据没有在数据库中找到"


def jieping_com(xy1, xy2):
    pass  # 先截屏，再引用百度api的图片识别,两个变量都是列表，存储x坐标和y坐标


def start_enter():  # 进入总入口，貌似多做了两个函数（）
    global flag, f3_cb1_
    flag = True
    print(f3_cb1_.get())
    if f3_cb1_.get() == 0:
        start1_enter()
    if f3_cb1_.get() == 1:
        start2_enter()


def start1_enter():  # start1的进入函数，采用多线程
    global flag
    flag = True
    threading.Thread(target=start1).start()


def start2_enter():  # start2的进入函数，采用多线程
    global flag
    flag = True
    threading.Thread(target=start2).start()


def start1():  # 批题start1函数
    global f2_t_com, flag
    f3_cb1['state'] = 'disabled'  # 禁用checkbutton,防止改动
    tk.protocol("WM_DELETE_WINDOW", no_closing)  # 这五秒不能关闭窗口
    f3_b['command'] = no_closing  # 防止开多个批题函数，设定一下点击按钮操作
    tk.attributes("-topmost", 1)  # 置顶
    for i in range(5):  # 数秒将键盘焦点（光标）移到题目位置上
        f3_b['text'] = '即将开始自动批题,请立即将键盘焦点切换至题目位置\n此窗口已置顶,距离批题还有%s秒' % (4-i)
        tk.update()  # 刷新一下窗口，防止程序假卡死
        time.sleep(1)  # 倒计时
    f3_b['text'] = '停止批题'  # 将“开始批题”改为“停止批题”
    f3_b['command'] = stop  # 用来结束循环
    tk.protocol("WM_DELETE_WINDOW", stop)  # 将关闭窗口的操作设定为stop函数
    while flag:  # 在每份间循环
        score = 0  # 每份卷子的分数要初始化
        for i in range(len(f2_t_com)):  # 在小题间循环
            text = jieping_com(
                f2_t_jp_com[i][0], f2_t_jp_com[i][1])  # 截屏并识别图片，返回文本
            for o in f2_t_com[i].split('\n'):
                if eval(o[i].split(':')[0]):  # 执行python代码，在之前的基础上改进了一下
                    if len(o[i].split(':')[1].split(';')) > 1:
                        for u in o[i].split(':')[1].split(';'):
                            eval(u)
            f2_score_label[i]['text'] = "得分：%s" % score  # 及时反馈得分
            tk.update()
            time.sleep(0.1)
        f1_score2['text'] = str(score)
        time.sleep(0.1)  # 怕电脑反应不过来
        k.type(str(score))  # 将score的值用键盘打出来
        time.sleep(0.1)  # 怕电脑反应不过来
        k.type('\n')  # 回车进行下一个人的批改
        # 由用户自己设定的等待时间，防止还没刷新就截屏
        time.sleep(int(search_list(1, "mode1waitsec")))
    # 如果循环完至少一遍，程序发现flag已经变成False了，退出循环，执行常规化操作
    f3_b['command'] = start_enter  # 将按下按钮的功能恢复
    f3_b['text'] = '开始批题'  # 开始批题按钮的还原
    tk.protocol('WM_DELETE_WINDOW', tk.destroy)
    f3_cb1['state'] = 'normal'  # 让check button的功能正常
    tk.attributes("-topmost", 0)  # 取消置顶


def start2():
    global f2_t_com, flag, start2_t
    f3_cb1['state'] = 'disabled'  # 禁用checkbutton,防止改动
    tk.attributes("-topmost", 1)  # 置顶
    f3_b['text'] = '停止批题'  # 将“开始批题”改为“停止批题”
    f3_b['command'] = stop  # 用来结束循环
    tk.protocol("WM_DELETE_WINDOW", stop)  # 将关闭窗口的操作设定为stop函数
    keyboard.hook(start2_callback)
    while flag:
        while start2_t <= int(search_list(1, "mode2waitsec")):  # 和start1一样，根据用户设定的等待时间来等待
            start2_t += 1
            time.sleep(1)
        score = 0  # 每份卷子的分数要初始化
        for i in range(len(f2_t_com)):  # 在小题间循环
            text = jieping_com(
                f2_t_jp_com[i][0], f2_t_jp_com[i][1])  # 截屏并识别图片，返回文本
            for o in f2_t_com[i].split('\n'):
                if eval(o[i].split(':')[0]):  # 执行python代码，在之前的基础上改进了一下
                    if len(o[i].split(':')[1].split(';')) > 1:
                        for u in o[i].split(':')[1].split(';'):
                            eval(u)
            f2_score_label[i]['text'] = "得分：%s" % score  # 及时反馈得分
            tk.update()
        # 这里不将t设置为0是因为防止过了时间后重复截屏


def start2_callback():
    global start2_t
    start2_t = 0


def stop():
    global flag
    flag = False
    f3_b['text'] = '正在停止...'
    f3_b['command'] = no_closing
    tk.update()


def no_closing():  # 定义一个不可关闭的函数
    pass


def expand():  # 扩展函数,去github获取文件
    pass  # 此版本没有此功能


# 定义变量
set_list_start = [['mode1waitsec', 3], [
    'mode2waitsec', 6]]  # 定义初始值，防止后面有bug时文件丢失
start2_t = 0  # 存放2模式下未点击键盘的秒数
e_ = 0  # 存放点击编辑代码的小题的列表下标
f2_counter = 0  # 用来记录添加题目的数目
f2_score_label = []  # 题目（第一题、第二题等）label的列表
f2_t_del = []  # 删除按钮列表
f2_subframe_list = []  # frame2中的frame的列表
f2_t_label = []  # 题目label列表
f2_t_com = []  # 命令存放列表
f2_t_com_b = []  # 命令按钮列表
f2_t_jp_com = []  # 截屏数据列表（二维）
f2_t_jp_com_b = []  # 截屏按钮列表
set_list = []
# 主窗口
tk = tkinter.Tk()
# 告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 获取屏幕的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 设置程序缩放
tk.tk.call('tk', 'scaling', ScaleFactor/75)
tk.resizable(False, False)
tk.title("自动批题软件-V1.0.0.1")
get_list()
tk_frame1 = tkinter.LabelFrame(tk, bd=0)
tk_frame1.grid(row=0, column=0)
tk_frame2 = tkinter.LabelFrame(tk, bd=0)
tk_frame2.grid(row=2, column=0, columnspan=2)
tk_frame3 = tkinter.LabelFrame(tk, bd=0)
tk_frame3.grid(row=4, column=0, columnspan=2)
# 功能按钮labelframe
func_frame = tkinter.LabelFrame(tk, bd=0)
func_frame.grid(row=0, column=1)
# "?"帮助按钮
help_button = tkinter.ttk.Button(
    func_frame, text='需要帮助？', command=open_help_txt)
help_button.grid(row=0, column=0)
# "扩展”按钮
expand_button = tkinter.ttk.Button(func_frame, text='扩展(实验性)', command=expand)
expand_button.grid(row=1, column=0)
# frame1
f1_score1 = tkinter.Label(tk_frame1, text="分数：", font=("等线", 30), fg="red")
f1_score1.pack()
f1_score2 = tkinter.Label(tk_frame1, text="0", font=("等线", 45), fg="red")
f1_score2.pack()
# frame2
try:
    f = open("set\command_set.ini", "r", encoding='utf-8')
    f_ = open('set\jp_set.ini', 'r', encoding='utf-8')
    f1 = f.read()
    f1 = f1.split('\n————\n')[:-1]
    f1_ = f_.read()
    f1_ = f1_.split('\n')[:-1]
    # print(f1_)
    f1__ = []
    for i in f1_:
        # print(i.split('-')[0].split(','))
        f1__.append([i.split('-')[0].split(','), i.split('-')[1].split(',')])
    for i in range(len(f1)):
        f2_t_subframe = tkinter.LabelFrame(tk_frame2, bd=0)
        f2_t_subframe.grid(column=i, row=0)
        f2_subframe_list.append(f2_t_subframe)
        f2_counter += 1
    for i in range(len(f1)):
        l = tkinter.ttk.Label(f2_subframe_list[i], text="第%s题" % (i+1))
        l.grid(row=0, column=0)
        f2_t_label.append(l)
        f2_t_com.append(f1[i])
        l = tkinter.Label(f2_subframe_list[i], text='此小题分数:0', fg='red')
        l.grid(row=0, column=1)
        f2_score_label.append(l)
        b = tkinter.ttk.Button(f2_subframe_list[i], text='编辑代码和截屏范围')
        b.bind('<1>', command_edit)
        b.grid(row=1, column=0, columnspan=2)
        f2_t_jp_com_b.append(b)

        b = tkinter.ttk.Button(f2_subframe_list[i], text="-")
        b.bind("<1>", del_topic)
        b.grid(row=2, column=0, columnspan=2)
        f2_t_del.append(b)
    f.close()
    f_.close()
except BaseException as error:
    tkinter.messagebox.showerror(
        '提示', '软件发生错误,请手动打开设置文件将文件内容删除！\n错误原因:%s' % error)
    f = open("set\command_set.ini", "w", encoding='utf-8')
    f.close()
f2_t_jp_com = f1__  # 缺少与截屏文件的保存与读取(已修复)
f2_button_add = tkinter.ttk.Button(tk_frame2, text='+', command=plus_topic)
f2_button_add.grid(row=0, column=1000)
# frame3
f3_cb1_ = tkinter.IntVar()
f3_cb1 = tkinter.ttk.Checkbutton(
    tk_frame3, variable=f3_cb1_, text='勾选自动批题，不勾选辅助批题')
f3_cb1.pack()
f3_b = tkinter.ttk.Button(tk_frame3, text='开始批题', command=start_enter)
f3_b.pack()
print(f2_t_com)
threading.Thread(target=check_update).start()
tk.mainloop()
