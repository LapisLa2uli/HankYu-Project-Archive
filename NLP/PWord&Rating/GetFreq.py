'''This code calculates PWord occurrences in the papers'''
import pandas,os,shutil,spacy
nlp = spacy.load("en_core_web_sm")
from hype_list_pg import hype_list
df=pandas.read_csv("D://stuff//NLP//PWord&Rating//ICLR (1).csv")
print(df)
print(list(df['id']))
newWords=['optimal','various']
os.chdir('D://stuff//NLP//ICLR papers')
'''for word in newWords:
    df.insert(list(df.columns).index('total_num_hype_words'),word,[0 for i in range(len(df))])'''
print(list(df.columns))
for folder in os.listdir('D://stuff//NLP//ICLR papers'):
    for paper in os.listdir(folder):
        with open(os.path.abspath(folder)+'\\'+paper,'r',encoding='utf-8') as f:
            txt=f.read()
            f.close()
        '''if paper[:-4] not in list(df['forum']):
            print(paper[:-4],'NOT IN')
            doc=nlp(txt)
            pwordDict={}
            for word in hype_list:
                pwordDict[word]=0
            for token in doc:
                # Check if the token is an adjective
                if token.pos_ == "ADJ":
                    # Find the noun that the adjective is modifying
                    for child in token.head.children:
                        if child.dep_ == "amod" and:  # 'amod' stands for adjectival modifier
                            if token.text in hype_list:
                                pwordDict[token.text]+=1
            outDict=pwordDict.copy()
            outDict['forum']=paper[:-4]
            df=df._append(outDict,ignore_index=True)
            print(len(df))'''#OBSOLETE
        doc = nlp(txt)
        pwordDict = {}
        for word in hype_list:
            pwordDict[word] = 0
        for token in doc:
            # Check if the token is an adjective
            if token.pos_ == "ADJ":
                # Find the noun that the adjective is modifying
                for child in token.head.children:
                    if child.dep_ == "amod":  # 'amod' stands for adjectival modifier
                        if token.text in hype_list:
                            pwordDict[token.text] += 1
        outDict = pwordDict.copy()
        outDict['forum'] = paper[:-4]
        df = df._append(outDict, ignore_index=True)

        print(os.path.abspath(folder)+'\\'+paper)
        txt=txt.split()
        '''for word in hype_list:
            print(word,txt.count(word))'''
df.to_csv("D://stuff//NLP//PWord&Rating//ICLR_OUT_original.csv") # This is the back-up file; the file originally exported to is ICLR_OUT.csv