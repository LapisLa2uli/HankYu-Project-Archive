from os import listdir
print('importing spaCy')
import spacy
print('initializing GPU...')
#spacy.require_gpu()
print('GPU initialized')
print('importing model...')
# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")
# Example sentence
sentence = "The beautiful park had a large tree."

# Process the sentence with spaCy
doc = nlp(sentence)

# Loop through each token (word) in the sentence
for token in doc:
    # Check if the token is an adjective
    if token.pos_ == "ADJ":
        # Find the noun that the adjective is modifying
        for child in token.head.children:
            if child.dep_ == "amod":  # 'amod' stands for adjectival modifier
                print(f"Adjective: {token.text}, Modifies Noun: {token.head.text}")
# Import module
import os

# Assign directory
directory = r"D:\stuff\NLP\2018 Papers\TXT"
rfile=open('Noun_cloud_ICLR2018.txt','r',encoding='utf-8')
lines=rfile.readlines()
nounDict={}
for i in range(0,len(lines),2):
    nounDict[lines[i][:-1]]=lines[i+1][:-1].split()
rfile.close()
flag=0
# Iterate over files in directory
for name in os.listdir(directory):
    # Open file
    with open(os.path.join(directory, name),encoding='utf-8') as f:
        print(f"Content of '{name}'")
        content=f.read()
        f.close()
        doc = nlp(content)
        wList=[]
        # Loop through each token (word) in the sentence
        for token in doc:
            # Check if the token is an adjective
            if token.pos_ == "ADJ":
                # Find the noun that the adjective is modifying
                for child in token.head.children:
                    if child.dep_ == "amod":  # 'amod' stands for adjectival modifier
                        if token.head.text.isalpha():
                            try:
                                nounDict[token.text.lower()].append(token.head.text.lower())
                            except KeyError:
                                nounDict[token.text.lower()]=[token.head.text.lower()]
wFile=open('Noun_cloud_ICLR2018.txt','w',encoding='utf-8')
ansStr=''
for key,value in nounDict.items():
    ansStr+=key+'\n'+' '.join(value)+'\n'
wFile.write(ansStr)
wFile.close()


