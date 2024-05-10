import streamlit as st
import pandas as pd
import numpy as np
from src.utils.db import read_from_table, insert_into_db, execute_statement


def highlight_existing_articles(s, props: str = ""):
    return (
        [props] * len(s)
        if np.isin(s["Title"], np.array(scored_article_ids))
        else [""] * len(s)
    )


st.header(":rainbow[Add]: ", divider=True)
st.subheader("a score")
with st.form("score", clear_on_submit=False):
    articles = read_from_table("articles", sort_by=["Cite_count"])

    metrics = read_from_table("metrics", ["id"])
    datasets = read_from_table("datasets", ["id"])
    architecture = read_from_table("architectures", ["id"])

    scored_article_ids = execute_statement(
        """SELECT DISTINCT a.*  FROM article_scores as2 inner join articles a ON as2.article = a.id """
    )

    st.dataframe(
        articles.style.apply(
            highlight_existing_articles,
            subset=["Id", "Title"],
            props="color:white;background-color:darkred",
            axis=1,
        ),
    )
    article_ids = articles.loc[:, ["Id"]]

    chosen_article_id = st.selectbox("Article", options=article_ids, key="article")
    # articles.loc[]
    dset, metr, arch = st.columns(3)
    with dset:
        chosen_dataset_name = st.selectbox("dataset", options=datasets, key="dataset")
    with metr:
        chosen_metrics_name = st.selectbox("metrics", options=metrics, key="metrics")
    with arch:
        chosen_architectures_name = st.selectbox(
            "architectures", options=architecture, key="architecture"
        )
    score = st.number_input("Score", key="score")

    button = st.form_submit_button(label="add a score")

    if button:
        try:
            if score is None or score == "":
                raise Exception
            form_data = pd.DataFrame(
                [
                    (
                        chosen_article_id,
                        chosen_dataset_name,
                        chosen_metrics_name,
                        chosen_architectures_name,
                        score,
                    )
                ],
                columns=["article", "dataset", "metric", "architecture", "score"],
            )
            insert_into_db("article_scores", form_data)
            st.success(
                f"**{chosen_metrics_name}**: ***{score}*** of the architecture **{chosen_architectures_name}** has been inserted into db!",
                icon="✅",
            )
        except Exception as exc:
            st.error(f"{score} cannot be inserted into db!", icon="🚨")
            print(exc)

st.subheader(" a metric")
with st.form("metric", clear_on_submit=True):
    metric_id = st.text_input("Metric", key="metric_id")
    button = st.form_submit_button("Add a new metric!")
    if button:
        try:
            if metric_id is None or metric_id == "":
                raise Exception
            form_data = pd.DataFrame([metric_id], columns=["id"])
            insert_into_db("metrics", form_data)
            st.success(f"{metric_id} has been inserted into db!", icon="✅")
        except Exception as exc:
            st.error(f"{metric_id} cannot be inserted into db!", icon="🚨")
            print(exc)

st.subheader(" a architecture")
with st.form("architecture", clear_on_submit=True):
    architecture_id = st.text_input("Architecture", key="architecture_id")
    button = st.form_submit_button("Add a new architecture!")
    if button:
        try:
            if architecture_id is None or architecture_id == "":
                raise Exception
            form_data = pd.DataFrame([architecture_id], columns=["id"])
            insert_into_db("architectures", form_data)
            st.success(f"{architecture_id} has been inserted into db!", icon="✅")
        except Exception as exc:
            st.error(f"{architecture_id} cannot be inserted into db!", icon="🚨")

st.subheader(" a dataset")
with st.form("dataset", clear_on_submit=True):
    dataset_id_col, dataset_url_col = st.columns(2)
    with dataset_id_col:
        dataset_id = st.text_input(
            "Dataset",
            key="dataset_id",
        )
    with dataset_url_col:
        dataset_url = st.text_input("Url", key="dataset_url")
    dataset_availability = st.checkbox(label="Publicly available data", value=True)
    button = st.form_submit_button("Add a new architecture!")
    if button:
        try:
            if dataset_id is None or dataset_id == "":
                raise Exception
            form_data = pd.DataFrame(
                [
                    (
                        dataset_id,
                        dataset_url,
                        dataset_availability,
                    )
                ],
                columns=["id", "url", "available"],
            )
            insert_into_db("datasets", form_data)
            st.success(f"{dataset_id} has been inserted into db!", icon="✅")
        except Exception as exc:
            st.error(f"{dataset_id} cannot be inserted into db!", icon="🚨")
            print(exc)
