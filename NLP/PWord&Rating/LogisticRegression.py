'''DEPRECATED AND OBSOLETE --- This aim to create a logistic regression model of average score of papers and the frequency of hype words of them'''
import numpy
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
import pandas
import matplotlib.pyplot as plt
from scipy.special import expit
df=pandas.read_csv("ICLR_OUT.csv")
print(df)
XList=[]
YList=[]
for i in range(len(df)):
    if numpy.isnan(df.loc[i,"avg_score"]):
        break
    if numpy.isnan(df.loc[i,"frac_hype_words"]):
        continue
    if df.loc[i,"frac_hype_words"]>0.04:
        continue
    XList.append(float(df.loc[i,"frac_hype_words"]))
    YList.append(int(df.loc[i,"count_as_pass"]))
XList=[1,2,3,4,5]
YList=[0,0,1,1,1]
print(XList,YList)

XList=numpy.array(XList).reshape(-1,1)
YList=numpy.array(YList)
print(XList)
print(numpy.isnan(YList).any())
logr = linear_model.LogisticRegression()
logr.fit(XList, YList)
plt.scatter(XList.ravel(), YList, label="example data", color="black", zorder=20)
X_test = numpy.linspace(0, max(XList), 300)
loss = expit(X_test * logr.coef_ + logr.intercept_).ravel()
plt.plot(X_test, loss, label="Logistic Regression Model", color="red", linewidth=3)
plt.show()