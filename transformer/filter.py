from datetime import datetime
from utils.db_connect import connect
from utils.write_to_json import write_dict_to_json

OUTPUT_JSON_PATH = 'output_data.json'

def get_user_ids_in_batches(limit, offset):
    try:
        client,user_collection =connect('User')
        user_ids = user_collection.find({}, {'_id': 1}).skip(offset).limit(limit)
        ids = [dict(user) for user in user_ids]
        return ids
    except Exception as e:
        print(f"An error occurred: {e}")

def moodScore(userId,date):
    start_date = datetime.fromisoformat(date)
    end_date = start_date.replace(hour=23, minute=59, second=59)
    client,mood_collection =connect('Mood')
    for user in userId:
        query = {
            "user": user['_id'],
            "createdAt": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        # Fetch the mood_score
        mood_score= mood_collection.find_one(query)
        if(mood_score):
            user['mood_score']=mood_score['value']
            user['date']=str(start_date)

def seelTime(userId,query_date):
    client,sleep_collection =connect('Sleep')
    for user in userId:
        query = {
            "USER": user['_id'],
            "DATE": query_date  
        }
        # Projection to include only the desired fields
        projection = {
            "SLEEP SCORE": 1,
            "HOURS OF SLEEP": 1,
            "HOURS IN BED": 1,
        }

        # Fetch the mood_score and additional fields
        sleep_score_doc = sleep_collection.find_one(query, projection)
        if sleep_score_doc:
            user['sleep']=dict(sleep_score_doc)


def activities_performed(userId,query_date):
    client,activity_collection =connect('Activity')
    for user in userId:
        query = {
            "USER": user['_id'],
            "DATE": query_date  
        }
        # Projection to include only the desired fields
        projection = {
            "activity": 1,
            "steps": 1,
            "distance": 1,
            "duration": 1,
        }

        # Fetch all activities with the specified projection
        activities = activity_collection.find(query, projection)

        # Convert the cursor to a list of dictionaries (if needed)
        activity_list = list(activities)
        if activity_list:
            user['activity']=dict(activity_list)

def transformer(date):
    date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    date=str(date_object.date())
    # date="2023-11-18" 
    i=0
    while True:
        query_date_format=f"{date_object.month}/{date_object.day}/{str(date_object.year)[2:]}"
        limit = 50  # Number of records to fetch per batch
        offset = i  # Start from the first record
        # Fetch the first batch
        user_details = get_user_ids_in_batches(limit, offset)
        moodScore(user_details,date)
        print(user_details)
        seelTime(user_details,query_date_format)
        activities_performed(user_details,query_date_format)
        print(f'User Details for batch {i} writing to csv ...')
        write_dict_to_json(user_details,OUTPUT_JSON_PATH)
        if(len(user_details)<=50):
            break



