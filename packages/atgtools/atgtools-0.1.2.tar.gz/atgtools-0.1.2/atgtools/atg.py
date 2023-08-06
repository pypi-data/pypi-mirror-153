import time
from functools import wraps
from . import __version__
import atgtools.richard as r
import click
import sys
import os

# import sys
from pathlib import Path

ROOT_COMMAND_HELP = """\b
ATGtools command-line interface
-------------------------------
"""


@click.group(
    invoke_without_command=False,
    no_args_is_help=True,
    help=ROOT_COMMAND_HELP,
)
@click.pass_context
def main(ctx):
    pass


def _echo_version():
    pyver = sys.version_info
    click.echo(f"Python version: {pyver.major}.{pyver.minor}.{pyver.micro}")
    click.secho(f"atgcli version: {__version__}")


def timeit(method):
    """
    Calculate the time it takes to run a method
    """

    @wraps(method)
    def wrapper(*args, **kargs):
        starttime = time.time()
        result = method(*args, **kargs)
        endtime = time.time()
        print(end="\n")
        r.CONSOLE.print(f"Completed in: {(endtime - starttime)} minutes")

        return result

    return wrapper


@main.group(invoke_without_command=True)
@click.pass_context
def info(ctx):
    """
    Display information about curret deployment.
    """
    click.secho("System versions", fg="green")
    _echo_version()
    # click.secho("\nInstalled plugins", fg="green")
    # _echo_plugins()

    click.secho("\nGetting help", fg="green")
    click.secho(
        "To get help with ATGtools, join us:\n" "https://discord.com/invite/ygGmxfphAR"
    )


@main.group()
@click.pass_context
def tools(ctx):
    """Command lines tools for NGS preprocessing"""


@tools.command(
    "manifest",
    help="""\b
    Create manifest file for Qiiime2

    FASTQ format filename: ID_R1.fastq.gz, ID_R2.fastq.gz
    """,
    no_args_is_help=True,
)
@click.option("--fqdir", "-d", help="Folder with FASTQ files.")
@click.option(
    "--output", "-o", default="manifest.csv", show_default=True, help="Output file"
)
def create_manifest(fqdir, output):
    """
    Create a manifest file (.csv) from a directory containing FASTQ files.


    Parameters
    ----------
    fqdir : str
        Path to the directory containing input FASTQ files.
    output : str
        Path to the output file.
    """

    _fastq_dir = Path(fqdir).resolve()
    output_manifest = {}
    output = Path(os.getcwd()) / output
    fq_files = [z for x, y, z in os.walk(_fastq_dir)][0]
    prefix = sorted({"_".join(i.split("_")[:1]) for i in fq_files})

    for sample in prefix:
        output_manifest[sample] = (
            f"{_fastq_dir}/{sample}_R1.fastq.gz\t" f"{_fastq_dir}/{sample}_R2.fastq.gz"
        )

    if output.is_file():
        print("There is a previous manifest file")
        sys.exit()
    else:
        with open(output, "w", encoding="utf-8") as f:
            headers = [
                "sample-id",
                "forward-absolute-filepath",
                "reverse-absolute-filepath",
            ]
            f.write("\t".join(headers) + "\n")

            for k, v in output_manifest.items():
                f.write(f"{k}\t{v}" + "\n")


if __name__ == "__main__":
    main(obj={})
