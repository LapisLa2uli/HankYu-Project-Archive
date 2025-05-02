**PWord&Rating**

`Concreteness_ratings.xlsx`

```         
a list of words and its concreteness, and is used to calculated the concreteness score in `fill2024info.py` 
```

`delete_tagged.py`

```         
Deletes p-words that have most of is usages deemed as false positives
```

`fill2024info.py`

```         
adds average rating score, concreteness and flesch reading ease scores (DEPRECATED, alternative in R WIP) to newly added 2024 papers in ICLR_OUT.csv
```

`GetFreq.py`

```         
This code calculates PWord occurrences in the papers, mainly for added papers from 2024.
```

`hype_list_pg.py`

```         
Provides a list of hype words
```

`ICLR (1).csv`

```         
Original data from the google drive of the information for each paper
```

`ICLR_2024_reviews.csv`

```         
Reviews of 2024 ICLR papers.
```

`ICLR_OUT.csv`

```         
Processed form of `ICLR (1).csv`, added pWord occurrences for 2024 papers
```

`ICLR_OUT_FILLED.csv`

```         
Product of `fill2024info.py`, for specific added features see its description
```

`ICLR_OUT_original.csv`

```         
Backup for `ICLR_OUT.csv`
```

`ICLR_OUT_TRIMMED.csv`

```         
product of `delete_tagged.py`. For specific added features refer to its description
```

`LogisticRegression.py`

```         
DEPRECATED AND OBSOLETE --- This aims to create a logistic regression model of average score of papers and the frequency of hype words of them
```

`Ordered_Logistic_Regression.R`

```         
Uses ICLR_OUT_FILLED.csv to construct ologit regression models. This produces the main results of the project. This code requires Precess_Data.R to be ran prior, without cleaning the workspace.
```

`Process_Data.R`

```         
Calculates average reader confidence for each paper.
```

`pWordVsRating.pdf`

```         
(OBSOLETE) a product of Ordered_Logistic_Regression.R, it is a collection of ologit graphs of groups of papers with same year and team size.
```

`ScatterPlot.py`

```         
DEPRECATED AND OBSOLETE --- visualizes the correlation between average score and frequency of hype words in each paper
```

`TotalFreq.py`

```         
calculates total number of hype words and subsequently the frequency of hype words in each paper
```
