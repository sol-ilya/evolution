# Evolution Simulator

A simple evolution simulator with a Tkinter front‑end and a modular
backend.  The grid wraps around like a torus and the simulation logic can
be easily swapped out.

## Usage

The application depends only on the Python standard library.  Run it with
Python 3.11 or newer:

```bash
python main.py
```

* Left click an empty cell to place a species.
* Left click an existing organism and then another empty cell to move it.
* Use **Start/Stop** to run or pause the simulation.
* **Step** advances a single generation.
* **Clear** removes all organisms.
* Adjust **Delay ms** to control the time between generations.
* The current generation number is shown next to the controls.
