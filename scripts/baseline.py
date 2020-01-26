# coding: utf8

import argparse
import re
import sys
import warnings
from pathlib import Path
from typing import List

from .utils import Collection, Keyphrase, Relation, Sentence


class Algorithm:
    def run(
        self, collection: Collection, *args, taskA: bool, taskB: bool, **kargs
    ) -> Collection:
        raise NotImplementedError()


class Baseline(Algorithm):
    def __init__(self):
        self.model = None

    def train(self, finput: Path):
        collection = Collection().load(finput)

        self.model = keyphrases, relations = {}, {}

        for sentence in collection.sentences:
            for keyphrase in sentence.keyphrases:
                text = keyphrase.text.lower()
                keyphrases[text] = keyphrase.label

        for sentence in collection.sentences:
            for relation in sentence.relations:
                origin = relation.from_phrase
                origin_text = origin.text.lower()
                destination = relation.to_phrase
                destination_text = destination.text.lower()

                relations[
                    origin_text, origin.label, destination_text, destination.label
                ] = relation.label

    def run(self, collection, *args, taskA, taskB, **kargs):
        gold_keyphrases, gold_relations = self.model

        if taskA:
            next_id = 0
            for gold_keyphrase, label in gold_keyphrases.items():
                for sentence in collection.sentences:
                    text = sentence.text.lower()
                    pattern = r"\b" + gold_keyphrase + r"\b"
                    for match in re.finditer(pattern, text):
                        keyphrase = Keyphrase(sentence, label, next_id, [match.span()])
                        keyphrase.split()
                        next_id += 1

                        sentence.keyphrases.append(keyphrase)

        if taskB:
            for sentence in collection.sentences:
                for origin in sentence.keyphrases:
                    origin_text = origin.text.lower()
                    for destination in sentence.keyphrases:
                        destination_text = destination.text.lower()
                        try:
                            label = gold_relations[
                                origin_text,
                                origin.label,
                                destination_text,
                                destination.label,
                            ]
                        except KeyError:
                            continue
                        relation = Relation(sentence, origin.id, destination.id, label)
                        sentence.relations.append(relation)

                sentence.remove_dup_relations()

        return collection


class Run:
    SCENARIOS = ["scenario1-main", "scenario2-taskA", "scenario3-taskB"]

    def __init__(self, user: str, run_name: str, algorithm: Algorithm, *, testing=True):
        self.user = user
        self.run_name = run_name
        self.algorithm = algorithm

        self.testing = testing
        self.mode = "test" if testing else "dev"
        self.scenarios = self.SCENARIOS if testing else ["scenario"]

    def __call__(self, *args, **kargs):
        for scenario in self.scenarios:
            collection = self._load_collection(scenario)
            output = self.algorithm.run(
                collection,
                taskA=(scenario != self.SCENARIOS[2]),
                taskB=(scenario != self.SCENARIOS[1]),
                *args,
                **kargs
            )
            output.dump(
                Path(
                    "data/submissions/{0}/{1}/{2}/{3}/scenario.txt".format(
                        self.user, self.mode, self.run_name, scenario
                    )
                )
            )

    def _load_collection(self, scenario):
        if self.testing:
            gold = "data/testing/{0}/scenario.txt".format(scenario)
        else:
            gold = "data/development/scenario.txt"

        return Collection().load(
            Path(gold),
            legacy=False,
            keyphrases=(scenario == self.SCENARIOS[2]),
            relations=False,
            attributes=False,
        )

    @staticmethod
    def on(user: str, *algorithms, testing=True):
        if len(algorithms) > 3:
            warnings.warn(
                "Too many runs. Expected (3) and ({0}) were given.".format(
                    len(algorithms)
                )
            )
        elif len(algorithms) < 3:
            warnings.warn(
                "Too few runs. Expected (3) and ({0}) were given.".format(
                    len(algorithms)
                )
            )
        runs = []
        for i, algorithm in enumerate(algorithms, 1):
            run_name = "run{0}".format(i)
            run = Run(user, run_name, algorithm, testing=testing)
            runs.append(run)
        return runs

    @staticmethod
    def exec(runs: "List[Run]", *args, **kargs):
        for run in runs:
            run(*args, **kargs)


def main(testing):
    baseline = Baseline()
    baseline.train(Path("data/testing/scenario1-main/scenario.txt"))
    Run.exec(Run.on("Baseline", baseline, testing=testing))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testing", action="store_true")
    args = parser.parse_args()
    main(args.testing)
