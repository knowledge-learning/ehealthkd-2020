# Testing data

This folder contains the test data for the challenge.
The instructions for submission are provided in the [documentation](https://knowledge-learning.github.io/ehealthkd-2020/submission)

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
