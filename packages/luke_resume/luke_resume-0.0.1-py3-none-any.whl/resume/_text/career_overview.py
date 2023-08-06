"""Generates all text for career overview section"""
# Standard library imports
from typing import List

# Third party imports
import typer

JOB_HISTORY: List[str] = []  # Assembled below


def get_career_overview(num_prev_jobs: int = 0) -> str:
    """Assembled results"""
    if num_prev_jobs == 0:
        return "\n".join(JOB_HISTORY)
    else:
        return "\n".join(JOB_HISTORY[0 : num_prev_jobs + 1])


# Organized from last to first [last, ... first]
header = typer.style(
    "CAREER OVERVIEW & SELECTED ACHIEVEMENTS",
    fg=typer.colors.GREEN,
    bold=True,
    italic=True,
)
JOB_HISTORY = [header]


def build_career_template(
    *, job_title: str, job_company: str, job_date: str, job_description: str
) -> str:
    """Template - Keyword Only - All Required

    Note: there's not additional formatting applied other then layout. All variables just passed through

    Args:
        job_title: represent job title
        job_company: represent company name
        job_date: preformated text string of date
        job_description: description of job
    Returns:
        Formated Job Section per Job
    """
    # Current Equifax Stint
    job_title = typer.style(job_title, fg=typer.colors.YELLOW, bold=True)
    job_company = typer.style(job_company, fg=typer.colors.BRIGHT_CYAN, italic=True)
    job_date = typer.style(job_date, fg=typer.colors.BRIGHT_CYAN, italic=True)
    return f"""{job_title} - {job_company} - {job_date}
        {job_description}
    """


# Equifax II
efx_ii = {
    "job_title": "Sr. Data Engineer, Data Analyst",
    "job_company": "Equifax Workforce Solutions",
    "job_date": "05/2021-present",
    "job_description": """
        - Architected marketing datamart that captures all user activity across Google Analytics, Pardot,
        Salesforce and inhouse transactional systems; designed and built an attribution model framework in Spark
        - Developed a simple Airflow framework that allows analysts to quickly deploy and schedule BigQuery
        scripts
        - Built a metadata-driven framework in Python that automates the migration of tables from one dataset to
        another - automatically adding or deleting new tables or new columns - scaled to 100s of tables
        - Data Architected & implemented a Google Analytics pipeline using BigQuery stored procedures and
        dynamic SQL to reuse logic across multiple GA sites.
        - Leveraged advanced concepts of BigQuery to solve complex business problems (e.g. JavaScript
        UDF, BiqQuery ML, dynamic SQL & JSON)""",
}
JOB_HISTORY.append(build_career_template(**efx_ii))

# Mastercard
mc = {
    "job_title": "Director, Data Architect & Analyst",
    "job_company": "Mastercard",
    "job_date": "12/2019-05/2021",
    "job_description": """
    - Designed a full analytics environment for People Analytics leveraging Mastercard's enterprise data
      science platform and BI infrastructure
    - Created Workday centric data model and extraction requirement to optimize implementation time and
      adoption curve
    - Led effort to upskill team to the new platform via live sessions and training artifacts
    - Developed the pilot self-service diversity dashboard in Tableau, along with the corresponding data model""",
}
JOB_HISTORY.append(build_career_template(**mc))

# Slalom
contracter_company = typer.style(
    "Fortune 500 Telecommunication Firm", underline=True, fg=typer.colors.MAGENTA
)
contracter_title = typer.style(
    "Data Architect, Data Analyst", italic=True, fg=typer.colors.MAGENTA
)
sl = {
    "job_title": "Consultant, Data & Analytics",
    "job_company": "Slalom Consulting",
    "job_date": "07/2019-12/2019",
    "job_description": f"""
    -  {contracter_company}: {contracter_title}
      - Architected & Developed Fact/Dimension tables into the enterprise data warehouse to
        generate executive dashboards that track the ordering process
      - Worked with IT data visualization team upstream to develop core data structure & logic
        for the operational dashboard related to ordering fallout
      - Provided extensive gap analysis and created/maintained an ongoing issues/risk log""",
}
JOB_HISTORY.append(build_career_template(**sl))

# Equifax - Direct
efx_id = {
    "job_title": "Interim Director, Talent Analytics",
    "job_company": "Equifax Workforce Solutions",
    "job_date": "05/2019-07/2019",
    "job_description": """
    - Led a small team of data analysts and visualization specialists, with responsibility for surfacing innovative
      talent insights for thousands of employers
    - Designed and developed sales enablement dashboards for I9 services to help employers understand
      geographies where they may be out of compliance
    - Architected and implemented an automated data pipeline to enrich and extend Graduate Outcomes
      product""",
}
JOB_HISTORY.append(build_career_template(**efx_id))

