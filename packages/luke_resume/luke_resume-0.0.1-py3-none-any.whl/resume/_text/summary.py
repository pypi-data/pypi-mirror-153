"""Generates all text for summary section"""
# Third party imports
import typer

header = typer.style("SUMMARY", fg=typer.colors.GREEN, bold=True)

SUMMARY = f"""{header}
    Demonstrated history of creating solutions that help businesses effectively utilize data
"""


def get_summary() -> str:
    """return formated summary test"""
    return SUMMARY
