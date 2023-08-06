"""Generates all text for technical proficiencies"""
# Third party imports
import typer


def get_technical_proficiencies() -> str:
    """return formatted text for technical proficiencies"""
    header = typer.style(
        "TECHNICAL PROFICIENCIES", fg=typer.colors.GREEN, bold=True, italic=True
    )
    text_description = """Python (3.5+, PyData Stack), PySpark, JavaScript (ES6+, Vue),
    Big Data (Cloudera/Hortonworks), Cloud (GCP-BigQuery), NoSQL(MongoDB, Elasticsearch),
    Airflow, Tableau, Traditional ML (scikit-learn, xgboost, statsmodel), Deep Learning (TensorFlow/Keras),
    NLP (Huggingface), Bayesian Data Analytics (pymc3)
    """
    return f"""{header}
    {text_description}"""