# Equifax - Part 1
second_title = typer.style(
    "Team Lead on Talent Analytics", underline=False, fg=typer.colors.MAGENTA
)
second_date = typer.style("12/2018-05/2019", italic=True, fg=typer.colors.MAGENTA)
first_title = typer.style(
    "Data Analyst - Unemployment Consulting", underline=False, fg=typer.colors.MAGENTA
)
first_date = typer.style("01/2018-12/2018", italic=True, fg=typer.colors.MAGENTA)

efx_i = {
    "job_title": "Data Engineer, Data Analyst",
    "job_company": "Equifax Workforce Solutions",
    "job_date": "01/2018-05/2019",
    "job_description": f"""
    - {second_title} - {second_date}
      - Designed a Hadoop ETL pipeline and data model to productionalize custom-analytics solutions
      - Developed a Python/Bokeh codebase to automate generating HTML reports that allowed Equifax Sales
        team to seamlessly distribute talent insights (e.g. benchmarking) to client's HR leaders
      - Mentored fellow team members to adopt standards and best practices; led Data Engineering Guild
        across all scrum team
    - {first_title} - {first_date}
      - Produced initial key metrics for Executives (Market Share, Opportunities, Client Concentration Risk)
      - Built a metadata-driven framework to profile UC databases that generated HTML artifacts with key
        metrics like “fill rate” along with the initial ER diagram
      - Built and implemented a file-based approach to extract and analyze data on an isolated
        server by using Dask and developing a custom-built multiprocessing framework""",
}
JOB_HISTORY.append(build_career_template(**efx_i))

# Daugherty Business Solution

second_company = typer.style(
    "Fortune 500 Pharmacy Benefit Management Firm",
    underline=True,
    fg=typer.colors.MAGENTA,
)
second_title = typer.style("Hadoop Developer", underline=False, fg=typer.colors.MAGENTA)
second_date = typer.style("07/2017-01/2018", italic=True, fg=typer.colors.MAGENTA)

first_company = typer.style(
    "Daugherty Business Solutions", underline=True, fg=typer.colors.MAGENTA
)
first_title = typer.style(
    "Information Analyst II", underline=False, fg=typer.colors.MAGENTA
)
first_date = typer.style("04/2017-07/2017", italic=True, fg=typer.colors.MAGENTA)

dbs = {
    "job_title": "Consultant, Information Analyst",
    "job_company": "Daugherty Business Solutions",
    "job_date": "04/2017-05/2019",
    "job_description": f"""
    - {second_title} - {second_date}
      - Designed and documented the data model schema to build a data mart for
        Pharmacy Technology operational reporting requirements
      - Designed and developed a framework to move data from HDFS into Hive tables
      - Developed Python script to automate building XML required to leverage Oozie

    - {first_title} - {first_date}
      - Participated in an Internal project to identify talent in the STL market by leveraging publicly available
        networks like (GitHub, Meetup, Twitter, LinkedIn, etc.) - goal was to create a recommendation system
      - Wrote Python scripts to scrape websites and interface with Restful APIs as well as coordinate recursive
        calls and store network data into Amazon DynamoDB""",
}
JOB_HISTORY.append(build_career_template(**dbs))

# evolve24
e24 = {
    "job_title": "Technical Specialist, Sr. Data Analyst",
    "job_company": "evolve24",
    "job_date": "08/2016-04/2017",
    "job_description": """
    - Built custom client-facing Tableau dashboards with hourly TDS refreshes via robust SQL that allowed
      clients to monitor brand sentiment across published media and social network sites
    - Leverage Python to automate PowerPoint reports - from MySQL through Excel to PowerPoint
    - Generated and maintained ER Diagram to support the researcher's ad hoc analysis
""",
}
JOB_HISTORY.append(build_career_template(**e24))

# everbank bi transition
eb2 = {
    "job_title": "AVP, Business Intelligence Developer",
    "job_company": "TIAA (formerly EverBank)",
    "job_date": "7/2013-08/2016",
    "job_description": """
    - Built and maintained Banking Operations' data mart that consolidated various data sources that allowed
      executives to monitor the key KPIs related to Banking Operations
    - Automated Executive and Operational (Self Service Model) dashboards using SSIS/Task Scheduler
    - Created a single entry point in SharePoint for the Executive to view metrics from Tableau Server, SSRS,
      Excel & SharePoint
    - Leveraged SSAS Time Series Forecasting model to predict application volumes to help with staffing
""",
}
JOB_HISTORY.append(build_career_template(**eb2))

eb1 = {
    "job_title": "AVP, Product Manager",
    "job_company": "TIAA (formerly EverBank)",
    "job_date": "11/2008-08/2016",
    "job_description": """
    - Team was responsible for the client's new banking account experience - from the external website though
      an internal proprietary queue-based system that processed the request
    - Led effort for complete rewrite/redesign of online customer application
    - Designed process to integrate account opening from physical branches into a centralized hub
    - Built and maintained KPI analytics to monitor and improve customer experience and internal processes

""",
}
JOB_HISTORY.append(build_career_template(**eb1))
