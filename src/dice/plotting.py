import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm

from dice.config import ExperimentConfig
from dice.simulation import experiment, theoretical_stats


def overlay_gaussian(ax: plt.Axes, num_dice: int, faces: int) -> None:
    mu, sigma = theoretical_stats(num_dice, faces)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 200)
    ax.plot(x, norm.pdf(x, mu, sigma), "r--", linewidth=2, label="Gaussian")
    ax.legend()


def run_experiments(experiments: list[ExperimentConfig], save_path: str | None = None) -> None:
    cols = min(len(experiments), 3)
    rows = (len(experiments) + cols - 1) // cols
    _fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = np.array(axes).flat

    for ax, exp in zip(axes, experiments, strict=False):
        values = experiment(n=exp.faces, dices=exp.num_dice, rolls=exp.num_rolls)
        sns.histplot(values, kde=True, discrete=True, stat="density", ax=ax, color="steelblue")
        overlay_gaussian(ax, exp.num_dice, exp.faces)
        ax.set_title(f"{exp.num_dice}d{exp.faces} x {exp.num_rolls}")
        ax.set_xlabel("Sum")
        ax.set_ylabel("Density")

    for ax in list(axes)[len(experiments) :]:
        ax.set_visible(False)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
