# coding: utf8

import argparse
import random
from pathlib import Path
from typing import List

from scripts.utils import Collection, Sentence


def get_clean_collection(anns_path: Path, select: str) -> Collection:
    collection = Collection()

    for file in sorted((anns_path / select).iterdir()):
        if file.suffix == ".txt":
            collection.load(file, attributes=False)

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


def get_training_and_development(anns_path: Path) -> List[Sentence]:
    sentences = get_clean_collection(anns_path, "traindev").sentences
    random.seed(37)
    random.shuffle(sentences)
    return sentences


def get_test(anns_path: Path) -> List[Sentence]:
    sentences = get_clean_collection(anns_path, "test").sentences
    random.seed(137)
    random.shuffle(sentences)
    return sentences


def get_transfer(anns_path: Path) -> List[Sentence]:
    sentences = get_clean_collection(anns_path, "transfer").sentences
    random.seed(3737)
    random.shuffle(sentences)
    return sentences


def get_extra(anns_path: Path, *collections):
    extra_sentences = []
    all_sentences = {s.text for collection in collections for s in collection}

    for file in sorted((anns_path / "plain").iterdir()):
        if file.suffix == ".txt":
            with file.open() as fp:
                file_sentences = [s.strip() for s in fp.read().split("\n") if s.strip()]

                for s in file_sentences:
                    if s not in all_sentences:
                        extra_sentences.append(s)

    random.seed(1371)
    random.shuffle(extra_sentences)
    extra_sentences = [Sentence(s) for s in extra_sentences[:8700]]
    return extra_sentences


def main(anns_path: Path, training_path, develop_path, test_path):
    random.seed(42)  # default seed, but each generator should use his own

    # dump training and development collections ----------------------------------
    train_develop_sentences = get_training_and_development(anns_path)

    #### training
    training = Collection(train_develop_sentences[:800])
    training.dump(training_path / "scenario.txt")

    #### development/main
    develop = Collection(train_develop_sentences[800:])
    develop.dump(develop_path / "main" / "scenario.txt")

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

    # dump transfer learning collections ----------------------------------------
    transfer_sentences = get_transfer(anns_path)

    #### development/transfer
    develop_transfer = Collection(transfer_sentences[:100])
    develop_transfer.dump(develop_path / "transfer" / "scenario.txt")

    #### test/scenario4
    scn4 = Collection(transfer_sentences[100:])
    scn4.dump(test_path / "scenario4-transfer" / "scenario.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "corpus",
        default="./corpus",
        nargs="?",
        help="path to the ann directory ('./corpus')",
    )
    parser.add_argument(
        "training",
        default="./data/training",
        nargs="?",
        help="output training collection to this directory ('./data/training')",
    )
    parser.add_argument(
        "development",
        default="./data/development",
        nargs="?",
        help="output development collection to this directory ('./data/development')",
    )
    parser.add_argument(
        "test",
        default="./data/testing",
        nargs="?",
        help="output test collection to this directory ('./data/testing')",
    )
    args = parser.parse_args()
    main(
        Path(args.corpus), Path(args.training), Path(args.development), Path(args.test),
    )
