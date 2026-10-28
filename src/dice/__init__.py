from dice.cli import main
from dice.config import ExperimentConfig
from dice.plotting import overlay_gaussian, run_experiments
from dice.simulation import experiment, roll, theoretical_stats

__all__ = [
    "ExperimentConfig",
    "experiment",
    "main",
    "overlay_gaussian",
    "roll",
    "run_experiments",
    "theoretical_stats",
]
