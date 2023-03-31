import tkinter
import tkinter.ttk


def stop():
    global flag
    flag = True


def start():
    global flag


tk = tkinter.Tk()
tk.title('正在关闭...')
label = tkinter.Label(tk, text='正在关闭...')
label.grid(row=0, column=0)
button = tkinter.ttk.Button(tk, text='取消')
button.grid(row=1, column=0)
tk.mainloop()
