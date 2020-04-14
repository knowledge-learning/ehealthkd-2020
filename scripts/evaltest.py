# coding: utf8
import argparse
import collections
import json
import pprint
import warnings
from pathlib import Path

from scripts.score import compute_metrics, subtaskA, subtaskB
from scripts.utils import Collection


def evaluate_scenario(submit_path: Path, gold: Collection, scenario: int):
    submit_file = submit_path / ("scenario.txt")
    if not submit_file.exists():
        warnings.warn("Input file not found in '%s'" % submit_path)
        return {}

    submit = Collection().load(submit_file)
    resultA = subtaskA(gold, submit)
    resultB = subtaskB(gold, submit, resultA)

    results = {}
    for k, v in list(resultA.items()) + list(resultB.items()):
        results[k] = len(v)

    metrics = compute_metrics(
        dict(resultA, **resultB), skipA=scenario == 3, skipB=scenario == 2
    )
    results.update(metrics)

    return results


def evaluate_one(submit_path: Path, *scenario_golds: Collection):
    names = [
        "scenario1-main",
        "scenario2-taskA",
        "scenario3-taskB",
        "scenario4-transfer",
    ]

    result = dict(submit=submit_path.name)

    # not all scenarios have to be provided
    for i, (scenario_gold, name) in enumerate(zip(scenario_golds, names), 1):
        scenario_submit = submit_path / name

        scenario = dict(
            evaluate_scenario(scenario_submit, scenario_gold, i),
            submit=submit_path.name,
        )

        result[name.split("-")[0]] = scenario

    return result


def filter_best(results):
    best = {}

    for user, submits in results.items():
        user_dict = {}
        for name in ["scenario1", "scenario2", "scenario3", "scenario4"]:
            try:
                scenario = [entry[name] for entry in submits]
                best = max(scenario, key=lambda d: d["f1"])
                user_dict[name] = best
            except KeyError:
                warnings.warn("Scenario {0} not found!".format(name))
                user_dict[name] = collections.defaultdict(float)
        best[user] = user_dict

    return best


def ensure_number_of_runs(run_folder):
    n = len([x for x in run_folder.iterdir() if x.is_dir()])
    if n > 3:
        raise Exception(
            "Too many runs at {0}. Expected (3) and ({1}) were given.".format(
                run_folder, n
            )
        )
    elif n < 3:
        warnings.warn(
            "Too few runs at {0}. Expected (3) and ({1}) were given.".format(
                run_folder, n
            )
        )


