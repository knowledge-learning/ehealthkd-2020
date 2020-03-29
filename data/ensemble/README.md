# Automatic corpus

Using the submissions from the past edition, we built an ensemble of all participant systems and automatically annotated 3000 additional sentences. These sentences **have not** been manually revised, so they should not be considered gold standard. We invite you to evaluate if using these sentences for training improves your validation score. 

The file `ensemble.scr` is provided with a numerical score for each sentence (in the same order they appear in the plain text file). This score is based on the agreement of the ensembled systems, i.e., a score of 0.5 means that on average 50% of the systems agree on each annotation. The score is **not** an indication of quality of the annotation, since no human review has been performed, but a smaller score should be correlated with a less accurate annotation. Use at your own risk.
