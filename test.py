import _thread
import time
def A(a):
    while(True):
        print(a[0])
        time.sleep(0.5)
if __name__=='__main__':
    tmp=[0]
    _thread.start_new_thread(A,(tmp,))
    while(True):
        tmp[0]+=1
        time.sleep(0.5)