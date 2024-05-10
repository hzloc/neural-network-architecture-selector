import sqlite3

from typing import Optional
import pandas as pd


def connect_to_db(db_name: str = "./src/study.db") -> sqlite3.Connection:
    database = sqlite3.connect(db_name, check_same_thread=False)
    return database


def execute_statement(stmt) -> list:
    res = conn.execute(stmt)
    res = res.fetchall()
    return res


def create_view_from_statement(view_name: str, stmt: str):
    curr = conn.cursor()
    curr.execute(
        f"""
    CREATE TEMP VIEW IF NOT EXISTS {view_name} AS {stmt}
    """
    )
    conn.commit()


def read_from_table(
    table_name: str,
    columns: Optional[list[str]] = None,
    sort_by: Optional[list[str]] = None,
) -> pd.DataFrame:
    curr = conn.cursor()
    if columns is None:
        stmt = f"""SELECT * FROM {table_name} """
    else:
        cols_as_str = ", ".join(columns)
        stmt = f"""SELECT {cols_as_str} FROM {table_name}"""

    res = curr.execute(stmt)
    res = res.fetchall()
    cols = list(map(lambda x: x[0].capitalize(), curr.description))
    df = pd.DataFrame(res, columns=cols)

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], downcast="integer", errors="ignore")
        except Exception:
            pass

    return df


def get_already_scored_articles():
    articles_already_scored = execute_statement(
        """SELECT DISTINCT article FROM article_scores"""
    )
    return articles_already_scored


def insert_into_db(table_name: str, data: pd.DataFrame):
    cur = conn.cursor()
    cols = data.columns
    col_names_str = ", ".join(cols)
    binding_col_names = ", ".join([f":{col}" for col in cols])
    set_clause = ",\n".join([f"{col}=excluded.{col}" for col in cols])

    cur.executemany(
        f"""INSERT INTO {table_name}({col_names_str})
         VALUES({binding_col_names}) 
         ON CONFLICT DO UPDATE SET {set_clause}""",
        data.values,
    )
    conn.commit()


conn = connect_to_db()
