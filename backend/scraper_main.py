from webscraper import *
from database import *



if __name__ == '__main__':
    
    for title in ["Data Analyst", "Data Scientist", "Tech Sales"]:
               
        
        # execute the command to webscrape
        job_search_results = job_search(title=title, location="Singapore", n_pages=2)
        job_search_results.main()

        # add entries to the database
        table_name = title.replace(" ", "") #+ "_" + location

        db = database(db_name="db", table_name=table_name, df_results=job_search_results.results)
        db.main()


    
 