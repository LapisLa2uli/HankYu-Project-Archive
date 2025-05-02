'''calculates total number of hype words and subsequently the frequency of hype words in each paper'''
import pandas
df=pandas.read_csv("ICLR_OUT.csv")
print(df)
for i in range(len(df)):
    df.loc[i,"total_num_hype_words"]=sum(list(df.iloc[i,:141]))
    df.loc[i, "frac_hype_words"] = df.loc[i,"total_num_hype_words"]/df.loc[i,"num_words"]
df.to_csv("ICLR_OUT.csv",index=False)