---
title: Home
permalink: /
nav_order: 0
---

# IberLEF eHealth-KD 2020: eHealth Knowledge Discovery

Natural Language Processing (NLP) methods are increasingly being used to mine knowledge from unstructured health texts. Recent advances in health text processing techniques are encouraging researchers and health domain experts to go beyond just reading the information included in published texts (e.g. academic manuscripts, clinical reports, etc.) and structured questionnaires, to discover new knowledge by mining health contents. This has allowed other perspectives to surface that were not previously available.

Over the years many eHealth challenges have taken place, which have attempted to identify, classify, extract and link knowledge, such as Semevals, CLEF campaigns and others.

The eHealth-KD 2020 proposes --as the previous editions [eHealth-KD 2019](https://knowledge-learning.github.io/ehealthkd-2019) and [eHealth-KD 2018](http://www.sepln.org/workshops/tass/2018/task-3/)--  modeling the human language in a scenario in which Spanish electronic health documents could be machine readable from a semantic point of view. With this task, we expect to encourage the development of software technologies to automatically extract a large variety of knowledge from eHealth documents written in the Spanish Language.

Even though this challenge is oriented to the health domain, the structure of the knowledge to be extracted is general-purpose. The semantic structure proposed models four types of information units. Each one represents a specific semantic interpretation, and they make use of thirteen semantic relations among them. The following sections provide a detailed presentation of each unit and relation type. An example is provided in the following picture.

![](img/task_b.png)

This challenge can be of interest for experts in the field of natural language processing, specifically for those working on automatic knowledge extraction and discovery. It is not a requirement to have expertise in health texts processing for dealing with the eHealth-KD task, due to the general purpose of the semantic schema defined. Nevertheless, eHealth researchers could find interesting this challenge to evaluate their technologies that rely on health domain knowledge.

**Novelties**. This edition will involve an additional scenario in which an alternative domain (not health related) will be evaluated, to experience with transfer learning techniques. In addition, [COVID-19](https://en.wikipedia.org/wiki/Coronavirus_disease_2019) related documents, i.e. news and documentation, will be played.
![](img/COVID-19.png)

## Description of the Subtasks

To simplify the evaluation process, two subtasks are presented:

1. [Entity recognition](tasks#subtask-a-entity-recognition)
2. [Relation extraction](tasks#subtask-b-relation-extraction)

## Submissions and evaluation

There are four evaluation scenarios:

1. [A main scenario covering both tasks](tasks#main-evaluation-scenario-1)
2. [An optional scenario evaluating subtask A](tasks#optional-subtask-a-scenario-2)
3. [An optional scenario evaluating subtask B](tasks#optional-subtask-b-scenario-3)
4. [An optional scenario in a completely different domain](tasks#optional-alternative-domain-evaluation-scenario-4)

The challenge will be graded in Codalab.

* [Submission instructions are provided here](submission)

## Resources

All the data will be made available to participants in due time. This includes training, development and test data, as well as evaluation scripts and sample submissions. [More details are provided here](resources).

## Schedule

### News 

* Due to the potential difficulties caused by COVID-19 to participants,
  we are **delaying all dates** starting with the test set release **2 weeks** into the future.
* COVID19 related documents, i.e. news and documentation, will be played.
* An additional 100 sentences extracted from the Spanish version of Wikinews are available for cross-validation purposes, to evaluate transfer learning approaches (folder `data/development/transfer`) [(read more)](resources#transfer-learning-corpora).
* An additional 3000 automatically annotated sentences from Medline are available for further training. Note that these sentences have been manually revised and hence are not considered gold standard [(read more)](resources#automatic-corpora).

|Date|Event|Link|
|---|---|---|
| 03&nbsp;Feb&nbsp;2020 | Training and development data ready                                 | [📝 Sign Corpus License](https://forms.gle/pUJutSDq2FYLwNWQA)<br>[🏃‍ Training and dev data](https://github.com/knowledge-learning/ehealthkd-2020/data) |
| 30&nbsp;Mar&nbsp;2020 | Alternative scenario development data ready                         | [🏃‍ Alt dev data](https://github.com/knowledge-learning/ehealthkd-2020/data/development/transfer)  |
| 30&nbsp;Mar&nbsp;2020 | Ensemble dataset for augmenting training stage, ready                         | [🏃‍ Ensemble](https://github.com/knowledge-learning/ehealthkd-2020/tree/master/data/ensemble)  |
| 20&nbsp;Apr&nbsp;2020<br>~~06&nbsp;Apr&nbsp;2020~~ | **Evaluation start** <br> Test data released                        |  |
| 03&nbsp;May&nbsp;2020<br>~~19&nbsp;Apr&nbsp;2020~~ | **Evaluation end** <br> (due by 23:59 UTC)                          |  |
| 03&nbsp;May&nbsp;2020<br>~~19&nbsp;Apr&nbsp;2020~~ | **Registration deadline** <br> (due by 23:59 UTC)                   |  |
| 08&nbsp;May&nbsp;2020<br>~~24&nbsp;Abr&nbsp;2020~~ | Results posted                                                      |  |
| 22&nbsp;May&nbsp;2020<br>~~08&nbsp;May&nbsp;2020~~ | System description paper submissions <br> (due by 23:59 UTC)        |  |
| 05&nbsp;Jun&nbsp;2020<br>~~22&nbsp;May&nbsp;2020~~ | Paper reviews                                                       |  |
| 12&nbsp;Jun&nbsp;2020<br>~~29&nbsp;May&nbsp;2020~~ | Author notifications                                                |  |
| 26&nbsp;Jun&nbsp;2020<br>~~12&nbsp;Jun&nbsp;2020~~ | Camera ready submissions                                            |  |
| Sep&nbsp;2020         | IberLEF Workshop                                                       |  |


## Instructions for participation

The competition is managed and run in the [Codalab Competitions platform](https://competitions.codalab.org/competitions/23454). For participation, please register on the platform and follow the instructions detailed there. The following pages provide a detailed description of the problem to be solved and the evaluation. In Codalab you will find details about how to submit a solution, as well as all relevant links.

<!-- [Click here to enter the competition](https://competitions.codalab.org/competitions/21781). -->

To download the relevant data, [please visit here](https://forms.gle/3KHAvo7e5MfxtnME9).

## Publication instructions

The following instructions are subject to change to adapt to the official IberLEF 2020 requirements.

Send your paper to our Program Comitee at [chairs_eHealth-KD@googlegroups.com](mailto:chairs_eHealth-KD@googlegroups.com) before **(May 22th, 2020)**.

The Organization Committee of eHealth-KD encourages participants to submit a description paper of their systems. Submitted papers will be reviewed by a scientific committee, and only accepted papers will be published at CEUR. The proceedings of eHealth-KD will be jointly published with the proceedings of all tasks of IberLEF 2020. The submitted papers will be peer-reviewed by a Program Commitee which is composed by all the participants and the Organization Commitee.

The manuscripts must satisfy the following rules:

The minimum length of the regular paper should be 5 (mandatory minimum) and up to 10 pages plus references formatted according to the [Conference Proceedings Springer template](https://www.springer.com/gp/computer-science/lncs/conference-proceedings-guidelines). The style that appears in the template by default must be used.

* Articles can be written in English. The title, abstract and keywords must be written in English.
* The document format must be Word or Latex, but the submission must be in PDF format.
* Instead of describing the task and/or the corpus, you should focus on the description of your experiments and the analysis of your results, and include a citation to the Overview paper. Indications for this citation will be provided in due time.
* Depending on the final number of participants and the time allocated for the workshop, all or a selected group of papers will be presented and discussed in the Workshop session.

## Organization committee

| Name                     | Email                                                 | Institution                   |
|--------------------------|-------------------------------------------------------|-------------------------------|
| Yoan Gutiérrez Vázquez (contact person)   | [ygutierrez@dlsi.ua.es](mailto:ygutierrez@dlsi.ua.es) | University of Alicante, Spain |
| Suilan Estévez Velarde   | [sestevez@matcom.uh.cu](mailto:sestevez@matcom.uh.cu) | University of Havana, Cuba    |
| Alejandro Piad Morffis   | [apiad@matcom.uh.cu](mailto:apiad@matcom.uh.cu)       | University of Havana, Cuba    |
| Yudivián Almeida Cruz    | [yudy@matcom.uh.cu](mailto:yudy@matcom.uh.cu)         | University of Havana, Cuba    |
| Andrés Montoyo Guijarro  | [montoyo@dlsi.ua.es](mailto:montoyo@dlsi.ua.es)       | University of Alicante, Spain |
| Rafael Muñoz Guillena    | [rafael@dlsi.ua.es](mailto:rafael@dlsi.ua.es)         | University of Alicante, Spain |

### Discussion group

A Google Group will be set up for this "Health Shared Task" where announcements will be made.
Feel free to send your questions and feedback to [ehealth-kd@googlegroups.com](mailto:ehealth-kd@googlegroups.com).
General issues and feedback should be posted on our [Issues Page](https://github.com/knowledge-learning/ehealthkd-2020/issues) in Github.

Follow [@eHealthKD](https://twitter.com/eHealthKD) on Twitter for up-to-date news, comments and tips about the competition.

### Funding

This research has been supported by a Carolina Foundation grant in agreement with University of Alicante and University of Havana, sponsoring to Suilan Estévez Velarde. Moreover, it has also been partially funded by both aforementioned universities, Generalitat Valenciana, Spanish Government, Ministerio de Educación, Cultura y Deporte through the project PROMETEU/2018/089.
