from datetime import datetime
from utils.db_connect import connect
from utils.write_to_json import write_dict_to_json,start_json_file,end_json_file

OUTPUT_JSON_PATH = 'output_data.json'


def getMonogoPipeline(date,limit=0,skip=0):
    pipeline = [
    {
        "$lookup": {
            "from": "Mood",
            "let": { "userId": "$_id" },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                { "$eq": ["$user", "$$userId"] },
                                {
                                    "$eq": [
                                        { "$dateToString": { "format": "%d/%m/%Y", "date": "$createdAt" } },
                                        date
                                    ]
                                }
                            ]
                        }
                    }
                },
                { "$limit": 1 }
            ],
            "as": "moodData"
        }
    },
    {
        "$lookup": {
            "from": "Activity",
            "let": { "userId": "$_id" },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                { "$eq": ["$User", "$$userId"] },
                                { "$eq": ["$Date", date] }
                            ]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "Activity": 1,
                        "Distance": 1,
                        "Duration": 1
                    }
                }
            ],
            "as": "activityData"
        }
    },
    {
        "$lookup": {
            "from": "Sleep",
            "let": { "userId": "$_id" },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                { "$eq": ["$USER", "$$userId"] },
                                { "$eq": ["$DATE", date] }
                            ]
                        }
                    }
                },
                { "$limit": 1 },
                {
                    "$project": {
                        "_id": 0,
                        "SLEEP SCORE": 1,
                        "HOURS OF SLEEP": 1,
                        "HOURS IN BED": 1
                    }
                }
            ],
            "as": "sleepData"
        }
    },
    {
        "$project": {
            "_id": 0,
            "user": "$_id",
            "date": datetime.now().isoformat(),  # Fixed date
            "mood_score": { "$arrayElemAt": ["$moodData.value", 0] },
            "activity": "$activityData",
            "sleep": {
                "sleep_score": { "$arrayElemAt": ["$sleepData.SLEEP SCORE", 0] },
                "hours_of_sleep": { "$arrayElemAt": ["$sleepData.HOURS OF SLEEP", 0] },
                "hours_in_bed": { "$arrayElemAt": ["$sleepData.HOURS IN BED", 0] }
            }
        }
    }
]
    if limit > 0:
        pipeline.append({ "$limit": limit })
        pipeline.append({ "$skip": skip }) 
    return pipeline

def getUserDetails(pipeline):
    try:
        print("here")
        client,user_collection=connect("User")
        results = list(user_collection.aggregate(pipeline))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        return results
    
def transformer(date):
    try:
        date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        date=str(date_object.date())
        i=0
        start_json_file(OUTPUT_JSON_PATH)
        while True:
            limit = 50  # Number of records to fetch per batch
            offset = i  # Start from the first record
            print(f"Limit : {limit}, Offset :{offset}")
            # Fetch the first batch
            pipeline = getMonogoPipeline(date, limit, offset)
            user_details=getUserDetails(pipeline)
            print("🚀 ~ User_details:",user_details)
            write_dict_to_json(user_details,OUTPUT_JSON_PATH)
            if(len(user_details)<=50):
                print(f"Total Batches processed: {i+1}")
                break
        end_json_file(OUTPUT_JSON_PATH)
    except Exception as e:
        print(f"Exception while transforming ::{e}")
        


