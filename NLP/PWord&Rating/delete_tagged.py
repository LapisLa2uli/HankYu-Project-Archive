'''Deletes p-words that have most of is usages deemed as false positives'''
import pandas
df=pandas.read_csv("ICLR_OUT.csv")
print(df)
words=['first','effective','international']
for i in range(len(df)):
    '''ans=0
    for word in words:
        ans+=df.loc[i,word]'''
    df.loc[i,"total_num_hype_words"]=sum(list(df.iloc[i,139:141]))
    if df.loc[i,"num_words"]==0:
        df.loc[i, "frac_hype_words"]=0
    else:
        df.loc[i, "frac_hype_words"] = df.loc[i,"total_num_hype_words"]/df.loc[i,"num_words"]
df.to_csv("ICLR_OUT_TRIMMED.csv",index=False)