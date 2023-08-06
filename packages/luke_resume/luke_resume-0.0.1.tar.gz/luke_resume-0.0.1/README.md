# Luke's Garzia Resume - CLI App

This represents a weekend project to make writing a resume a tad more interesting.
Specifically --- I wanted to turn the resume into a CLI app and post on pypi.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

[Additional Information on Read the docs](https://luke-resume.readthedocs.io/en/latest/)

## Installation

```shell
>> pip install luke-resume
```

## Usage

There two commands:

- Display in terminal `luke display-resume`
- Open pdf version of resume `luke open-resume`

### Display resume in terminal

Scroll through the whole resume

```shell
>> luke display-resume
```

![Display Resume Example](https://github.com/lgarzia/resume/blob/main/docs/source/_static/luke_full_resume.gif)

## Additional flag is `--num-prev-jobs 3`

View an abridged edition

```shell
>> luke display-resume --abridged
```

![Display Abridged Resume](https://github.com/lgarzia/resume/blob/main/docs/source/_static/luke_display_abridged2.gif)

---

### Open pdf version of resume

Open the pdf version of the resume locally

```shell
>>luke open-resume
```

![Open PDF Resume](https://github.com/lgarzia/resume/blob/main/docs/source/_static/luke_open_resume.gif)

Alternative is `luke open-resume --method web` to open version on GitHub
