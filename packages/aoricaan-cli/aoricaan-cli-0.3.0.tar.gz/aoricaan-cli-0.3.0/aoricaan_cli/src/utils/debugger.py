from functools import partial

import typer
from tabulate import tabulate


class Debug:
    success = partial(typer.secho, fg=typer.colors.GREEN, bold=True)
    info = partial(typer.secho, fg=typer.colors.BLUE, bold=True)
    process = partial(typer.secho, fg=typer.colors.YELLOW, bold=True)
    error = partial(typer.secho, fg=typer.colors.YELLOW, bg=typer.colors.RED, bold=True)
    warning = partial(typer.secho, fg=typer.colors.WHITE, bg=typer.colors.YELLOW, bold=True)

    @classmethod
    def table(cls, *, values, headers):
        Debug.info(tabulate(values, headers, tablefmt="github"))
