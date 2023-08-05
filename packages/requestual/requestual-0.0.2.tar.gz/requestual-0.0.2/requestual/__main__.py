import sys
from pathlib import Path

from textual.app import App
from textual.widgets import Footer, Placeholder


class Requestual(App):
    async def on_load(self) -> None:
        """Called before going in to application mode"""
        try:
            self.path = sys.argv[1]
        except IndexError:
            self.path = str(Path().absolute())

        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        """Called after going in to application mode"""
        print(self.path)
        self.sidebar = Placeholder()
        self.body = Placeholder()
        self.footer = Footer()

        await self.view.dock(self.footer, edge="bottom")
        await self.view.dock(self.sidebar, edge="left", size=48)
        await self.view.dock(self.body, edge="top")


def main():
    Requestual.run(log="requestual.log")


if __name__ == "__main__":
    main()
