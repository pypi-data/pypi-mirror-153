"""CLI Entry Point for Luke Garzia's Resume - Making Resumes fun since 2022"""

# Standard library imports
import webbrowser

# Third party imports
import typer

# resume imports
from resume._text import get_resume_pdf_path
from resume._text.abridged import get_abridged
from resume._text.career_overview import get_career_overview
from resume._text.contact import get_contact
from resume._text.education import get_education
from resume._text.summary import get_summary
from resume._text.technical_proficiencies import get_technical_proficiencies

app = typer.Typer()


def main() -> None:
    """Dispatch to typer"""
    app()


@app.command()
def display_resume(abridged: bool = False, num_prev_jobs: int = 0):
    """Print the whole resume to the terminal or just an abridged version

    Example Usages:
    >> luke display-resume
    >> luke display-resume --abridged
    >> luke display-resume --num-prev-jobs 3

    Args:
        abridged: if set shows a simple, high-level - version
        num-prev-jobs: displays how many jobs to show - 0 means 'all'
    """
    typer.clear()
    if abridged:
        typer.echo("Displaying abridged version")
        typer.echo_via_pager(get_abridged(), color=True)
    else:
        typer.echo(get_summary())
        typer.echo_via_pager(get_career_overview(num_prev_jobs), color=True)
        typer.echo(get_technical_proficiencies())
        typer.echo(get_education())
        typer.echo(get_contact())


@app.command()
def open_resume(method: str = "pdf"):
    """Opens the full resume as either a local pdf or via the web

    Example Usages:
    >> luke open-resume
    >> luke open-resume --method web
    >> luke open-resume --method pdf

    Args:
        method: default is "pdf", also supports web

    Raise:
        ValueError - incorrect method passed in.
    """
    if method == "pdf":
        # Standard library imports
        path = get_resume_pdf_path()
        typer.echo("Opening PDF Locally")
        webbrowser.open_new(path)
    elif method == "web":
        typer.echo("Opening PDF on Github")
        path = r"https://github.com/lgarzia/resume/blob/main/src/resume/_text/Luke_Garzia_Resume_202205.pdf"
        webbrowser.open_new(path)
    else:
        raise ValueError("Unsupported method passed")
