import random
a=eval(input('amount of questions: '))
op=input('enter the operations needed (no spaces!) ')
opList=list(op)
print(opList)
for i in range(a):
    print(random.randint(1,1000),opList[random.randint(0,len(opList)-1)],random.randint(1,1000),end='')
    if i%2==0:
        for i in range(3):
            print('\t',end='')
        else:
            print()
