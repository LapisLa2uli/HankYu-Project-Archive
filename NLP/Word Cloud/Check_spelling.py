import enchant
directory = r"D:\stuff\NLP\2017 Papers\TXT"
rfile=open('Noun_cloud_ICLR2018.txt','r',encoding='utf-8')
nounDict={}
d=enchant.Dict('en_US')
lines=rfile.readlines()
for i in range(0,len(lines),2):
    nounDict[lines[i][:-1]]=lines[i+1][:-1].split()
rfile.close()
nounDict2=nounDict.copy()
for key in nounDict.keys():
    try:
        if d.check(key)==False:
            del nounDict2[key]
    except:
        del nounDict2[key]
wFile=open('Noun_cloud_ICLR2018.txt','w',encoding='utf-8')
ansStr=''
for key,value in nounDict2.items():
    ansStr+=key+'\n'+' '.join(value)+'\n'
wFile.write(ansStr)
wFile.close()
