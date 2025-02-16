import requests
import json
from dataclasses import dataclass
import random
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
pushover_api_key = os.getenv('PUSH_OVER_API_GOOD_MORNING')
pushover_user_key = os.getenv('PUSH_OVER_USER_KEY')

sgt_timezone = pytz.timezone('Asia/Singapore')
collection_name = "good_morning_quotes"
notification_topic = "dbarr_good_morning_smiles"
headers = {"Firebase": "yes"}
payload_data = {
    "topic": notification_topic,
    "markdown": True,
    "title": "Good morning with a smile 🙂",
    "tags": ["sunny"]
}

quotes_data = {
    "Kahlil Gibran": "data/kg-quotes.json",
    "Bhagawad Gita": "data/gita-quotes.json",
    "Rumi": "data/rumi-quotes.json"
}


@dataclass
class Quote:
    quote: str = "Good morning! Have a great day ahead! 🌞"
    source: str = None

    def __str__(self):
        return self.quote if self.source is None else f"{self.quote} [{self.source}]"


def push_notify(data):
    push_url = "https://ntfy.sh/"
    payload_data["message"] = data.__str__()
    print(payload_data)
    requests.post(push_url, data=json.dumps(payload_data), headers=headers)


def get_quote_for_today() -> Quote:
    quote_source = random.choice(list(quotes_data.keys()))
    add_source = False if quote_source == "Bhagawad Gita" else True
    quotes_file = quotes_data[quote_source]
    with open(quotes_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    quote = random.choice(data["quotes"])
    source = quote_source if add_source else None
    return Quote(quote=quote, source=source)


def send_to_pushover(quote):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": pushover_api_key,
        "user": pushover_user_key,
        "message": quote.__str__()
    }

    response = requests.post(url, data=data)
    print(response.status_code, response.json())


def process(send_notification):
    quote = get_quote_for_today()
    print(quote)
    if send_notification:
        push_notify(quote)
        send_to_pushover(quote)


if __name__ == '__main__':
    process(send_notification=True)
