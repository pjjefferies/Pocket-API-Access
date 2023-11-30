""" Get updated Pocket Archive and Unread Data if Latest saved is too old """

import datetime as dt

from src.config.config_main import cfg
from src.datetime_older_than import datetime_older_than
from src.retrieve_history import retreive_history


def get_updated_save_data_if_latest_is_too_old(
    latest_archive_date: dt.datetime, latest_unread_date: dt.datetime
) -> bool:
    """Get updated Pocket_Saves data if latest for either archives or unread is not late enough"""

    archive_data_out_of_date: bool = datetime_older_than(
        latest_archive_date, cfg.MAX_SAVED_DATA_AGE_DAYS
    )
    unread_data_out_of_date: bool = datetime_older_than(
        latest_unread_date, cfg.MAX_SAVED_DATA_AGE_DAYS
    )

    if archive_data_out_of_date or unread_data_out_of_date:
        retreive_history(state="all", count=cfg.MAX_ARTICLE_SUMMARY_RETRIEVAL)
        return True

    return False
