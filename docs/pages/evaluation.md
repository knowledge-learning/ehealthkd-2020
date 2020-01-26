---
title: Evaluation
permalink: /evaluation
nav_order: 3
---

<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML'></script>

# Evaluation measures

This challenge proposes a main evaluation scenario (Scenario 1) where both subtasks previously described are performed in sequence. The submission that obtains the highest F1 score for the Scenario 1 will be considered the best overall performing system of the challenge. Additionally, participants will have the opportunity to address specific subtasks by submitting to two optional scenarios, once for each subtask. Scoring tables will be published also for each optional scenario.

## Main Evaluation (Scenario 1)

This scenario evaluates all of the subtasks together as a pipeline. The input consists only of a plain text, and the expected output will be the two output files for Subtask A and B, as described before. The measures will be precision, recall and F1 as follows:

$$Rec_{AB} = \frac{C_A + C_B + \frac{1}{2} P_A}{C_A + I_A + C_B + P_A + M_A + M_B} $$

$$Prec_{AB} = \frac{C_A + C_B + \frac{1}{2} P_A}{C_A + I_A + C_B + P_A + S_A + S_B} $$

$$F_{1AB} = 2 \cdot \frac{Prec_{AB} \cdot Rec_{AB}}{Prec_{AB} + Rec_{AB}} $$

> F1 will determine the ranking of Scenario 1 and consequently of the eHealthKD challenge.

The exact definition of Correct, Missing, Spurious, Partial and Incorrect is presented in the following sections for each subtask.

## Optional Subtask A (Scenario 2)

This scenario only evaluates Subtask A. The input is a plain text with several sentences and the output is as described in Subtask A. To compute the scores we define correct, partial, missing, incorrect and spurious matches. The expected and actual output files do not need to agree on the ID for each phrase, nor on their order. The evaluator matches are based on the START and END values and LABEL. A brief description about the metrics follows:

* **Correct matches** are reported when a text in the dev file matches exactly with a corresponding text span in the gold file in START and END values, and also LABEL. Only one correct match per entry in the gold file can be matched. Hence, duplicated entries will count as Spurious.
* **Incorrect matches** are reported when START and END values match, but not the LABEL.
* **Partial matches** are reported when two intervals [START, END] have a non-empty intersection, such as the case of “vías respiratorias” and “respiratorias” in the previous example (and matching LABEL). Notice that a partial phrase will only be matched against a single correct phrase. For example, “tipo de cáncer” could be a partial match for both “tipo” and “cáncer”, but it is only counted once as a partial match with the word “tipo”. The word “cancer” is counted then as Missing. This aims to discourage a few large text spans that cover most of the document from getting a very high score.
* **Missing matches** are those that appear in the gold file but not in the dev file.
* **Spurious matches** are those that appear in the dev file but not in the gold file.

From these definitions, we compute precision, recall, and a standard F1 measure as follows:

$$Rec_{A} = \frac{C_A + \frac{1}{2} P_A}{C_A + I_A + P_A + M_A} $$

$$Prec_{A} = \frac{C_A + \frac{1}{2} P_A}{C_A + I_A + P_A + S_A} $$

$$F_{1A} = 2 \cdot \frac{Prec_{A} \cdot Rec_{A}}{Prec_{A} + Rec_{A}} $$

> A higher precision means that the number of spurious identifications is smaller compared to the number of missing identifications, and a higher recall means the opposite. Partial matches are given half the score of correct matches, while missing and spurious identifications are given no score.

> F1 will determine the ranking of Scenario 2.

## Optional Subtask B (Scenario 3)

This scenario only evaluates Subtask B. The input is plain text and the correct outputs from Subtask A. The expected output is as described in Subtask C. Similarly to previous scenarios, we define the correct, missing and spurious items, defined as follows:

* **Correct:** relationships that matched exactly to the gold file, including the LABEL and the corresponding IDs for each of the participants.
* **Missing:** relationships that are in the gold file but not in the dev file, either because the LABEL is wrong, or because one of the IDs didn’t match.
* **Spurious:** relationships that are in the dev file but not in the gold file, either because the LABEL is wrong, or because one of the IDs didn’t match.

We define standard precision, recall and F1 metrics as follows:

$$Rec_{B} = \frac{C_B}{C_B + M_B} $$

$$Prec_{B} = \frac{C_B}{C_B + S_B} $$

$$F_{1B} = 2 \cdot \frac{Prec_{B} \cdot Rec_{B}}{Prec_{B} + Rec_{B}} $$

> F1 will determine the ranking of Scenario 3.

> **NOTE**: The Scenario 1 is more complex than solving each optional scenario separately, since errors in subtask A will necessary translate to errors in subtask B. For this reason it is considered the main evaluation metric. Additionally, this scenario also provides the possibility for integrated end-to-end solutions that solve both subtask simultaneously.

## Running the final evaluation script

Now that the challenge is finished, we have published the [official evaluation script](https://github.com/knowledge-learning/ehealthkd-2019/blob/master/scripts/evaltest.py) along with gold files for the test set. This script performs the full evaluation of all scenarios for all submissions and outputs a pretty-printed representation (either JSON or CSV) that you can use to verify your results or test different submissions.

To use it, you need to place all your different submissions inside respective folders with descriptive names~(such as `using-cnn`, `using-crf`, etc.) and all of that inside the `submissions` folder. As an example, when you clone (or pull from) the eHealth-KD repository, you will find inside the `data/submission` folder another subfolder named `baseline` and inside it all three `scenario*` subfolders with the corresponding submissions files. Feel free to add alongside the `baseline` subfolder all your additional submissions.

Then run the following line from the root of the project (i.e., not inside the `scripts` folder):

```bash
$ python -m scripts.evaltest data/submissions data/testing --single --pretty

{
  "submissions": [
    {
      "scenario1": {
        "correct_A": 388,
        "correct_B": 37,
        "f1": 0.43091787439613516,
        "incorrect_A": 32,
        "missing_A": 175,
        "missing_B": 539,
        "partial_A": 42,
        "precision": 0.5204200700116686,
        "recall": 0.3676834295136026,
        "spurious_A": 268,
        "spurious_B": 90,
        "submit": "baseline"
      },
      "scenario2": {
        "correct_A": 355,
        "correct_B": 0,
        "f1": 0.5466377440347071,
        "incorrect_A": 35,
        "missing_A": 210,
        "missing_B": 592,
        "partial_A": 46,
        "precision": 0.5128900949796472,
        "recall": 0.5851393188854489,
        "spurious_A": 301,
        "spurious_B": 0,
        "submit": "baseline"
      },
      "scenario3": {
        "correct_A": 615,
        "correct_B": 40,
        "f1": 0.12307692307692308,
        "incorrect_A": 0,
        "missing_A": 0,
        "missing_B": 528,
        "partial_A": 0,
        "precision": 0.4878048780487805,
        "recall": 0.07042253521126761,
        "spurious_A": 0,
        "spurious_B": 42,
        "submit": "baseline"
      },
      "submit": "baseline"
    }
  ]
}
```

As output you will get all the submissions (subfolders inside `data/submissions`) evaluated on each scenario, with several detailed metrics, such as correct, incorrect, missing and spurious matches, as well as precision, recall and F1. Feel free to use these metrics in your system description paper as you see fit.

Finally run `python -m scripts.evaltest -h` to see all options for the evaluation script, it also provides CSV output and it automatically generates a table with the best submission for each scenario.
