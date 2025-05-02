'''This code is to check if there are 3 reviews for each paper'''
# Import the pandas library for data handling
import pandas

# Iterate over each year from 2017 to 2021 (inclusive)
for year in range(2017, 2022):
    paperList = []  # Initialize a list to keep track of papers with fewer than 3 reviews
    dataframe = pandas.read_csv(f'ICLR_{year}_reviews_GH.csv')  # Load the CSV file for the given year
    titleList = list(dataframe['title'])  # Extract the 'title' column as a list
    ans = 0  # Initialize a counter to sum reviews of papers with fewer than 3 reviews
    row = 0  # Initialize the row index
    illegalList = ['N/A | OpenReview', 'NA | OpenReview']  # List of invalid titles (not used in logic)

    # Loop through each row in the title list
    while row < len(titleList):
        title = titleList[row]  # Get the title at the current row

        # Checks if title is nan, and print it if it is
        if title == float('nan'):
            print(title)

        # Check if the current title appears fewer than 3 times and hasn’t been processed before
        if titleList.count(title) < 3 and title not in paperList:
            paperList.append(title)  # Add this paper title to the list of under-reviewed papers
            ans += titleList.count(title)  # Add the number of reviews it does have

            # Attempt to drop all rows with this title from the dataframe
            i = row
            while titleList[i] == title:
                dataframe = dataframe.drop(i)  # Drop the row at index i
                i += 1
            row -= 1  # Adjust the row index to account for removed entries

        row += 1  # Move to the next row

    # Print the current year
    print(year)
    # Print all paper titles that had fewer than 3 reviews
    for paper in paperList:
        print(paper)
    # Print the cleaned dataframe (with low-review papers removed)
    print(dataframe)

    # Refresh titleList after possible removals
    titleList = list(dataframe['title'])

    # Check for papers that have an incorrect number of reviews (not exactly 3)
    for title in titleList:
        if titleList.count(title) > 3 or titleList.count(title) < 2:
            pass  # Placeholder for potential debugging output

    # Optional: save the cleaned dataframe to a new file
    # dataframe.to_csv(f'ICLR_{year}_reviews_GH - copy.csv')