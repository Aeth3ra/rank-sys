from dataclasses import dataclass

@dataclass
class Config:
    mu: float = 25.0
    sigma: float = 25.0 / 3