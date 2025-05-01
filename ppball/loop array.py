qList=[i+1 for i in range(16)]
cnt=0
while len(qList)>1:
    cnt=(cnt+4)%len(qList)
    qList.pop(cnt)
print(qList[0])

qList=[1 for i in range(16)]
cnt=-1
while qList.count(1)>1:
    for i in range(5):
        while qList[(cnt+1)%16]==0:
            cnt+=1
        cnt+=1
        cnt%=16
    qList[cnt]=0
print(qList.index(1)+1)