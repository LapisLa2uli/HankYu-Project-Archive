df_false <- readxl::read_excel("D:\\stuff\\NLP\\Word Cloud\\Noun_cloud_ICLR2018_FP.xlsx")
df_all <- read.csv("D:\\stuff\\NLP\\Word Cloud\\Noun_cloud_ICLR2018.csv", header=TRUE, stringsAsFactors=FALSE)
# Assume your dataframes are df_all and df_false

# Step 1: Summarize total frequency of each adjective
total_freq <- aggregate(Freq ~ Adj, data = df_all, sum)

# Step 2: Summarize false positive frequency of each adjective
false_freq <- aggregate(Freq ~ Adj, data = df_false, sum)

# Step 3: Merge total and false positive frequencies
merged_freq <- merge(total_freq, false_freq, by = "Adj", all.x = TRUE, suffixes = c("_total", "_false"))

# Step 4: Replace NAs in false frequencies with 0
merged_freq$Freq_false[is.na(merged_freq$Freq_false)] <- 0

# Step 5: Calculate true positive percentage
merged_freq$True_Positive_Percentage <- ((merged_freq$Freq_total - merged_freq$Freq_false) / merged_freq$Freq_total) * 100

# Step 6: View result
print(merged_freq[, c("Adj", "True_Positive_Percentage")])
