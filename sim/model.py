"""Core simulation logic for evolution simulator.

This module is intentionally independent from any UI code to make it
possible to swap out the simulation engine or front‑end with minimal
changes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Simulation:
    """Simulation of organisms on a toroidal grid.

    Each cell may contain a species identified by an integer.  ``None``
    means the cell is empty.  The update rules are a simple
    generalisation of Conway's Game of Life where organisms only interact
    with members of the same species:

    * An organism survives if it has two or three neighbours of the same
      species.
    * An empty cell spawns a new organism of species ``s`` if it has
      exactly three neighbours of species ``s``.
    """

    width: int
    height: int
    grid: List[List[Optional[int]]] = field(init=False)
    generation: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    # ------------------------------------------------------------------
    # Grid helpers
    def in_bounds(self, x: int, y: int) -> tuple[int, int]:
        """Return coordinates wrapped around the torus."""
        return x % self.width, y % self.height

    def get(self, x: int, y: int) -> Optional[int]:
        x, y = self.in_bounds(x, y)
        return self.grid[y][x]

    def set(self, x: int, y: int, species: Optional[int]) -> None:
        x, y = self.in_bounds(x, y)
        self.grid[y][x] = species

    def move(self, sx: int, sy: int, tx: int, ty: int) -> None:
        """Move species from source to target cell."""
        species = self.get(sx, sy)
        self.set(sx, sy, None)
        self.set(tx, ty, species)

    # ------------------------------------------------------------------
    def neighbour_counts(self, x: int, y: int) -> dict[int, int]:
        """Return a mapping of species->count of neighbours."""
        counts: dict[int, int] = {}
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                species = self.get(x + dx, y + dy)
                if species is not None:
                    counts[species] = counts.get(species, 0) + 1
        return counts

    def step(self) -> None:
        """Advance the simulation by one generation."""
        new_grid: List[List[Optional[int]]] = [[None for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                species = self.grid[y][x]
                counts = self.neighbour_counts(x, y)
                if species is not None:
                    if counts.get(species, 0) in (2, 3):
                        new_grid[y][x] = species
                else:
                    for s, c in counts.items():
                        if c == 3:
                            new_grid[y][x] = s
                            break
        self.grid = new_grid
        self.generation += 1

    def clear(self) -> None:
        """Remove all organisms."""
        for row in self.grid:
            for x in range(len(row)):
                row[x] = None
        self.generation = 0
