f=open('hamlet.txt','r')
content=f.read()
f.close()
wordList=['']
for i in range(len(content)):
    if content[i].isalpha():
        wordList[-1]+=content[i]
    else:
        wordList[-1]=wordList[-1].lower()
        if len(wordList[-1])==1 or wordList[-1] in wordList[:-1]:
            wordList[-1]=''
            continue
        if len(wordList[-1])>0:
            wordList.append('')
wordList.pop(-1)
print(wordList)
f=open('word_cloud.txt','w')
f.write('\n'.join(wordList))
f.close()
