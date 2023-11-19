""" Read list of articles from Pocket """

import datetime as dt
from urllib.parse import parse_qs, urlencode
from urllib.request import Request, urlopen

import pandas as pd
import requests

from configs.pocket_api_key_file import CONSUMER_KEY
from src.config.config_logging import logger
from src.config.config_main import cfg

# POST request for token
url: str = "https://getpocket.com/v3/oauth/request"  # Set destination URL here

# Set POST fields here
post_fields: dict[str, str] = {
    "consumer_key": CONSUMER_KEY,
    "redirect_uri": "http://www.google.com",
}

request = Request(url, urlencode(post_fields).encode())

request_token: str = urlopen(request).read().decode().split("=")[1]
logger.debug(msg=f"{request_token=}")


print(
    f"Go the following URL to accept access:\n"
    f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri=http://www.google.com"
)
wait_to_continue = input("Please press ENTER after accepting access")


# POST request an access token
url = "https://getpocket.com/v3/oauth/authorize"  # Set destination URL here
post_fields = {
    "consumer_key": CONSUMER_KEY,
    "code": request_token,
}  # Set POST fields here
request = Request(url, urlencode(post_fields).encode())
user_access_data = {
    k: v[0] for k, v in parse_qs(urlopen(request).read().decode()).items()
}
logger.debug(msg=user_access_data)

access_token = user_access_data["access_token"]
username = user_access_data["username"]

logger.debug(msg=f"{access_token=}, {username=}")


# GET request for data in JSON format
parameters = {"consumer_key": CONSUMER_KEY, "access_token": access_token}
response = requests.get("https://getpocket.com/v3/get", params=parameters)

df = pd.DataFrame(response.json()["list"])

df = df.T

datestring: str = dt.datetime.strftime(dt.datetime.now(), "%Y-%M-%dT%H%M%S")

df.to_csv(f"{cfg.FILENAMES.ARTICLE_HISTORY_LIST_BASE}{datestring}.csv")

article_count: int = df.shape[0]

article_count_history: df = pd.read_csv(f"{cfg.FILENAMES.ARTICLE_COUNT_HISTORY}")

new_count_history: pd.Series = pd.Series(
    {"datetime": datestring, "count": article_count}
)

article_count_history = pd.concat(
    [article_count_history, new_count_history.to_frame().T], ignore_index=True
)

article_count_history.to_csv(f"{cfg.FILENAMES.ARTICLE_COUNT_HISTORY}")

logger.info(
    msg=f"On/at {datestring}, there are {article_count} articles in your Pocket Saves"
)
