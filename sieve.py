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
    if url in urls:
        return
    tot+=1
    try:
        rq=request.Request(url)
        rp=request.urlopen(rq)
        rep=rp.read().decode('utf-8')
        # print(rep)
        for ele in ban:
            if ele in rep:
                if lsbox!=None:
                    lsbox.insert(tk.END,"Delete "+url)
                # print("del "+url)
                tot-=1
                return
        for ele in requires:
            if ele not in rep:
                if lsbox!=None:
                    lsbox.insert(tk.END,"Delete "+url)
                tot-=1
                return
        if lsbox!=None:
            lsbox.insert(tk.END,"Remain "+url)
        f.write(url+'\n')
        f.flush()
        urls.append(url)
        tot-=1
        return
    except:
        tot-=1
        return

def Sieve(flag,lsbox=None,maxtot=1000):
    global timeset
    global urls
    timeset=0
    if lsbox!=None:
        lsbox.insert(tk.END,"Sieving the urls...")
    try:
        f=open("web_list.txt",'r',encoding='utf-8')
        lines=f.readlines()
        f.close()
    except:
        lines=[]
    f=open("web_list.txt",'w',encoding='utf-8')
    urls=[]
    for line in lines:
        if(flag[0]):
            break
        # print(line)
        while tot>maxtot:
            continue
        url=line.strip('\n')
        _thread.start_new_thread(Bing,(lsbox,url,f))
    time.sleep(0.5)
    while tot>0:
        continue
    f.close()
    if lsbox!=None:
        lsbox.insert(tk.END,"Sieving Over")