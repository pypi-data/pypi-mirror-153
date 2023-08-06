from rich.console import Console
from rich.logging import RichHandler
from rich import box
from rich.panel import Panel
from rich.theme import Theme
import logging
import sys
from pathlib import Path


THEMEFILE = str(Path(__file__).parent.resolve() / "theme.ini")
CONSOLE = Console(theme=Theme().read(THEMEFILE))

# logger - Rich
logging.basicConfig(
    # filename='',
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(console=CONSOLE, rich_tracebacks=True, omit_repeated_times=False)
    ],
)
logging = logging.getLogger("rich")


def banner(banner_title):
    """
    Rich util Banner.
    """

    print("\n")
    CONSOLE.print(
        Panel("", title=f"[h1]{banner_title}", height=1, width=95, box=box.DOUBLE_EDGE)
    )


# Non Rich util.
def ctrl_c(txt="[ENTER] to continue / [CTRL-C] to quit..."):
    """
    Press ENTER / CTRL-C
    """

    try:
        input(f"\n{txt}")
    except KeyboardInterrupt:
        print(f"\nQuit: detected [CTRL-C] ")
        sys.exit(0)
