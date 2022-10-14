import _thread
from urllib import request
import time
import tkinter as tk

ban=['Bad Gateway','Internal Server Error','No interface is running right now','"auth_required": true']
requires=['txt2img']
tot=0
def Bing(lsbox,url,f):
    global tot
    global timeset
    # print(id)
    tot+=1
    try:
        rq=request.Request(url)
        rp=request.urlopen(rq)
        rep=rp.read().decode('utf-8')
        # print(rep)
        for ele in  ban:
            if ele in rep:
                tot-=1
                return
        for ele in requires:
            if ele not in rep:
                tot-=1
                return
        if lsbox!=None:
            lsbox.insert(tk.END,"Find "+url)
        f.write(url+'\n')
        f.flush()
        tot-=1
        return
    except:
        tot-=1
        return

def Search(flag,lsbox=None,low=10000,high=30000,maxtot=1000):
    global timeset
    timeset=0
    if lsbox!=None:
        lsbox.insert(tk.END,"Searching from {0} to {1}".format(low,high))
    try:
        f=open("web_list.txt",'r',encoding='utf-8')
        lines=f.readlines()
        f.close()
    except:
        lines=[]
    f=open("web_list.txt",'a',encoding='utf-8')
    for i in range(low,high+1):
        if(flag[0]):
            break
        while tot>maxtot:
            continue
        # print(i)
        url="https://{0}.gradio.app/".format(i)
        if url in lines:
            continue
        _thread.start_new_thread(Bing,(lsbox,url,f))
        time.sleep(0.005)
    time.sleep(0.5)
    while tot>0:
        continue
    f.close()
    if lsbox!=None:
        lsbox.insert(tk.END,"Searching Over")