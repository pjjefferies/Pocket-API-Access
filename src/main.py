""" Main start of Pocket Archive and Unread Data Summary and Plotting """

import datetime as dt

import pandas as pd

from src.get_latest_datetime_of_saved_data import get_latest_datetime_of_saved_data
from src.get_updated_save_data_if_latest_is_too_old import (
    get_updated_save_data_if_latest_is_too_old,
)
from src.plot_archive_and_unread_data import plot_archive_and_unread_data
from src.summarize_pocket_save_data import (
    summarize_pocket_save_data_stage_1,
    summarize_pocket_save_data_stage_2,
)


def main() -> None:
    """Main start of Pocket Archive and Unread Data Summary and Plotting"""
    archive_sum_data: dict[str, pd.DataFrame]
    unread_sum_data: dict[str, int]
    archive_sum_data, unread_sum_data = summarize_pocket_save_data_stage_1()

    last_archive_date: dt.datetime
    last_unread_date: dt.datetime
    last_archive_date, last_unread_date = get_latest_datetime_of_saved_data(
        archive_sum_data, unread_sum_data
    )

    if get_updated_save_data_if_latest_is_too_old(
        latest_archive_date=last_archive_date, latest_unread_date=last_unread_date
    ):
        archive_sum_data, unread_sum_data = summarize_pocket_save_data_stage_1()
        last_archive_date, last_unread_date = get_latest_datetime_of_saved_data(
            archive_sum_data, unread_sum_data
        )

    final_archive_summary_data: pd.DataFrame
    final_unread_summary_data: pd.DataFrame
    (
        final_archive_summary_data,
        final_unread_summary_data,
    ) = summarize_pocket_save_data_stage_2(
        archive_summary_data=archive_sum_data, unread_summary_data=unread_sum_data
    )

    plot_archive_and_unread_data(
        archive_data=final_archive_summary_data, unread_data=final_unread_summary_data
    )


if __name__ == "__main__":
    main()
