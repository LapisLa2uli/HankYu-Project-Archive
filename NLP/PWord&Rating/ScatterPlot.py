'''DEPRECATED AND OBSOLETE --- visualizes the correlation between average score and frequency of hype words in each paper'''
import matplotlib.pyplot as plt
import pandas
import numpy
df=pandas.read_csv("ICLR_OUT.csv")
print(df)
XList=[]
YList=[]
for i in range(len(df)):
    if numpy.isnan(df.loc[i,"avg_score"]):
        break
    XList.append(df.loc[i,"frac_hype_words"])
    YList.append(df.loc[i,"avg_score"])
print(XList,YList)
print(YList[-1]==float('nan'))
plt.scatter(XList,YList)
plt.show()