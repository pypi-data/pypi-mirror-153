"""Generates all text for education section"""
# Third party imports
import typer


def get_education() -> str:
    """return formated text for Education Section"""
    header = typer.style("EDUCATION", fg=typer.colors.GREEN, bold=True, italic=True)
    text_description = """
    M.S. Finance - Saint Louis University
    B.S. Electrical Engineering with minor in Applied Mathematics - University of Missouri Science & Technology
    """
    return f"""{header}
    {text_description}"""
