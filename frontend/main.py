import requests
import streamlit as st
import pandas as pd
import json
import time

st.title("Job Search Interface")

Jobs = ["Data Analyst", "Data Scientist", "Tech Sales"]

job_search_str = "dummy"

job_search_str = st.selectbox("Looking for a job? Click below 👇", [i for i in Jobs])



if job_search_str != "dummy":   
    res = requests.post(f"http://backend:8080/{job_search_str}")
    res_path = res.json()
    df = res_path.get("jobs")
    df = pd.DataFrame(json.loads(df))
#     df = df_path.get("jobs")
    st.dataframe(df)
    
    

