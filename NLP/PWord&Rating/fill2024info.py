'''This code adds average rating score, concreteness and flesch reading ease scores (DEPRECATED, alternative in R WIP) to newly added 2024 papers in ICLR_OUT.csv'''
# Import required libraries
import textstat       # For computing readability metrics like Flesch Reading Ease
import pandas         # For handling CSV and Excel files as DataFrames
import os             # For navigating the file system
import math           # For checking for NaN values
import re             # For regex-based text cleaning
import nltk           # For tokenization
from nltk.tokenize import word_tokenize

# Download the Punkt tokenizer model required by nltk
nltk.download('punkt_tab')

def load_concreteness_lexicon(filepath):
    """
    Load the concreteness lexicon from an Excel file.
    Assumes the file contains a column 'Word' and a column 'Conc.M' (mean concreteness rating).
    Returns a dictionary mapping words to their concreteness scores.
    """
    df = pandas.read_excel(filepath)
    lexicon = {}
    for row in df.index:
        lexicon[df.loc[row, 'Word']] = df.loc[row, 'Conc.M']
    return lexicon

def calculate_concreteness_score(text, lexicon):
    """
    Calculate the average concreteness score of a given text using the provided lexicon.
    Tokenizes the text, cleans the words, and averages scores of matching words.
    """
    words = word_tokenize(text.lower())  # Tokenize and lowercase text
    words = [re.sub(r'[^a-z]', '', word) for word in words]  # Remove punctuation and non-letters
    words = [word for word in words if word]  # Remove empty strings

    # Collect concreteness scores for words found in the lexicon
    scores = [lexicon[word] for word in words if word in lexicon]

    if not scores:
        return None  # Return None if no words matched

    return sum(scores) / len(scores)  # Return average score

# Read in metadata and reviews
print('reading ICLR_OUT.csv...')
df = pandas.read_csv("ICLR_OUT.csv")  # DataFrame with paper metadata

print('reading ICLR_2024_reviews.csv...')
reviewdf = pandas.read_csv('ICLR_2024_reviews.csv')  # DataFrame with review scores

# Load concreteness lexicon
print('loading concreteness lexicon...')
lexicon = load_concreteness_lexicon('Concreteness_ratings.xlsx')

# Change working directory to where the paper text files are stored
os.chdir('D:\\stuff\\NLP\\ICLR papers\\ICLR2024')

# Read full text of all papers into a dictionary {paper_id: paper_text}
paperDict = {}
print('reading papers...')
for paper in os.listdir('.'):
    with open(paper, encoding='utf-8') as f:
        paperDict[paper[:-4]] = f.read()  # Strip ".txt" from filename

errorList = []

# Process each paper in the metadata DataFrame
for i in df.index:
    paperid = df.loc[i, 'forum']
    print(f'processing {paperid}')
    
    # Check if the paper text is available
    if paperid not in paperDict.keys():
        print(f'ERROR {paperid}')
        errorList.append(paperid)
        continue

    print(i)
    
    # Add Flesch Reading Ease score if missing
    if math.isnan(df.loc[i, 'flesch_reading_ease']):
        df.loc[i, 'flesch_reading_ease'] = textstat.flesch_reading_ease(paperDict[paperid])
    
    # Add average review score if missing
    if math.isnan(df.loc[i, 'avg_score']):
        ratings = list(reviewdf.loc[reviewdf['forum'] == paperid]['rating'])
        for i in range(len(ratings)):
            ratings[i] = int(ratings[i][11])  # Extract numerical score from format like 'Rating: 7'
        if len(ratings) != 0:
            print(1)
            df.loc[i, 'avg_score'] = sum(ratings) / len(ratings)
    
    # Add concreteness score if missing
    if math.isnan(df.loc[i, 'concreteness']):
        print(2)
        df.loc[i, 'concreteness'] = calculate_concreteness_score(paperDict[paperid], lexicon)

# Display the tail of the updated DataFrame
print(df.tail)

# Save the filled DataFrame to a new CSV
os.chdir('D:\\stuff\\NLP\\PWord&Rating')
df.to_csv('ICLR_OUT_FILLED.csv', index=False)

# Print any papers that had issues (e.g., not found)
print('List of erroneous paper ids: ', ' '.join(errorList))
