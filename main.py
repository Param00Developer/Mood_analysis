from datetime import datetime
from utils.write_to_db import csv_to_mongo
from transformer.filter import transformer

if __name__=='__main__':
    try:
        csv_to_mongo('Sleep', './data_csv/sleep_data.csv')
        csv_to_mongo('Activity', './data_csv/activity_data_csv.csv')
        #getting today date in Iso format
        today = str(datetime.now().isoformat())
        print(f"Fetching Data for {today}")
        transformer(today)
    except Exception as e:
        print(f"Some error occured {e}")