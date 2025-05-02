
# Python program to generate WordCloud

# importing all necessary modules
'''from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
'''
# Reads 'Youtube04-Eminem.csv' file
'''df = pd.read_csv(r"Noun_cloud_ICLR2017.csv", encoding ="utf-8")

comment_words = ''
stopwords = set(STOPWORDS)

# iterate through the csv file
print(df.size,df.shape,list(df.iloc[0])[0]*list(df.iloc[0])[2])
words=''
print('importing...')
for i in range(df.shape[0]):
    if i%1000==0:
        print(f'processing... (i={i})')
    words+=(list(df.iloc[0])[0]+' ')*list(df.iloc[0])[2]'''
'''with open('example.txt') as f:
    words=f.read()
    f.close()
print('import complete!')'''
'''wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='white',
                      stopwords = stopwords,
                      min_font_size = 10).generate(words)'''
'''with open('temp.txt','w') as f:
    f.write(words)
    f.close()'''

'''wordcloud=WordCloud().generate(words)
print('showing word cloud...')
# plot the WordCloud image
plt.imshow(wordcloud)
plt.show()'''
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Read the text file
with open('temp.txt') as f:
    words = f.read()

# Generate the word cloud
wordcloud = WordCloud(background_color='white').generate(words)
wordcloud.to_file('wordcloud.png')
# Create a figure for the word cloud
plt.figure(figsize=(10, 10))  # Set figure size
plt.imshow(wordcloud, interpolation='bilinear')  # Display the image with interpolation
plt.axis("off")  # Turn off axis
print('showing word cloud...')
plt.show()  # Show the plot