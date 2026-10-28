from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ExperimentConfig:
    num_rolls: int = 10000
    num_dice: int = 1
    faces: int = 6
