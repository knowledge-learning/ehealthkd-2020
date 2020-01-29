import argparse
import warnings
from pathlib import Path
from typing import List
from shutil import make_archive

from scripts.utils import Collection


class Algorithm:
    def run(
        self, collection: Collection, *args, taskA: bool, taskB: bool, **kargs
    ) -> Collection:
        raise NotImplementedError()


class Run:
    def __init__(
        self,
        user: str,
        run_name: str,
        algorithm: Algorithm,
        *,
        gold: Path,
        mode: str,
        scenarios: List[str]
    ):
        self.user = user
        self.run_name = run_name
        self.algorithm = algorithm

        self.gold = gold
        self.mode = mode
        self.scenarios = scenarios

    def __call__(self, *args, **kargs):
        for scenario in self.scenarios:
            collection = self._load_collection(scenario)
            output = self.algorithm.run(
                collection,
                taskA=(not scenario.endswith("-taskB")),
                taskB=(not scenario.endswith("-taskA")),
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
        gold = self.gold.format(scenario)

        return Collection().load(
            Path(gold),
            legacy=False,
            keyphrases=scenario.endswith("-taskB"),
            relations=False,
            attributes=False,
        )

    @staticmethod
    def on(user: str, *algorithms, config):
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
            run = Run(user, run_name, algorithm, **config)
            runs.append(run)
        return runs

    @staticmethod
    def exec(runs: "List[Run]", *args, **kargs):
        for run in runs:
            run(*args, **kargs)

    @staticmethod
    def zip(user: str):
        make_archive(
            "data/submissions/{0}".format(user),
            "zip",
            "data/submissions/{0}".format(user),
        )

    @staticmethod
    def submit(usr: str, configurations, *algorithms):
        for config in configurations:
            Run.exec(Run.on(usr, *algorithms, config=config))
        Run.zip('baseline')

    @staticmethod
    def testing():
        yield dict(
            gold="data/testing/{0}/scenario.txt",
            mode="test",
            scenarios=[
                "scenario1-main",
                "scenario2-taskA",
                "scenario3-taskB",
                "scenario4-transfer",
            ],
        )

    @staticmethod
    def development():
        yield dict(
            gold="data/development/main/scenario.txt",
            mode="dev",
            scenarios=["scenario1-main", "scenario2-taskA", "scenario3-taskB"],
        )
        yield dict(
            gold="data/development/transfer/scenario.txt",
            mode="dev",
            scenarios=["scenario4-transfer"],
        )

    @staticmethod
    def training():
        yield dict(
            gold="data/training/scenario.txt",
            mode="train",
            scenarios=["scenario1-main", "scenario2-taskA", "scenario3-taskB"],
        )


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--dev", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument(
        "--custom",
        action="append",
        nargs=3,
        metavar=("GOLD", "MODE", "SCENARIOS"),
        help="""
        GOLD: path to gold file (use `{0}` for scenario template).
        MODE: name of the directory inside the user submit folder.
        SCENARIOS: name (or ',' separated list of names) for the run scenario(s).
        """,
    )
    args = parser.parse_args()

    tasks = []

    if args.train:
        tasks.extend(Run.training())

    if args.dev:
        tasks.extend(Run.development())

    if args.test:
        tasks.extend(Run.testing())

    if args.custom is not None:
        tasks.extend(
            dict(gold=gold, mode=mode, scenarios=scenarios.split(","))
            for gold, mode, scenarios in args.custom
        )

    return tasks
