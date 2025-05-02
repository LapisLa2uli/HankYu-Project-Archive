import enchant
from hype_list_pg import hype_list
rfile=open('Noun_cloud_ICLR2018 - 副本 (2).txt','r',encoding='utf-8')
nounDict={}
d=enchant.Dict('en_US')
lines=rfile.readlines()
for i in range(0,len(lines),2):
    nounDict[lines[i][:-1]]=lines[i+1][:-1].split()
rfile.close()
for key,value in nounDict.items():
    if key not in hype_list:
        continue
    Dict={}
    for item in value:
        if item in Dict:
            Dict[item]+=1
        else:
            Dict[item]=1
    ansStr=''
    while len(Dict)>0:
        if d.check(max(Dict,key=Dict.get)):
            ansStr+=key+','+max(Dict,key=Dict.get)+','+str(max(Dict.values()))+'\n'
        del Dict[max(Dict,key=Dict.get)]
    nounDict[key]=ansStr
print(nounDict['neural'])
wFile=open('Noun_cloud_ICLR2018.csv','w',encoding='utf-8')
ansStr='Adj,N,Freq\n'
for key,value in nounDict.items():
    try:
        ansStr+=value
    except:
        continue
wFile.write(ansStr)
wFile.close()