"""Entry point for the evolution simulator."""

from sim.gui import App


def main() -> None:
    app = App()
    app.run()


if __name__ == "__main__":
    main()
