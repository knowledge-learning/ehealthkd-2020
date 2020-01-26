---
title: Tasks
permalink: /tasks
nav_order: 2
---

## Subtask A: Entity recognition

Given a list of eHealth documents written in Spanish, the goal of this subtask is to identify all the entities per document and their classes. These entities are all the relevant terms (single word or multiple words) that represent semantically important elements in a sentence. The following figure shows the relevant entities that appear in the example sentences shown in the previous section.

![](img/task_a.png)

Note that some entities ("*vías respiratorias*" and "*60 años*") span more than one word. Entities will always consist of one or more complete words (i.e., not a prefix or a suffix of a word), and will never include any surrounding punctuation symbols, parenthesis, etc.
There are four categories or classes for entities:

* **Concept:** indentifies a relevant term, concept, idea, in the knowledge domain of the sentence.
* **Action:** indentifies a process or modification of other entities. It can be indicated by a verb or verbal construction, such as "*afecta*" (*affects*), but also by nouns, such as "*exposición*" (*exposition*), where it denotes the act of being exposed to the Sun, and "*daños*" (*damages*), where it denotes the act of damaging the skin. It can also be used to indicate non-verbal functional relations, such as "*padre*" (*parent*), etc.
* **Predicate:** identifies a function or filter of another set of elements, which has a semantic label in the text, such as "*mayores*" (*older*), and is applied to an entity, such as "*personas*" (*people*) with some additional arguments such as "*60 años*" (*60 years*).
* **Reference:** identifies a textual element that refers to an entity --of the same sentence or of different one--, which can be indicated by textual clues such as "*esta*", "*aquel*", etc.

Subtask A input is a text document with a sentence per line. Sentences have not been preprocesed. The output consists of a plain text file, in [BRAT standoff format](https://brat.nlplab.org/standoff.html), where each line represents an entity. Each line has the following format:

```
ID \tab START END ; START END \tab LABEL \tab TEXT
```

The **ID** is a numerical identifier that will be used in Subtask B to link entities with their relations. The **START** and **END** indicate the starting and ending character of the text span. Multi-word phrases such as vías respiratorias where all the words are continuous can either be indicated by a single **START / END** pair or by several **START / END** (one for each word) separated by semicolons (;). Multi-word phrases where the words are not continuous must use semicolons to separate the different portions of the phrase. In the training documents we will always represent multi-word phrases separately for consistency.
The **TEXT** portion simply reproduces the full text of the key phrase. This portion will be ignored in the evaluation, so participants are free not to produce it, but it will be provided in all training documents, and we recommend participants to also produce it, since it simplifies manual inspection during development.
**LABEL** is one of the previous four categories defined. In this example, a possible output file is the following:

<script class="sample" src="https://gist-it.appspot.com/github/knowledge-learning/ehealthkd-v2/blob/master/docs/sample_output_a.txt?footer=minimal"></script>

> **NOTE**: Column headers are optional, and only shown here for illustrative purposes.

> **Recap:** Columns are separated by _one or more_ **TAB** characters. The two numbers inside each **START/END** pair are separated by _one_ **SPACE** character. The different **START/END** pairs for each multi-word are separated by _one_ **SEMICOLON** ( **;** ) character.

## Subtask B: Detection of semantic relations

Subtask B continues from the output of Subtask B, by linking the entities detected and labelled in each document. The purpose of this subtask is to recognize all relevant semantic relationships between the entities recognized. Eight of the thirteen semantic relations defined for this challenge can be identified in the following example:

![](img/task_b.png)

The semantic relations are divided in different categories:

**General relations (6):** general-purpose relations between two concepts (it involves Concept, Action, Predicate, and Reference) that have a specific semantic. When any of these relations applies, it is preferred over a domain relation --tagging a key phrase as a link between two information units--, since their
semantic is independent of any textual label:

* **is-a:** indicates that one concept is a subtype, instance, or member of the class identified by the other.
* **same-as:** indicates that two concepts are semantically the same.
* **has-property:** indicates that one concept has a given property or characteristic.
* **part-of:** indicates that a concept is a constituent part of another.
* **causes:** indicates that one concept provoques the existence or occurrence of another.
* **entails:** indicates that the existence of one concept implies the existence or occurrence of another.

**Contextual relations (3):** allow to refine a concept (it involves **Concept**, **Action**, **Predicate**, and **Reference**) by attaching modifiers. These are:

* **in-time:** to indicate that something exists, occurs or is confined to a time-frame, such as in "*exposición*" in-time "*verano*".
* **in-place:** to indicate that something exists, occurs or is confined to a place or location.
* **in-context:** to indicate a general context in which something happens, like a mode, manner, or state, such as "*exposición*" in-context "*prolongada*".

**Action roles (2):** indicate which role plays the concepts related to an **Action**:

* **subject:** indicates who performs the action, such as in "*[el] asma afecta [...]*".
* **target:** indicates who receives the effect of the action, such as in "*[...] afecta [las] vías respiratorias*".
Actions can have several subjects and targets, in which case the semantic interpreted is that the union of the subjects performs the action over each of the targets.

**Predicate roles (2):** indicate which role plays the concepts related to a **Predicate**:

* **domain:** indicates the main concept on which the predicate applies.
* **arg:** indicates an additional concept that specifies a value for the predicate to make sense. The exact semantic of this argument depends on the semantic of the predicate label, such as in "*mayores [de] 60 años*", where the predicate label "*mayores*" indicates that "*60 años*" is a quantity, that restricts the minimum age for the predicate to be true.

The output for Subtask B is a plain text file where each line corresponds to a semantic relation between two entities, in the format:

```
LABEL \tab SOURCE-ID \tab DEST-ID
```

The **LABEL** (i.e. column 1) is one of the previously defined, and the **ID**s correspond to the participants in the relation. Note that every relation is directed, hence the **SOURCE-ID** (i.e. column 2) and the **DEST-ID** (i.e column 3) must match the right direction, except for **same-as** which is symmetric, so both directions are equivalent. For the previous example the output is:

<script class="sample" src="https://gist-it.appspot.com/github/knowledge-learning/ehealthkd-v2/blob/master/docs/sample_output_b.txt?footer=minimal"></script>

> **NOTE**: Column headers are optional, and only shown here for illustrative purposes.

> **Recap:** Columns are separated by _one or more_ **TAB** characters.

### Important: Note about negated concepts

The eHealth-KD corpus considers negated actions, which are manually annotated in the corresponding Brat files (which will be released after the challenge is completed). However, for competition purposes, we are **not considering** the annotation of negation as part of the challenge.

This means that, in the corpus, you will find sentences with negated concepts, such as: _"No existe un tratamiento que restablezca la función ovárica normal."_. In this and similar sentences, we **still expect** that your system recognizes _existe_ as **Action** and _tratamiento_ as **Target**, as though if the negation did not exist.

In in doubt please contact the organizers at [ehealth-kd@googlegroups.com](mailto:ehealth-kd@googlegroups.com).
