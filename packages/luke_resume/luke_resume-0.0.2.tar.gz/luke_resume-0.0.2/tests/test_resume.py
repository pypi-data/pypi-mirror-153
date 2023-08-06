"""Testing Module - Mostly regression test to make sure functions returning values"""
# resume imports
from resume._text import get_resume_pdf_path
from resume._text.abridged import get_abridged
from resume._text.career_overview import JOB_HISTORY, get_career_overview
from resume._text.contact import get_contact
from resume._text.education import get_education
from resume._text.summary import get_summary
from resume._text.technical_proficiencies import get_technical_proficiencies


def test_pytest_check():
    """test to ensure pytest works"""
    assert True is True


def test_check_path_returns_pdf():
    """Simple check to see if local path returns a pdf"""
    path = get_resume_pdf_path()
    ext = str(path).split(".")[-1]
    assert ext == "pdf"


def test_summary_creation_gets_results():
    """A series of check to ensure content is returned"""
    assert len(get_abridged()) > 10
    assert len(get_career_overview()) > 10
    assert len(JOB_HISTORY) > 1
    assert len(get_contact()) > 1
    assert len(get_education()) > 1
    assert len(get_summary()) > 1
    assert len(get_technical_proficiencies()) > 1


def test_career_overview_num_prev_job():
    """A sanity check to ensure filter is working"""
    assert len(get_career_overview()) > len(get_career_overview(num_prev_jobs=3))
