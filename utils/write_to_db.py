import csv
from .db_connect import connect
def csv_to_mongo(collection_name, file_path):
    try:
        # Connect to MongoDB

        client,collection =connect(collection_name)

        # Open the input CSV file
        with open(file_path, mode='r', newline='', encoding='utf-8') as input_file:
            reader = csv.DictReader(input_file)
            
            # Prepare a list to store all documents to insert
            data_to_insert = []
            
            for row in reader:
                for itm in row:
                    if row[itm]=='?':
                        row[itm]=None
                data_to_insert.append(row)
            
            # Insert data into MongoDB collection
            if data_to_insert:
                collection.insert_many(data_to_insert)
                print(f"Successfully inserted {len(data_to_insert)} records into the collection '{collection_name}'")
            else:
                print("No data found in the CSV file.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        client.close()

