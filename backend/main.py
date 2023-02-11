from fastapi import FastAPI
import uvicorn
import sqlite3
import pandas as pd

from webscraper import *
# from database import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome from Fast API!"}


@app.post("/{job_search_str}")
def job_search_results(job_search_str: str):
    
    db_name = "db"
    table_name = job_search_str.replace(" ", "")
    db_conn = sqlite3.connect('{}.db'.format(db_name))
    df = pd.read_sql_query("SELECT * FROM {};".format(table_name), db_conn)

    return {"jobs": df.to_json()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
