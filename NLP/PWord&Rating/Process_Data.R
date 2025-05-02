# Load the main paper data
data1 <- read.csv("D:\\stuff\\NLP\\PWord&Rating\\ICLR_OUT.csv", header=TRUE, stringsAsFactors=FALSE)

# Initialize columns:
# - 'num_reviews' to store how many reviews each paper has
# - 'confidence' to accumulate confidence scores
data1$num_reviews = rep(0, 16440)
data1$confidence = rep(0, 16440)

# Loop over the years from 2018 to 2024 to read review data for each year
for (i in seq.int(from = 2018, to = 2024)) {
  
  # Read the review file for the given year
  data <- read.csv(sprintf("D:\\stuff\\NLP\\ICLR Reviews\\ICLR_%.0f_reviews.csv", i))
  
  # Remove NAs (though this doesn't modify 'data' unless reassigned)
  na.omit(data)
  
  print(i)  # Show the current year
  
  # Loop over each review entry in the review file
  for (y in seq.int(from = 1, to = length(data$confidence))) {
    
    # Proceed only if:
    # - The paper ID (forum) exists in data1
    # - The confidence field is not NA
    if (is.element(data$forum[y], data1$forum) && !is.na(data$confidence[y])) {
      
      #print(data$forum[y])  # Print forum ID (paper ID)
      
      # Get the position/index of the paper in data1
      Pos = which(data1$forum == data$forum[y])
      #print(Pos)
      
      # Loop through characters in the confidence field to extract the first digit (assumed to be the confidence score)
      for (pointer in seq.int(from = 0, to = nchar(data$confidence[y]))) {
        
        # Check if the character is a digit
        if (grepl('1|2|3|4|5|6|7|8|9|0', substr(data$confidence[y], start = pointer, stop = pointer))) {
          
          # Extract the digit and convert to numeric
          #print(substr(data$confidence[y], start = pointer, stop = pointer))
          data1$confidence[Pos] = data1$confidence[Pos] + as.numeric(substr(data$confidence[y], start = pointer, stop = pointer))
          
          # Increment the review counter
          data1$num_reviews[Pos] <- data1$num_reviews[Pos] + 1
          #print(data1$num_reviews[Pos])
          break  # Stop after the first digit is found
        }
      }
    } else {
      print(data$forum[y])  # Print unmatched or invalid forum ID
    }
  }
}

# Calculate average confidence by dividing the total confidence by the number of reviews
data1$confidence = data1$confidence / data1$num_reviews
# 
# # omit false positives
# # Assume 'merged_freq' is already calculated as before
# # Assume 'data1' is your dataframe
# #This part of code needs to be run after get_FP_rate in the Word Cloud folder
# 
# # Step 1: Make a named vector of True Positive Percentages
# tp_percent <- setNames(merged_freq$True_Positive_Percentage / 100, merged_freq$Adj) 
# # (dividing by 100 to turn % into proportion)
# 
# # Step 2: Find which columns in data1 are adjectives (i.e., columns present in tp_percent)
# adj_cols <- intersect(names(data1), names(tp_percent))
# 
# # Step 3: Multiply only adjective columns by their corresponding True Positive proportion
# data1[adj_cols] <- lapply(adj_cols, function(col) data1[[col]] * tp_percent[[col]])



# Remove any rows with NA values (e.g., those with zero reviews or missing fields)
data1 = na.omit(data1)

# After this, the user is directed to run the ordered logistic regression script
# Ordered_Logistic_Regression.R
