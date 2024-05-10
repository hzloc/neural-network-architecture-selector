import sqlite3

import pandas as pd

from src.utils.db import read_from_table
from src.utils.db import execute_statement, create_view_from_statement
import streamlit as st

st.set_page_config(page_title="Ranking", page_icon="🔝")
st.sidebar.markdown("# Ranks 🔝")

create_view_from_statement(
    "architecture_ranking",
    """
WITH architecture_rank as 
	(SELECT article, metric, dataset, architecture, score,
	 	COUNT(architecture) OVER(PARTITION BY as2.dataset, as2.metric) total_proposed_architecture,
     	CASE 
     	    WHEN metric = 'R2' OR metric = 'MBE' THEN ROW_NUMBER () OVER (PARTITION BY as2.dataset, as2.metric ORDER BY as2.score DESC)
     	    ELSE ROW_NUMBER () OVER (PARTITION BY as2.dataset, as2.metric ORDER BY as2.score)
     	END  architecture_score_rank
 	FROM  article_scores as2)
	select ar.*, a.title, 
	group_concat(architecture, ', ') FILTER(where architecture_score_rank <= 3) OVER (PARTITION BY dataset, metric ORDER BY score RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) top_3rd
	from architecture_rank ar inner join articles a on a.id = ar.article;
	""",
)

st.header("Ranking of the Deep Learning Architectures based on literature review")
st.dataframe(read_from_table(table_name="architecture_ranking"))

st.subheader("**Rank 1st architectures**")
top_1 = execute_statement(
    "SELECT metric, dataset, architecture, score, top_3rd  FROM architecture_ranking ar WHERE architecture_score_rank = 1 GROUP BY metric, dataset"
)
st.dataframe(
    pd.DataFrame(
        top_1, columns=["metric", "dataset", "architechture", "score", "top_3rd"]
    ),
)
