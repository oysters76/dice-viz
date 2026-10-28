import argparse
import json
import re
from collections import Counter

import numpy as np

from dice.config import ExperimentConfig
from dice.plotting import run_experiments
from dice.simulation import experiment, theoretical_stats


def parse_spec(spec: str, default_rolls: int) -> ExperimentConfig:
    m = re.fullmatch(r"(\d+)d(\d+)(?:x(\d+))?", spec)
    if not m:
        raise argparse.ArgumentTypeError(
            f"invalid spec '{spec}' — use NdF or NdFxR (e.g. 2d6, 3d8x5000)"
        )
    num_dice = int(m.group(1))
    faces = int(m.group(2))
    rolls = int(m.group(3)) if m.group(3) else default_rolls
    return ExperimentConfig(num_dice=num_dice, faces=faces, num_rolls=rolls)


def handle_simulate(args) -> int:
    if args.seed is not None:
        np.random.seed(args.seed)

    values = experiment(n=args.faces, dices=args.num_dice, rolls=args.rolls)
    counts = Counter(int(v) for v in values)
    mu_theo, sigma_theo = theoretical_stats(args.num_dice, args.faces)

    result = {
        "config": {
            "num_dice": args.num_dice,
            "faces": args.faces,
            "rolls": args.rolls,
            "seed": args.seed,
        },
        "results": {
            "mean": round(float(np.mean(values)), 4),
            "std": round(float(np.std(values)), 4),
            "min": int(np.min(values)),
            "max": int(np.max(values)),
            "median": float(np.median(values)),
            "theoretical_mean": round(mu_theo, 4),
            "theoretical_std": round(sigma_theo, 4),
            "histogram": dict(sorted(counts.items())),
        },
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        cfg = result["config"]
        res = result["results"]
        print(f"Dice: {cfg['num_dice']}d{cfg['faces']}  Rolls: {cfg['rolls']}  Seed: {cfg['seed']}")
        print(
            f"Mean: {res['mean']}  Std: {res['std']}  "
            f"Min: {res['min']}  Max: {res['max']}  Median: {res['median']}"
        )
        print(f"Theoretical — Mean: {res['theoretical_mean']}  Std: {res['theoretical_std']}")

    return 0


def handle_plot(args) -> int:
    if args.seed is not None:
        np.random.seed(args.seed)

    specs = args.specs if args.specs else ["1d6"]
    experiments = [parse_spec(s, args.rolls) for s in specs]
    run_experiments(experiments, save_path=args.save)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dice", description="Dice simulation toolkit")
    sub = parser.add_subparsers(dest="command")

    sim = sub.add_parser("simulate", help="Run a simulation and output stats")
    sim.add_argument("-d", "--num-dice", type=int, default=1)
    sim.add_argument("-f", "--faces", type=int, default=6)
    sim.add_argument("-r", "--rolls", type=int, default=10000)
    sim.add_argument("-s", "--seed", type=int, default=None)
    sim.add_argument("--format", choices=["json", "text"], default="json")

    plot = sub.add_parser("plot", help="Generate histogram plots")
    plot.add_argument(
        "specs", nargs="*", help="Experiment specs in NdF or NdFxR notation (e.g. 2d6 3d8x5000)"
    )
    plot.add_argument("-r", "--rolls", type=int, default=10000)
    plot.add_argument("-s", "--seed", type=int, default=None)
    plot.add_argument(
        "-o", "--save", type=str, default=None, help="Save figure to file instead of showing"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "simulate":
        return handle_simulate(args)
    elif args.command == "plot":
        return handle_plot(args)

    return 0
