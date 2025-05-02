# Import the OS module for file and directory operations
import os

wordList = []  # Will store a list of dictionaries: one per year, each with adjective -> frequency mapping

# Loop through all files in the current directory
for file in os.listdir():
    Dict = {}       # Dictionary to store adjective -> frequency for current file
    ansStr = ''     # Will hold the CSV-formatted string

    # Skip non-.txt files and misc. txt files
    if file[-4:] != '.txt' or file == 'New Promotional Words.txt':
        continue

    # Read the contents of the frequency file
    with open(file, 'r', encoding='utf-8') as f:
        txt = f.readlines()

    # Process each line of the file (format: frequency adjective)
    for line in txt:
        line = line.strip().split()  # Split line into [frequency, adjective]
        Dict[line[1]] = eval(line[0])  # Store in dictionary (eval converts string to float)
        ansStr += f'{line[1]},{line[0]}\n'  # Prepare CSV line: adjective,frequency

    wordList.append(Dict)  # Add the dictionary for this year to the main list

    # Save the processed data to a .csv file (same name, different extension)
    with open(f'{file[:-4]}.csv', 'w', encoding='utf-8') as f:
        f.write(ansStr)

# Now compare the first and last year’s dictionaries for adjectives that increased in usage
ansStr = ''  # Will store comparison results in CSV format

# Loop through each adjective in the last year's dictionary
for word in wordList[-1].keys():
    try:
        # Check if the word exists in both first and last year
        if wordList[-1][word] and wordList[0][word]:
            ansStr += f'{word},{int(wordList[0][word])},{int(wordList[-1][word])}\n'  # CSV format
            print(word, int(wordList[0][word]), int(wordList[-1][word]))  # Print change
    except:
        pass  # Silently skip words not found in the first year

# Write the comparison of adjectives to a summary CSV file
with open('adj_and_freqs.csv', 'w', encoding='utf-8') as f:
    f.write(ansStr)
