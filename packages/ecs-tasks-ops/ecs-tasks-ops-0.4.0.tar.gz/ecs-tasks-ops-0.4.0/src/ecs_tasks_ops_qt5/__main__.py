"""Qt5 UI Initialization."""
import click

from ecs_tasks_ops import ecs_conf
from ecs_tasks_ops_qt5 import qt5_gui


@click.version_option()
def main() -> None:
    """Open Qt5 User Interface."""
    ecs_conf.load_config()
    qt5_gui.main_gui()


if __name__ == "__main__":
    pass
