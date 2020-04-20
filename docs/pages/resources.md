---
title: Resources
permalink: /resources
nav_order: 5
---

# Linguistic resources

As in the previous edition, the corpus for eHealth-KD 2020 will be extracted from MedlinePlus sources.
This platform freely provides large health textual data from which we have made a selection for constituting the eHealth-KD corpus. The selection has been made by sampling specific XML files from the collection available in the [Medline website](https://medlineplus.gov/xml.html).

> "MedlinePlus is the National Institutes of Health's Website for patients and their families and friends. Produced by the National Library of Medicine, the world’s largest medical library, it brings you information about diseases, conditions, and wellness issues in language you can understand. MedlinePlus offers reliable, up-to-date health information, anytime, anywhere, for free." [1]

These files contain several entries related to health and medicine topics and have been processed to remove all XML markup to extract the textual content. Only Spanish language items were considered. Once cleaned, each individual item was converted to a plain text document, and some further post-processing is applied to remove unwanted sentences, such as headers, footers and similar elements, and to flatten HTML lists into plain sentences. The final documents are manually tagged using Brat by a group of annotators. After tagging, a post-processing was applied to Brat’s output files (ANN format) to obtain the output files in the formats described in this document.

> **NOTE:** The resulting documents and output files are distributed along with the Task. There is no need for participants to download extra data from MedlinePlus servers, since all the input is already distributed.

## Corpus data

The corpus will be divided into three sections. Training and development sets will be published along with baseline implementations, for participants to train and fine-tune their systems. These files will consist of both plain text input and the expected outputs for both subtasks. Afterward, a small test set will be released, with plain text only, further divided into 3 sub-sets, one for each scenario. Participants are expected to submit the corresponding output files to Codalab.

In no case, participants will be able to access the correct output files for the test set before the challenge ends. Afterward, the full corpus, including Brat-annotated files will be freely available under a suitable license for the research community.

### Download links:

All data is available in the [Github repository](https://github.com/knowledge-learning/ehealthkd-2020) of the project. Individual download links are listed below for ease of use.

### Training and development

The eHealth-KD Corpus is distributed free of charge under a Creative Commons Non-Commercial Share-Alike 4.0 License.

To accept the distribution terms, please fill in the following form:
> [https://forms.gle/pUJutSDq2FYLwNWQA](https://forms.gle/pUJutSDq2FYLwNWQA)

The **training** set contains a total of 800 sentences manually annotated in [BRAT](http://brat.nlplab.org/).
These sentences are expected to be used for training machine learning systems.
An additional 200 **sentences** are available in the development set.
These additional sentences are expected to be used for evaluating machine learning systems and tune their hyperparameters.

### Transfer learning corpora

An additional 100 sentences extracted from the Spanish version of Wikinews are available for cross-validation purposes, to evaluate transfer learning approaches (folder `data/development/transfer`). Your system is **not supposed** to be trained on these sentences, but rather, trained **only** on the 800 training sentences from Medline. You should use these sentences only for evaluation and cross-validation (i.e., hyperparameter tunning). Hence, your system should be able to learn from one domain (Medline) and generalize to new unseen domains (Wikinews) without further training. This is to encourage participants to design systems that can be broadly applied to new domains.

### Testing input files

The testing files are provided in the folder `data/testing`. As explained in the [subtasks page](https://knowledge-learning.github.io/ehealthkd-2020/tasks#challenge-scenarios), they are divided into 4 scenarios. In each scenario's folder, you will find plain text files, and specifically for scenario 3, the gold annotations for task A.

Please refer to the [submission instructions](https://knowledge-learning.github.io/ehealthkd-2020/submission) for additional details.

The following files are provided:

* `scenario1-main`: 
    * `scenario.txt`: 5000 sentences from medline. You should perform **tasks A and B** and generate the corresponding file in `submissions/<your-team>/test/<run>/scenario1-main/scenario.ann`.
    * `scenario.ann`: This annotations file is empty.
* `scenario2-taskA`:
    * `scenario.txt`: 100 sentences from medline. You should perform **task A** and generate the corresponding `submissions/<your-team>/test/<run>/scenario2-taskA/scenario.ann`.
    * `scenario.ann`: This annotations file is empty.
* `scenario3-taskB`:
    * `scenario.txt`: 100 sentences from medline. You should perform **task B** and generate the corresponding `submissions/<your-team>/test/<run>/scenario3-taskB/scenario.ann`.
    * `scenario.ann`: This annotations file contains the **gold output from task A** for this scenario.
* `scenario4-transfer`:
    * `scenario.txt`: 1500 sentences from wikipedia and wikinews. You should perform **task A and B** and generate the corresponding `submissions/<your-team>/test/<run>/scenario4-transfer/scenario.ann`.
    * `scenario.ann`: This annotations file is empty.

⚠️ **NOTE**: In scenarios 1 and 4, respectively, 5000 and 1500 plain text sentences are provided, but only 100 of these are actually evaluated. However, the exact sentences that will be evaluated are not disclosed to discourage manual annotation by participants and fine-tunning on the test set. Hence, your submission **must annotate all sentences** in each scenario.

### Automatic corpora

Using the submissions from the past edition, we built an ensemble of all participant systems and automatically annotated 3000 additional sentences (folder `data/ensemble`). These sentences **have not** been manually revised, so they should not be considered gold standard. We invite you to evaluate if using these sentences for training improves your validation score. 

A file (`data/ensemble/ensemble.scr`) is provided with a numerical score for each sentence (in the same order they appear in the plain text file). This score is based on the agreement of the ensembled systems, i.e., a score of 0.5 means that on average 50% of the systems agree on each annotation. The score is **not** an indication of quality of the annotation, since no human review has been performed, but a smaller score should be correlated with a less accurate annotation. Use at your own risk.

## Evaluation scripts

Evaluation scripts will be provided so that participants can test offline their systems with respect to the same metrics used in the challenge. Since participants will not have access to the test gold annotations, their offline performance will need to be evaluated in the development set. This metric will not be exactly the same as the one obtained in the test set, but it should serve for participants to compare different strategies and perform hyper-parameter tunning.

### **Download links**:

The evaluation is available in the [Github repository](https://github.com/knowledge-learning/ehealthkd-2020) of the project, in the file `script/evaltest.py`.
A detailed explanation is available in the [Submission section](/submission).

## Baselines

A simple baseline will be released along with the corpus. The baseline source code will be freely available as well. The baselines performance on the development and the test set will be published.

### **Download links**:

The evaluation is available in the [Github repository](https://github.com/knowledge-learning/ehealthkd-2020) of the project, in the file `script/baseline.py`.
A detailed explanation is available in the [Submission section](/submission).

# Additional resources

Participants may freely use any additional resources they consider necessary to improve their systems, from other corpora (annotated or not), to external knowledge either explicitly (i.e., using knowledge bases) or implicitly (i.e., captured in word embeddings). For the purpose of sharing the results we expect participants to fully disclose everything they use.
However, participants may not manually annotate the test set, since doing so would be in violation of the ethics of the competition. Furthermore, we expect participants to perform all the fine tuning using only the training and development, and then perform one single run in the test set for submission, so that no accidental overfitting occurs in the test set.

## References

**[1]**   MedlinePlus (Internet). Bethesda (MD): National Library of Medicine (US). Available from: [https://medlineplus.gov/](https://medlineplus.gov/).