def main(
    mode="test",
    best=False,
    single=False,
    csv=False,
    pretty=False,
    final=False,
    plain=False,
    compact=False,
    gold="data",
    submit="data/submissions",
):
    users = collections.defaultdict(list)

    if csv and not best:
        raise ValueError("Error: --csv implies --best")

    if final and (not csv or not best):
        raise ValueError("Error: --final implies --csv and --best")

    if mode == "test":
        test_gold = Path(gold)
        gold_scenarios = [
            Collection().load(test_gold / "testing/scenario1-main/scenario.txt"),
            Collection().load(test_gold / "testing/scenario2-taskA/scenario.txt"),
            Collection().load(test_gold / "testing/scenario3-taskB/scenario.txt"),
            Collection().load(test_gold / "testing/scenario4-transfer/scenario.txt"),
        ]
    elif mode == "dev":
        dev_gold = Path(gold)
        gold_scenarios = [
            Collection().load(dev_gold / "development/main/scenario.txt"),
            Collection().load(dev_gold / "development/main/scenario.txt"),
            Collection().load(dev_gold / "development/main/scenario.txt"),
            Collection().load(dev_gold / "development/transfer/scenario.txt"),
        ]
    elif mode == "train":
        dev_gold = Path(gold)
        gold_scenarios = [
            Collection().load(dev_gold / "training/scenario.txt"),
            Collection().load(dev_gold / "training/scenario.txt"),
            Collection().load(dev_gold / "training/scenario.txt"),
        ]
    else:
        raise ValueError("Unexpected mode: {0}".format(mode))

    submits = Path(submit)
    if single:
        submits = submits / single
        runs = submits / mode
        if not runs.exists():
            raise ValueError(
                "Directory {0} not found. Check --mode and --single options.".format(
                    runs
                )
            )
        ensure_number_of_runs(runs)
        for subfolder in runs.iterdir():
            users[submits.name].append(evaluate_one(subfolder, *gold_scenarios))
    else:
        for userfolder in submits.iterdir():
            if not userfolder.is_dir():
                continue
            runs = userfolder / mode
            if not runs.exists():
                raise ValueError(
                    "Directory {0} not found. Did you mean to use --single? Check --mode option.".format(
                        runs
                    )
                )
            ensure_number_of_runs(runs)
            for subfolder in runs.iterdir():
                users[userfolder.name].append(evaluate_one(subfolder, *gold_scenarios))

    results = dict(users)

    if best:
        results = filter_best(results)

    if csv:
        import pandas as pd

        items = []

        for user, data in results.items():
            userdata = dict(name=user)

            for k, metrics in data.items():
                userdata.update({"%s-%s" % (k, m): v for m, v in metrics.items()})

            items.append(userdata)

        df = pd.DataFrame(items)
        df = df.set_index("name").sort_index().transpose()

        if final:
            df1 = df.transpose()[
                ["scenario1-f1", "scenario1-precision", "scenario1-recall"]
            ]
            df1 = df1.sort_values("scenario1-f1", ascending=False).to_csv()

            df2 = df.transpose()[
                ["scenario2-f1", "scenario2-precision", "scenario2-recall"]
            ]
            df2 = df2.sort_values("scenario2-f1", ascending=False).to_csv()

            df3 = df.transpose()[
                ["scenario3-f1", "scenario3-precision", "scenario3-recall"]
            ]
            df3 = df3.sort_values("scenario3-f1", ascending=False).to_csv()

            df4 = df.transpose()[
                ["scenario4-f1", "scenario4-precision", "scenario4-recall"]
            ]
            df4 = df4.sort_values("scenario4-f1", ascending=False).to_csv()

            print(df1)
            print(df2)
            print(df3)
            print(df4)

        elif pretty:
            print(df.to_html())
        else:
            print(df.to_csv())

    elif plain:
        for user, info in results.items():
            print(50 * "=")
            print(" {0} ".format(user).center(50, ":").upper())
            print(50 * "=")
            for run in info:
                print("[ {0} ]".format(run["submit"]).center(50, "-"))
                for scenario, data in run.items():
                    if scenario == "submit":
                        continue
                    print("> {0} ".format(scenario))
                    for metric, value in data.items():
                        if metric == "submit":
                            continue
                        metric = "{0}".format(metric).ljust(15)
                        if isinstance(value, float):
                            print("     {0} ~ {1:0.4}".format(metric, value))
                        else:
                            print("     {0} = {1}".format(metric, value))

    elif compact:
        if not single:
            raise ValueError("--compact requires --single")
        if not best:
            raise ValueError("--compact requires --best")

        results = results[single]

        for scn, metrics in results.items():
            for m in ["f1", "precision", "recall"]:
                print(f"{scn}-{m}: {metrics[m]:0.5}")
    else:
        print(json.dumps(results, sort_keys=True, indent=2 if pretty else None))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("evaltest")
    parser.add_argument(
        "--mode",
        choices=["test", "dev", "train"],
        default="test",
        required=True,
        help="set the evaluation mode",
    )
    parser.add_argument(
        "--single",
        metavar="SUBMITS",
        help="if passed, then SUBMITS points to a single participant's name with submission folders inside, otherwise SUBMITS points to a folder (./data/submissions/) with many participants, each with submission folders inside.",
    )
    parser.add_argument(
        "--best",
        action="store_true",
        help="report only the best submission per scenario, otherwise all submissions are reported.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="if passed then results are formatted as a table, can only be used with --best. Otherwise, results are returned in JSON format.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="if passed results are pretty printed: indented in JSON or in HTML when using --csv.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="if passed results are printed in compacted form suitable for Codalab.",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="if passed results are pretty printed in a plain manner.",
    )
    parser.add_argument(
        "--final",
        action="store_true",
        help="if passed, results are formatted for final publication. Can only be passed with --csv and --best.",
    )
    parser.add_argument(
        "--gold",
        help="if passed, overrides the path of the gold collection.",
        default="data",
    )
    parser.add_argument(
        "--submit",
        help="if passed, overrides the path of the submit folder.",
        default="data/submissions",
    )
    args = parser.parse_args()
    main(
        args.mode,
        args.best,
        args.single,
        args.csv,
        args.pretty,
        args.final,
        args.plain,
        args.compact,
        args.gold,
        args.submit,
    )
