import argparse
import warnings
from pathlib import Path

from scripts.utils import Collection


class Algorithm:
    def run(
        self, collection: Collection, *args, taskA: bool, taskB: bool, **kargs
    ) -> Collection:
        raise NotImplementedError()


class Run:
    SCENARIOS = [
        "scenario1-main",
        "scenario2-taskA",
        "scenario3-taskB",
        "scenario4-transfer",
    ]

    def __init__(self, user: str, run_name: str, algorithm: Algorithm, *, testing=True):
        self.user = user
        self.run_name = run_name
        self.algorithm = algorithm

        if hasattr(testing, "__iter__"):
            self.gold, self.mode, self.scenarios = testing
        elif testing:
            self.gold = "data/testing/{0}/scenario.txt"
            self.mode = "test"
            self.scenarios = self.SCENARIOS
        else:
            self.gold = "data/development/{0}/scenario.txt"
            self.mode = "dev"
            self.scenarios = ["main", "transfer"]

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
        gold = self.gold.format(scenario)

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


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_const", const=False, default=None)
    parser.add_argument("--test", action="store_const", const=True, default=None)
    parser.add_argument(
        "--custom",
        action="append",
        nargs=3,
        metavar=("GOLD", "MODE", "SCENARIOS"),
        help="""
        GOLD: path to gold file (use `{0}` for scenario template).
        MODE: name of the directory inside the user submit folder.
        SCENARIOS: name (or ',' separated list of names) for the run escenario(s).
        """,
    )
    args = parser.parse_args()

    sources = []

    if args.dev is not None:
        sources.append(args.dev)

    if args.test is not None:
        sources.append(args.test)

    if args.custom is not None:
        for gold, mode, scenarios in args.custom:
            sources.append((gold, mode, scenarios.split(",")))

    return sources
