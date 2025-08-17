"""Tkinter front‑end for the evolution simulator."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from .model import Simulation


class App:
    def __init__(self, width: int = 50, height: int = 30, cell_size: int = 20) -> None:
        self.sim = Simulation(width, height)
        self.cell_size = cell_size
        self.running = False
        self.selected: Optional[tuple[int, int]] = None

        self.root = tk.Tk()
        self.root.title("Evolution Simulator")

        # Canvas for drawing the grid
        self.canvas = tk.Canvas(
            self.root,
            width=width * cell_size,
            height=height * cell_size,
            bg="white",
        )
        self.canvas.pack(side=tk.TOP)
        self.canvas.bind("<Button-1>", self.on_click)

        # Controls
        ctrl = tk.Frame(self.root)
        ctrl.pack(side=tk.TOP, fill=tk.X)

        self.start_btn = tk.Button(ctrl, text="Start", command=self.toggle)
        self.start_btn.pack(side=tk.LEFT)

        tk.Button(ctrl, text="Step", command=self.step).pack(side=tk.LEFT)
        tk.Button(ctrl, text="Clear", command=self.clear).pack(side=tk.LEFT)

        tk.Label(ctrl, text="Delay ms:").pack(side=tk.LEFT)
        self.delay = tk.Scale(ctrl, from_=50, to=1000, orient=tk.HORIZONTAL)
        self.delay.set(200)
        self.delay.pack(side=tk.LEFT)

        self.gen_var = tk.StringVar()
        self.gen_var.set("Generation: 0")
        tk.Label(ctrl, textvariable=self.gen_var).pack(side=tk.LEFT, padx=10)

        self.draw()

    # ------------------------------------------------------------------
    def draw(self) -> None:
        self.canvas.delete("all")
        for y, row in enumerate(self.sim.grid):
            for x, species in enumerate(row):
                if species is not None:
                    x1 = x * self.cell_size
                    y1 = y * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    color = "green"  # single species
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        if self.selected is not None:
            x, y = self.selected
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

    def update_loop(self) -> None:
        if self.running:
            self.sim.step()
            self.gen_var.set(f"Generation: {self.sim.generation}")
            self.draw()
        self.root.after(self.delay.get(), self.update_loop)

    def toggle(self) -> None:
        self.running = not self.running
        self.start_btn.config(text="Stop" if self.running else "Start")

    def step(self) -> None:
        self.sim.step()
        self.gen_var.set(f"Generation: {self.sim.generation}")
        self.draw()

    def clear(self) -> None:
        self.sim.clear()
        self.gen_var.set("Generation: 0")
        self.draw()

    # ------------------------------------------------------------------
    def on_click(self, event: tk.Event) -> None:
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if self.selected is None:
            if self.sim.get(x, y) is None:
                self.sim.set(x, y, 0)
            else:
                self.selected = (x, y)
        else:
            if self.sim.get(x, y) is None:
                sx, sy = self.selected
                self.sim.move(sx, sy, x, y)
            self.selected = None
        self.draw()

    # ------------------------------------------------------------------
    def run(self) -> None:
        self.update_loop()
        self.root.mainloop()
