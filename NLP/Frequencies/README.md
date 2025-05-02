**Frequencies**

`ICLR<year>.txt` contain adjectives used in papers in the year along with its frequency per million words. It has the same content as `ICLR<year>.csv` only with the order of columns inverted

`Get_Word_Frequencies.py` produces `ICLR<year>.txt` using `ICLR papers`

`cmp_word_frequencies.py` transforms `ICLR<year>.txt` into its csv form, and print all words that have risen in usage, and stores it in `adj_and_freqs.csv`
