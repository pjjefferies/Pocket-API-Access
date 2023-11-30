""" Get saved data in data folder and show summary over time of unread and archive articles in text and graphic forms """

import os
import datetime as dt

import pandas as pd

from src.summarize_pocket_archived_articles import summarize_pocket_archived_articles
from src.summarize_pocket_unread_articles import summarize_pocket_unread_articles
from src.config.config_logging import logger
from src.config.config_main import cfg


def summarize_pocket_save_data_stage_1() -> (
    tuple[dict[str, pd.DataFrame], dict[str, int]]
):
    """
    Get Saved Data in data folder and save archived and unread summaries in dictionary of DataFrames with datetimes strings as keys
    """

    # Get summary data from saved data in data folder
    saved_files: list[list[str]] = [
        [filename, filename[13:-4]]
        for filename in os.listdir(cfg.DATA.FOLDER)
        if filename.startswith(cfg.DATA.FILE_PREFIX)
    ]

    archive_summary_data: dict[str, pd.DataFrame] = {}
    unread_summary_data: dict[str, int] = {}

    for filename, file_dt in saved_files:
        filepath: str = os.path.join(cfg.DATA.FOLDER, filename)
        archive_data: pd.DataFrame = summarize_pocket_archived_articles(filepath)
        if not archive_data.empty:
            archive_summary_data[file_dt] = archive_data

        unread_count: int
        _, unread_count = summarize_pocket_unread_articles(filepath)
        unread_summary_data[file_dt] = unread_count

    return archive_summary_data, unread_summary_data


def summarize_pocket_save_data_stage_2(
    archive_summary_data: dict[str, pd.DataFrame], unread_summary_data: dict[str, int]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create new DataFrame with total read per year and unready by datetime of data"""
    # Archive Data
    #     First get previous year archive totals
    this_year: int = dt.datetime.now().year
    latest_archive_data_date: str = dt.datetime.strftime(
        max(
            [
                dt.datetime.strptime(datetime_str, cfg.APP.DATETIME_FORMAT)
                for datetime_str in archive_summary_data
            ]
        ),
        cfg.APP.DATETIME_FORMAT,
    )
    last_saved_archive_data: pd.DataFrame = archive_summary_data[
        latest_archive_data_date
    ]

    archive_dates: pd.Series = pd.Series(
        [
            dt.datetime(year, 1, 1, 12)
            for year in last_saved_archive_data.index
            if year != dt.datetime.now().year
        ]
    )

    archive_counts: pd.Series = pd.Series(
        [
            last_saved_archive_data.at[year, "Total"]
            for year in last_saved_archive_data.index
            if year != dt.datetime.now().year
        ]
    )

    #     Second get this year archive history
    this_year_saved_archive_totals_dict: dict[str, int] = {
        datetime_str: archive_summary_data[datetime_str].at[
            int(datetime_str[:4]), "Total"
        ]
        for datetime_str in archive_summary_data
        if datetime_str[:4] == str(this_year)
    }
    this_year_saved_archive_totals: pd.DataFrame = pd.DataFrame(
        data=this_year_saved_archive_totals_dict.values(),
        index=this_year_saved_archive_totals_dict.keys(),
        columns=["Totals"],
    )

    archive_dates = pd.concat(
        [archive_dates, pd.to_datetime(pd.Series(this_year_saved_archive_totals.index))]
    )
    archive_counts = pd.concat(
        [archive_counts, this_year_saved_archive_totals["Totals"]]
    )

    new_archive_data: pd.DataFrame = pd.DataFrame(
        {"archive_date": list(archive_dates), "archive_count": list(archive_counts)}
    )

    # Unread Data
    unread_dates: list[str] = list(unread_summary_data.keys())
    unread_counts: list[int] = list(unread_summary_data.values())

    new_unread_data: pd.DataFrame = pd.DataFrame(
        {"check_date": unread_dates, "unread_count": unread_counts}
    )
    new_unread_data["check_date"] = pd.to_datetime(
        arg=new_unread_data["check_date"], format=cfg.APP.DATETIME_FORMAT
    )

    return new_archive_data, new_unread_data
