""" Read list of articles from Pocket """

import datetime as dt
from os.path import join
from urllib.parse import parse_qs, urlencode
from urllib.request import Request, urlopen

import pandas as pd
import requests

from configs.pocket_api_key_file import CONSUMER_KEY
from src.config.config_logging import logger
from src.config.config_main import cfg


def retreive_history(state: str = "unread", count: int = 5_000) -> None:
    """Read list of articles from Pocket"""
    # POST request for token
    url: str = cfg.POCKET.POST_REQUEST_URL  # Set destination URL here

    # Set POST fields here
    post_fields: dict[str, str] = {
        "consumer_key": CONSUMER_KEY,
        "redirect_uri": cfg.POCKET.POST_REQUEST_REDIRECT_URL,
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
    url = cfg.POCKET.POST_AUTHORIZE_URL  # Set destination URL here
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
    parameters = {
        "consumer_key": CONSUMER_KEY,
        "access_token": access_token,
        "state": state,
        "count": count,
    }
    response = requests.get(cfg.POCKET.POST_GET_URL, params=parameters)

    df = pd.DataFrame(response.json()["list"])

    df = df.T

    datestring: str = dt.datetime.strftime(dt.datetime.now(), cfg.APP.DATETIME_FORMAT)

    # Save main Pocker List of Articles, Archived and Unread
    df.to_csv(f"{join(cfg.DATA.FOLDER, cfg.DATA.FILE_PREFIX)}{datestring}.csv")

    # Update Article Count History
    article_count: int = df.shape[0]

    article_count_history: df = pd.read_csv(
        f"{cfg.DATA.ARTICLE_COUNT_HISTORY}", index_col=0
    )

    new_count_history: pd.Series = pd.Series(
        {"datetime": datestring, "count": article_count}
    )

    article_count_history = pd.concat(
        [article_count_history, new_count_history.to_frame().T], ignore_index=True
    )

    article_count_history.to_csv(f"{cfg.DATA.ARTICLE_COUNT_HISTORY}")

    logger.info(
        msg=f"On/at {datestring}, there are {article_count} articles in your Pocket Saves"
    )


if __name__ == "__main__":
    retreive_history(state="all", count=cfg.MAX_ARTICLE_SUMMARY_RETRIEVAL)
