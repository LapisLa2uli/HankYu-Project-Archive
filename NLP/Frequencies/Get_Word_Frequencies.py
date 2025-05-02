# Import required libraries
import os
import spacy

# Load the English spaCy model for natural language processing
nlp = spacy.load("en_core_web_sm")

# Change the working directory to the folder containing yearly paper directories
os.chdir('D://stuff//NLP//ICLR papers')

wordList = []  # This will store the adjective frequency dictionary for each year

# Loop through each directory
for directory in os.listdir():
    Dict = {}  # Dictionary to store raw word frequencies
    length = 0  # Total number of words in all papers of the current directory/year

    # Loop through each paper in the current year's directory
    for paper in os.listdir(directory):
        with open(directory + '//' + paper, encoding='utf-8') as f:
            txt = f.read().split()  # Read the paper and split into words
        length += len(txt)  # Accumulate the total word count
        for word in txt:
            if word in Dict:
                Dict[word] += 1  # Increment the word count
            else:
                Dict[word] = 1  # Add new word with initial count

    print(length)  # Print total word count for this year

    # Convert raw counts to frequency per million words
    for key in Dict.keys():
        Dict[key] /= length
        Dict[key] *= 1_000_000  # Normalize to "per million words"

    cnt = 0  # Counter for how many adjectives have been selected
    ansDict = {}  # Dictionary to store the top adjectives and their frequencies

    # Loop to extract top 100 adjectives by frequency
    while cnt < 100:
        # Find the word with the highest frequency
        word, freq = max(Dict, key=Dict.get), Dict[max(Dict, key=Dict.get)]
        del Dict[max(Dict, key=Dict.get)]  # Remove it from the dictionary

        pWord = nlp(word)  # Run spaCy's NLP on the word

        # Check if the word is an adjective
        if pWord[0].pos_ == "ADJ":
            ansDict[word] = freq  # Store it in the answer dictionary
            print(freq, word)  # Print frequency and adjective
            cnt += 1  # Increment adjective counter

    wordList.append(ansDict)  # Store the current year's adjectives and frequencies

    # Save the result to a text file for the current year
    with open('D://stuff//NLP//Frequencies//' + directory + '.txt', 'w', encoding='utf-8') as f:
        ansStr = ''
        for key in ansDict:
            ansStr += f'{ansDict[key]} {key}\n'  # Format: frequency adjective
        f.write(ansStr)  # Write to file

    print()  # Print a blank line for readability between years

print()  # Final separation

# Compare adjectives from the last year to the first year
# Print any adjective whose frequency increased
for word in wordList[-1].keys():
    if wordList[-1][word] > wordList[0][word]:
        print(word)