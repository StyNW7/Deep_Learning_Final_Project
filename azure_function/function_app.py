import azure.functions as func
import logging
import os
import requests
from pymongo import MongoClient
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.timer_trigger(
    schedule="0 0 * * * *", 
    arg_name="myTimer", 
    run_on_startup=False,
    use_monitor=False
)
def hourly_job(myTimer: func.TimerRequest) -> None:
    logging.info("Timer trigger function started.")

    api_token = os.environ["AQI_TOKEN"]

    api_urls = [
        f"https://api.waqi.info/feed/korea/seoul/jongno-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/jung-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/seodaemun-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/mapo-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/seongdong-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/dongdaemun-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/seongbuk-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/gangbuk-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/dobong-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/yeongdeungpo-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/dongjak-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/gwanak-gu/?token={api_token}",
        f"https://api.waqi.info/feed/korea/seoul/seocho-gu/?token={api_token}"
    ]

    mongo_uri = os.environ["MONGO_URI"]
    db_name = os.environ["DB_NAME"]
    collection_name = os.environ["COLLECTION_NAME"]

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    for url in api_urls:
        try:
            logging.info(f"Calling API: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            collection.insert_one(data)
            logging.info(f"Inserted data from {url}")
        
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")

    logging.info("Timer trigger function finished.")