#-*-coding:utf-8-*-
import _thread
import time
import ctypes
import tkinter as tk
from webbrowser import open as webopen
from searcher import Search
from sieve import Sieve
import _thread
import tkinter.messagebox
import os

EDGE=100
urls={}
flag=[False]

class Win(tk.Tk, object):
    def __init__(self):
        super(Win, self).__init__()
        self.title('SD Finder')
        moni=ctypes.windll.user32
        global wt
        global ht
        wt=moni.GetSystemMetrics(0)
        ht=moni.GetSystemMetrics(1)
        self._build_win()
        #self.geometry('{0}x{1}'.format(10 * 30, 10 * 30))
        self.resizable(False,False)
    
    def _build_win(self):
        self.geometry("{0}x{1}+{2}+{3}".format(EDGE*5,EDGE*5,int((wt-EDGE*5)/2),int((ht-EDGE*5)/2)))
        self.b1=tk.Scrollbar(self,width=20)
        self.b1.pack(side = tk.RIGHT, fill = tk.Y)
        self.lb = tk.Listbox(self,yscrollcommand=self.b1.set,height=30,width=30)
        self.lb.pack(side=tk.RIGHT)
        self.b1.config(command=self.lb.yview)
        self.refresh=tk.Button(self,text='刷新',command=lambda:Refresh(self))
        self.sieve=tk.Button(self,text='筛除',command=lambda:_thread.start_new_thread(Sieve_,(root,)))
        self.search=tk.Button(self,text='搜索',command=lambda:_thread.start_new_thread(Search_,(root,)))
        self.stop=tk.Button(self,text='停止',command=Stop)
        self.refresh.pack()
        self.sieve.pack()
        self.search.pack()
        self.b2=tk.Scrollbar(self,width=20)
        self.b2.pack(side=tk.LEFT, fill=tk.Y)
        self.lb2 = tk.Listbox(self,yscrollcommand=self.b2.set,height=20,width=30)
        self.lb2.pack(side=tk.LEFT)
        self.b2.config(command=self.lb2.yview)
        self.refresh.place(x=20,y=10)
        self.sieve.place(x=20,y=50)
        self.search.place(x=20,y=90)
        self.lb2.place(x=20,y=120)
        self.b2.place(x=0,y=120,height=EDGE*5-120)
        self.stop.place(x=60,y=10)
        self.text_low=tk.StringVar()
        self.text_low.set("10000")
        self.low=tk.Entry(self,textvariable=self.text_low)
        self.text_high=tk.StringVar()
        self.text_high.set("30000")
        self.high=tk.Entry(self,textvariable=self.text_high)
        self.low.place(x=60,y=90,width=50)
        self.high.place(x=120,y=90,width=50)

def Run(root):
    while True:
        if root.lb.curselection()!=():
            choice=root.lb.curselection()[0]
            print(choice)
            webopen(urls[choice])
        root.lb.select_clear(0,tk.END)
        time.sleep(0.2)

def Refresh(root):
    if not os.path.exists('web_list.txt'):
        return
    with open('web_list.txt','r',encoding='utf-8') as f:
        root.lb.delete(0,tk.END)
        lines=f.readlines()
        for i,line in enumerate(lines):
            root.lb.insert(i,line)
            urls[i]=line
        n=len(lines)
        if n<root.lb.size():
            root.lb.delete(n,tk.END)

def Stop():
    flag[0]=True
    root.lb2.insert(tk.END,"Stopping the proccess, please wait.")

lock=False

def Sieve_(root):
    global lock
    if(lock):
        tk.messagebox.showinfo("Locked!","Please wait or restart the program.")
        return
    lock=True
    flag[0]=False
    try:
        Sieve(flag=flag,lsbox=root.lb2)
        Refresh(root)
    except:
        pass
    lock=False

def Search_(root):
    global lock
    if(lock):
        tk.messagebox.showinfo("Locked!","Please wait or restart the program.")
        return
    lock=True
    flag[0]=False
    try:
        low=int(root.text_low.get())
        high=int(root.text_high.get())
        Search(flag=flag,lsbox=root.lb2,low=low,high=high)
        Refresh(root)
    except:
        pass
    lock=False

if __name__=='__main__':
    root = Win()
    Refresh(root)
    _thread.start_new_thread(Run,(root,))
    root.mainloop()