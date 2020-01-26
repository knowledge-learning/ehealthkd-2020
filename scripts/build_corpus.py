# coding: utf8

import random
import sys
from pathlib import Path

from scripts.utils import Collection, Sentence


def get_clean_collection(anns_path: Path, select: str):
    collection = Collection()

    for file in sorted((anns_path / select).iterdir()):
        if file.name.endswith(".txt"):
            collection.load(file)

    for s in collection.sentences:
        overlaps = s.overlapping_keyphrases()

        if overlaps:
            print("Found overlapping:", overlaps)
            s.merge_overlapping_keyphrases()
            overlaps = s.overlapping_keyphrases()

        dups = s.dup_relations()

        if dups:
            print(
                "Found duplicated relations %r in sentence '%s'"
                % ([v[0] for v in dups.values()], s.text)
            )
            s.remove_dup_relations()
            dups = s.dup_relations()

        assert not overlaps
        assert not dups

    return collection


def get_training_and_development(anns_path: Path):
    sentences = get_clean_collection(anns_path, "traindev").sentences
    random.shuffle(sentences)
    return sentences


def get_test(anns_path: Path):
    sentences = get_clean_collection(anns_path, "test").sentences
    random.shuffle(sentences)
    return sentences


def get_extra(anns_path: Path, *collections):
    extra_sentences = []
    all_sentences = {s.text for collection in collections for s in collection}

    for file in sorted((anns_path / "plain").iterdir()):
        if file.name.endswith(".txt"):
            with file.open() as fp:
                file_sentences = [s.strip() for s in fp.read().split("\n") if s.strip()]

                for s in file_sentences:
                    if s not in all_sentences:
                        extra_sentences.append(s)

    random.shuffle(extra_sentences)
    extra_sentences = [Sentence(s) for s in extra_sentences[:8700]]
    return extra_sentences


def main(anns_path: Path, training_path, develop_path, test_path):
    random.seed(42)

    # dump training and development collections ----------------------------------
    train_develop_sentences = get_training_and_development(anns_path)

    #### training
    training = Collection(train_develop_sentences[:800])
    training.dump(training_path / "scenario.txt")

    #### development
    develop = Collection(train_develop_sentences[800:])
    develop.dump(develop_path / "scenario.txt")

    # dump test collection (per scenario) ----------------------------------------
    test_sentences = get_test(anns_path)
    extra_sentences = get_extra(anns_path, train_develop_sentences, test_sentences)

    #### test/scenario3
    scn3 = Collection(test_sentences[200:])
    scn3.dump(test_path / "scenario3-taskB" / "scenario.txt")

    #### test/scenario2
    scn2 = Collection(test_sentences[100:200])
    scn2.dump(test_path / "scenario2-taskA" / "scenario.txt")

    #### test/scenario1
    scn1 = Collection(
        extra_sentences[:4567] + test_sentences[:100] + extra_sentences[4567:]
    )
    scn1.dump(test_path / "scenario1-main" / "scenario.txt", False)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
