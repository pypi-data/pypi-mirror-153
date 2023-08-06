def show_step(step:int):
    print("hell",end="")
    print((8-step)*' ',end='')
    print(step*'-')

def diaosigui(use_windows=True,ans="purple"):
    a=['_']*len(ans)
    lt=[]
    #final=""
    step=0
    show_step(step)
    for i in a:print(i,end="")
    print()
    for i in lt:print(i+' ',end="")
    print()
    #reply=input("guess a letter:")
    correct=0
    while(step<=8 and correct<len(ans)):
        #final=""
        reply=input("guess a letter:")
        if(len(reply)==1):
            if(reply in ans and(not reply in a)):
                for i in range(len(ans)):
                    if ans[i]==reply:a[i]=reply;correct+=1
                
            else:
                step+=1
                lt.append(reply)
        else:
            if(reply==ans):pass#final=reply
            else:step+=1
        if(use_windows):
            import os
            os.system("cls")
        show_step(step)
        for i in a:
            print(i,end="")
        print()
        for i in lt:print(i+' ',end="")
        print()
    if(correct==len(ans)): print("you win!!!!!!!!")
    else: print("you lose!!!!!")
    if(use_windows):import os;os.system("pause")

if __name__=="__main__":
    diaosigui()
