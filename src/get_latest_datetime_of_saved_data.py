"""Find latest datetime in keys of saved data"""
import datetime as dt

import pandas as pd

from src.config.config_main import cfg


def get_latest_datetime_of_saved_data(
    archive_summary_data: dict[str, pd.DataFrame], unread_summary_data: dict[str, int]
) -> tuple[dt.datetime, dt.datetime]:
    """Find latest datetime in keys of saved data"""
    #     Archive data
    latest_archive_date: dt.datetime = max(
        [
            dt.datetime.strptime(datetime, cfg.APP.DATETIME_FORMAT)
            for datetime in archive_summary_data
        ]
    )

    #     Unread data
    latest_unread_date: dt.datetime = max(
        [
            dt.datetime.strptime(datetime, cfg.APP.DATETIME_FORMAT)
            for datetime in unread_summary_data
        ]
    )

    return latest_archive_date, latest_unread_date
