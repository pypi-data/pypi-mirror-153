"""Entry point to support text related to resume details"""
# Standard library imports
from pathlib import Path

RESUME_NAME = "Luke_Garzia_Resume_202205.pdf"


def get_resume_pdf_path():
    """Returns local path of pdf resume"""
    path = Path(__file__).parent / RESUME_NAME
    print(path)
    return path
