"""Generated text of high level bullet points """
# Standard library imports
from typing import List

# Third party imports
import typer

# resume imports
from resume._text.contact import get_contact


def get_abridged() -> str:
    """returns formatted text for abridged edition"""
    contact: str = get_contact()
    ABRIDGED.append(contact)
    return "\n".join(ABRIDGED)


ABRIDGED: List[str] = []

header = typer.style(
    "Past 5 job titles and timeframe", fg=typer.colors.GREEN, bold=True, italic=True
)
text = """
    - Sr Data Engineer, Data Analyst - Equifax Workforce Solutions - 05/2021 - present
    - Director, Data Architect & Analyst - Mastercard - 12/2019 - 05/2021
    - Consultant, Data & Analytics - Slalom Consulting - 07/2019 - 12/2019
    - Interim Director, Talent Analytics - Equifax Workforce Solutions - 05/2019 - 07/2019
    - Data Engineer, Data Analyst - Equifax Workforce Solutions - 01/2018 - 05/2019
"""
ABRIDGED.append(
    f"""{header}
                    {text}"""
)

header = typer.style(
    "Top 3 technical competencies", fg=typer.colors.GREEN, bold=True, italic=True
)
text = """
    - Python Development
    - SQL Development
    - Advance Analytics & Data Mining
"""
ABRIDGED.append(
    f"""{header}
                    {text}"""
)


header = typer.style(
    "Top 3 *recent* projects I'm proud of",
    fg=typer.colors.GREEN,
    bold=True,
    italic=True,
)
text = """
    - Attribution Model Development-> Mixture BigQuery & PySpark to develop an elegant data model and framework tool
    - Airflow framework for Analyst -> simplified to time from development to deploy
    - Designing from the ground up an analytics environment for People Analytics -> Workday + Enterprise Data Science solution
"""
ABRIDGED.append(
    f"""{header}
                    {text}"""
)

header = typer.style(
    "Top 3 business competencies", fg=typer.colors.GREEN, bold=True, italic=True
)
text = """
    - Innovative Problem Solving
    - Numerical Literacy
    - Tactical Project Management
    """
ABRIDGED.append(
    f"""{header}
                    {text}"""
)

header = typer.style(
    "Top 3 areas where I'm investing time",
    fg=typer.colors.GREEN,
    bold=True,
    italic=True,
)
text = """
    - GCP Services
    - Airflow
    - Python Open Source
"""
ABRIDGED.append(
    f"""{header}
                    {text}"""
)
