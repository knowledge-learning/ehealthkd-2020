---
title: Submission
permalink: /submission
nav_order: 4
---

# Submission details

The challenge will be graded on [Codalab]().

A fully working [evaluation script](https://github.com/knowledge-learning/ehealthkd-2020/blob/master/scripts/evaltest.py) is provided to participants, that exactly matches the evaluation formulas used in Codalab.
This way participants will have the possibility to evaluate their systems offline and perform hyper-parameter tuning with respect to the same evaluation metrics as used in the competition.

## Baseline implementation

A [baseline system](https://github.com/knowledge-learning/ehealthkd-2020/blob/master/scripts/baseline.py) is provided for participants to compare their results. If necessary, feel free to use the baseline as a starting point for developing your own solution, since the baseline already covers parsing the input and generating output in the correct format.

The baseline implementation is an extremely basic strategy that simply stores all the training, and at test time outputs keyphrases and relations if they exactly match something found in the training.

We recommend all participants to first run the baseline implementation (with the training and development sets) and upload it to Codalab, to get acquainted with the submission process. The following instructions detail this process.

## Running the baseline implementation on the development set

The first step consists in downloading the project and running the baseline implementation.

Clone the `ehealthkd-2020` project from Github:

```bash
$ git clone https://github.com/knowledge-learning/ehealthkd-2020.git
```

Run the baseline implementation for the main scenario. The baseline implementation is in the `scripts/baseline.py` file. The arguments are:

* `--train` to run the baseline on the training collection.
* `--dev` to run the baseline on the development collection.
* `--test` to run the baseline on the test collection.
* `--custom GOLD MODE SCENARIOS` to run the baseline on the `GOLD` collection, across a list of comma-separated `SCENARIOS`, and labeling the output in the submit directory as `MODE`.
    - The configuration `--train` is equivalent to:
        ```
        --custom data/training/scenario.txt train \
            scenario1-main,scenario2-taskA,scenario3-taskB
        ```
    - The configuration `--dev`  is equivalent to:
        ```
        --custom data/development/main/scenario.txt dev    \
            scenario1-main,scenario2-taskA,scenario3-taskB  \
        --custom data/development/transfer/scenario.txt dev  \
            scenario4-transfer
        ``` 
    - The configuration `--test` is equivalent to:
        ```
        --custom data/testing/{0}/scenario.txt test \
            scenario1-main,scenario2-taskA,scenario3-taskB,scenario4-transfer
        ```
    - Subtask A and Subtask B will not be run at scenarios labeled as `scenario3-taskB` and `scenario2-taskA` respectively (nor any other scenario that ends with `-taskB` and `-taskA` respectively).

> The module `scripts.submit` contains the utilities used by the baseline to handle the submission format.

In this case we will train with the `training` set (800 sentences) and evaluate on the `development` set (200 sentences) using the same sentences for the 3 evaluation scenarios. However, in the final TEST phase you will train with both training and development and evaluate on the corresponding test sets (different for each scenario).

Here is a baseline execution example:
```bash
$ cd ehealthkd-2020
# Inside the root folder ehealthkd-2020
$ python3 -m scripts.baseline --dev
```

Then, you can go to `data/submissions/baseline/dev/` and check the corresponding files were generated:
```bash
$ ls -l data/submissions/baseline/dev/scenario1-main
-rw-r--r-- 1 user user  1488 Jan 27 19:01 scenario.ann
-rw-r--r-- 1 user user  8756 Jan 27 19:01 scenario.txt

$ ls -l data/submissions/baseline/dev/scenario2-taskA
-rw-r--r-- 1 user user  1488 Jan 27 19:01 scenario.ann
-rw-r--r-- 1 user user  8756 Jan 27 19:01 scenario.txt

$ ls -l data/submissions/baseline/dev/scenario3-taskB
-rw-r--r-- 1 user user  1488 Jan 27 19:01 scenario.ann
-rw-r--r-- 1 user user  8756 Jan 27 19:01 scenario.txt

$ ls -l data/submissions/baseline/dev/scenario4-transfer
-rw-r--r-- 1 user user  1488 Jan 27 19:01 scenario.ann
-rw-r--r-- 1 user user  8756 Jan 27 19:01 scenario.txt
```

> **(!!!)** Make sure that your files are named _exactly_ as the files above, since the evaluation script in Codalab will expect these filenames.

> **(!!!)** Also make sure that you have the file `scenario.txt` with the input sentences in your submission folder. This is the _exact_ same file you processed as input, so you can just copy and paste it. The baseline script already handles this. This is necessary for the evaluation script to guarantee that you have the right sentences.

### Evaluating the main scenario

Now you can run the evaluation script offline just to check your results. The evaluation script is in the file `scripts/score.py` and the arguments are:

* The gold annotations (in this case, `data/development/input_develop.txt`).
* Your system's annotations (`data/submit/scenario1-main/output_scenario1.txt`)

The evaluation script outputs the total number of correct, incorrect, partial, missing and spurious matches for each subtask, and the final score as defined in the [Evaluation section](/evaluation).

```bash
$ python3 -m scripts.score data/development/input_develop.txt data/submit/scenario1-main/output_scenario1.txt

correct_A: 368
incorrect_A: 42
partial_A: 32
spurious_A: 267
missing_A: 162
correct_B: 44
spurious_B: 95
missing_B: 493
--------------------
recall: 0.3751
precision: 0.5047
f1: 0.4304
```

> **NOTE:** The exact numbers you see with the baseline may vary, as the evaluation script and/or the baseline implementation can suffer changes as we discover bugs or mistakes. These numbers are for illustrative purposes only. The actual scores are the ones published in Codalab.

Additionally, you can pass `--verbose` if you want to see detailed information about which keyphrases and relations were correct, missing, etc.

```bash
$ python3 -m scripts.score --verbose data/development/input_develop.txt data/submit/scenario1-main/output_scenario1.txt

===================  MISSING_A   ===================

Keyphrase(text='enfrentar', label='Action', id=3)
Keyphrase(text='tubos', label='Concept', id=7)
Keyphrase(text='filtran', label='Action', id=10)
Keyphrase(text='limpian', label='Action', id=11)
Keyphrase(text='eliminando', label='Action', id=13)

... LOTS OF OUTPUT

===================  MISSING_B  ===================

Relation(from='producen', to='genes', label='subject')
Relation(from='producen', to='proteínas', label='target')
Relation(from='producen', to='correctamente', label='in-context')
Relation(from='trastorno', to='niño', label='target')
Relation(from='trastorno', to='genético', label='in-context')
Relation(from='producen', to='trastorno', label='causes')
Relation(from='producen', to='trastorno', label='causes')
--------------------
recall: 0.3751
precision: 0.5047
f1: 0.4304
```

### Evaluating the optional scenarios

You can also (optionally) perform just subtask A or subtask B, writing the results to the corresponding folders.

For subtask A, the output folder is `submit/scenario2-taskA` and the dev file is `output_scenario2.txt`. Pass `--skip-B` to the baseline script to skip the output for subtask B. Again, we will be reusing the `development` set in this case, but in the TEST phase there will be an additional 100 sentences just for this scenario.

```bash
$ python3 -m scripts.baseline --skip-B data/training/input_training.txt data/development/input_develop.txt data/submit/scenario2-taskA/output_scenario2.txt
```

> **(!!!)** When submitting to subtask A, please make sure to write an **empty `output_b_scenario2.txt`** file. This file will not be taken into consideration when evaluating this scenario but is necessary for the evluation script when it parses the results. The baseline implementation already takes care of this detail.

You can evaluate just scenario 2 with the evaluation script by passing `--skip-B`:

```bash
$ python3 -m scripts.score --skip-B data/development/input_develop.txt data/submit/scenario2-taskA/output_scenario2.txt

correct_A: 368
incorrect_A: 42
partial_A: 32
spurious_A: 267
missing_A: 162
--------------------
recall: 0.6358
precision: 0.5416
f1: 0.5849
```

For subtask B, the output folder is `submit/scenario3-taskB` and the dev file is `output_scenario3.txt`. Pass `--skip-A` to the baseline script to skip the output for subtask B. Again, we will be reusing the `development` set in this case, but in the TEST phase there will be an additional 100 sentences just for this scenario.

```bash
$ python3 -m scripts.baseline --skip-A data/training/input_training.txt data/development/input_develop.txt data/submit/scenario3-taskB/output_scenario3.txt
```

> **(!!!)** When submitting to subtask B, please make sure to **copy the `output_a_scenario3.txt`** file _from the gold annotations_. This is the same as the `output_a_develop.txt` file in this case. This file will not be taken into consideration when evaluating this scenario but is necessary for the evaluation script when it parses the results. The baseline implementation already takes care of this detail.

> **(!!!)** When submitting to subtask B, make sure to **reuse the keyphrase ID** provided in the `output_a_develop.txt` (or corresponding TEST file) from the gold annotations. The baseline implementation already takes care of this detail.

You can evaluate just scenario 2 with the evaluation script by passing `--skip-A`:

```bash
$ python3 -m scripts.score --skip-A data/development/input_develop.txt data/submit/scenario3-taskB/output_scenario3.txt

correct_B: 50
spurious_B: 32
missing_B: 487
--------------------
recall: 0.09311
precision: 0.6098
f1: 0.1616
```

If you have succesfully generated the output files for all the scenarios, you should have the following structure in the `data/submit` folder:

```bash
$ ls -lR data/submit/*/
data/submit/scenario1-main/:
total 40
-rw-rw-r-- 1 user user 21604 abr 18 16:50 output_a_scenario1.txt
-rw-rw-r-- 1 user user  1488 abr 18 16:50 output_b_scenario1.txt
-rw-rw-r-- 1 user user  8756 abr 18 16:50 output_scenario1.txt

data/submit/scenario2-taskA/:
total 36
-rw-rw-r-- 1 user user 21604 abr 18 16:51 output_a_scenario2.txt
-rw-rw-r-- 1 user user     0 abr 18 16:51 output_b_scenario2.txt
-rw-rw-r-- 1 user user  8756 abr 18 16:51 output_scenario2.txt

data/submit/scenario3-taskB/:
total 36
-rw-rw-r-- 1 user user 19744 abr 18 16:51 output_a_scenario3.txt
-rw-rw-r-- 1 user user   764 abr 18 16:51 output_b_scenario3.txt
-rw-rw-r-- 1 user user  8756 abr 18 16:51 output_scenario3.txt
```

## Running the baseline on the test set

Once the test set input files are released, you will be able to test the baseline implementation on the test set as well. [Please read the details about the test set structure](resources#test-data).

These are the necessary steps:

Run the baseline on the test scenario 1 (this may take a couple minutes):

```bash
$ python3 -m scripts.baseline data/training/input_training.txt data/testing/scenario1-main/input_scenario1.txt data/submit/scenario1-main/output_scenario1.txt
```

Run the baseline on the test scenario 2, skipping subtask B:

```bash
$ python3 -m scripts.baseline --skip-B data/training/input_training.txt data/testing/scenario2-taskA/input_scenario2.txt data/submit/scenario2-taskA/output_scenario2.txt
```

> **(!!!)** Remember that for scenario 2 the file `output_b_scenario2.txt` **must exist** and **be empty**. The baseline already does this, but ensure your own implementation takes it into consideration.

Run the baseline on the test scenario 3, skipping subtask A:

```bash
$ python3 -m scripts.baseline --skip-A data/training/input_training.txt data/testing/scenario3-taskB/input_scenario3.txt data/submit/scenario3-taskB/output_scenario3.txt
```

> **(!!!)** Remember that for scenario 3 the file `output_a_scenario3.txt` **must exist** and **be an exact copy** of the provided file `data/testing/scenario3-taskB/output_a_scenario3.txt`. The baseline already does this, but ensure your own implementation takes it into consideration.

Once finished, you can submit your results to Codalab.

Remember that for the duration of the challenge the results for the test set will be hidden and only shown after the competition ends.

However, you will receive error notifications if your upload is invalid. You have up to **100** different submissions.

## Submitting your results to Codalab

> The file [submit_baseline_dev.zip](https://github.com/knowledge-learning/ehealthkd-2019/blob/master/data/submit/submit_baseline_dev.zip) contains an example submission for the TRAINING phase.

> The file [submit_baseline_test.zip](https://github.com/knowledge-learning/ehealthkd-2019/blob/master/data/submit/submit_baseline_test.zip) contains an example submission for the TEST phase.

Once you have all the corresponding outputs, please bundle the content of the submit folder in a `.zip` file:

```bash
$ cd data/submit
$ zip -r submit.zip *
```

> **(!!!)** Make sure you zip **the content** of the `submit` folder, and not the `submit` _itself_. When in doubt, `cd` into `data/submit` and run `zip` there. The idea is that the root of your `submit.zip` file should directly contain the three folders `scenario1-main`, etc., and **not** a `submit` folder.

### Structure of the submit folder

For recap here is the expected structure of the `submit.zip` file:

* **Folder `scenario1-main`**:
    * **File `output_a_scenario1.txt`**: Your output for subtask A.
    * **File `output_b_scenario1.txt`**: Your output for subtask B.
    * **File `output_scenario1.txt`**: Sentences, copied verbatim from input.

* **Folder `scenario2-taskA`**:
    * **File `output_a_scenario2.txt`**: Your output for subtask A.
    * **File `output_b_scenario2.txt`**: Empty file, but must exist.
    * **File `output_scenario2.txt`**: Sentences, copied verbatim from input.

* **Folder `scenario3-taskB`**:
    * **File `output_a_scenario3.txt`**: Output for subtask A, copied verbatim from input.
    * **File `output_b_scenario3.txt`**: Your output for subtask B.
    * **File `output_scenario3.txt`**: Sentences, copied verbatim from input.

> **NOTE:** For reference purposes, inside the `data/submit` folder you will find a `submit_baseline_dev.zip` file that corresponds to running the baseline following these instructions. Follow the structure of that file if in doubt.

> **(!!!)** Please double-check the files for all three scenarios, including the `output_scenario*.txt` files, the empty `output_b_scenario2.txt` and the copied `output_a_scenario3.txt`. If you do not plan to participate in any given scenario, kindly reuse the baseline output then, to avoid the evaluation script from raising errors about missing files.

### Uploading your results to the competition server

Please also make sure to fill-in this [Google Form](https://forms.gle/3KHAvo7e5MfxtnME9) to accept the license terms for the corpus.

Go to the [Codalab competition page](https://competitions.codalab.org/competitions/21781) and register if you have not done so already.
In Codalab, go to the [Participate](https://competitions.codalab.org/competitions/21781#participate-submit_results) section and enter the details of your submission:

* **Team name.**
* **Method name:** a short, memorable name for the technique you are presenting.
* **Method description:** refers to the type of techniques used. Please write a summary (~200 words) of the techniques, algorithms or approaches used. Also specify if you use external sources (other corpora, knowledge bases, etc.).
Finally, attach one or more of the following tags regarding techniques and/or resources used in your approach. These tags will help us better understand which approaches are more popular or perform better in this task in the future.

    * **K:** knowledge-bases
    * **S:** Shallow supervised methods (i.e., _logistic regression_, _SVM_, _Markov models_, _CRF_, ...)
    * **D:** Deep supervised methods (e.g, _CNNs_, _LSTMs_, ...)
    * **U:** Unsupervised methods (e.g. clustering or dimensionality reduction techniques, ...)
    * **E:** Embeddings (e.g., _word2vec_, _BERT_, _ELMo_, ...)
    * **N:** Standard NLP techniques (pos-tagging, _AMR_ parsing, dependency parsing, _NER_, ...)
    * **R:** Hand-crafted rules

Finally hit the submit button and attach you zip file. If everything is ok, after a few seconds hit the **Submit to leaderboard** button at the bottom of the page to see your results.

## Final words

> **DISCLAIMER:** The scoring you achieve during the training phase is only for your own reference, and should not be taken as an indication that you will achieve a similar score in the test phase. Particularly, participants that achieve the highest scores in the training phase are **not guaranteed** to win in the TEST phase, since participating in the training phase is completely optional. Likewise, at any point we may decide to change the evaluation script, including during the blind TEST phase, if we discover any kind of bug or error. We will inform you if that's the case and provide an updated evaluation script.

Finally, if you discover a mistake in the evaluation script, please let us know at [ehealth-kd@googlegroups.com](mailto:ehealth-kd@googlegroups.com) or post an issue on our [Issues Page](https://github.com/knowledge-learning/ehealthkd-v2/issues) in Github.
