"""Generate all text for contact section"""
# Third party imports
import typer


def get_contact() -> str:
    """return formated text for Contact Section"""
    header = typer.style("CONTACT", fg=typer.colors.GREEN, bold=True, italic=True)
    text_description = """
    - https://www.linkedin.com/in/luke-garzia/
    """
    return f"""{header}
    {text_description}"""
