from typing import Any, Callable

import pandas as pd


def summarize_pocket_archived_articles(filename: str) -> pd.DataFrame:
    pocket_save_data: pd.DataFrame = pd.read_csv(filepath_or_buffer=filename)

    archived_article_count: int = pocket_save_data[
        pocket_save_data["status"] == 1
    ].shape[0]
    if archived_article_count <= 0:
        return pd.DataFrame()

    pocket_save_data["time_added_dt"] = pd.to_datetime(
        pocket_save_data["time_added"], unit="s"
    )
    pocket_save_data["year_added"] = pocket_save_data["time_added_dt"].dt.year

    pocket_save_data["time_read_dt"] = pd.to_datetime(
        pocket_save_data["time_read"], unit="s"
    )
    pocket_save_data["year_read"] = pocket_save_data["time_read_dt"].dt.year

    first_year_added: int = pocket_save_data["year_added"].min()
    last_year_added: int = pocket_save_data["year_added"].max()

    first_year_read: int = pocket_save_data[pocket_save_data["time_read"] != 0][
        "year_read"
    ].min()
    last_year_read: int = pocket_save_data["year_read"].max()

    pocket_data_archived_summary = pd.DataFrame(
        {}, columns=range(first_year_added, last_year_added + 1)
    )
    for read_year in range(first_year_read, last_year_read + 1):
        this_read_year_by_saved_year: "pd.Series[int]" = pd.Series([])
        for added_year in range(first_year_added, last_year_added + 1):
            this_year_added_count: int = pocket_save_data[
                (pocket_save_data["year_added"] == added_year)
                & (pocket_save_data["year_read"] == read_year)
                & (pocket_save_data["status"] == 1)
            ].shape[0]

            this_read_year_saved_year: pd.Series[int] = pd.Series(
                [this_year_added_count], index=[added_year]
            )
            if this_read_year_by_saved_year.shape[0] == 0:
                this_read_year_by_saved_year = this_read_year_saved_year
            else:
                this_read_year_by_saved_year = pd.concat(
                    [
                        this_read_year_by_saved_year,
                        this_read_year_saved_year,
                    ]
                )
        this_read_year_by_saved_year = pd.concat(
            [
                this_read_year_by_saved_year,
                pd.Series([read_year], index=["read_year"]),
            ]
        )

        isint: Callable([Any], bool) = lambda x: isinstance(x, int)
        years_filter: pd.Series[bool] = pd.Series(
            this_read_year_by_saved_year.index
        ).apply(isint)
        years_filter.index = this_read_year_by_saved_year.index
        this_read_year_by_saved_year_years_only: pd.Series[
            int
        ] = this_read_year_by_saved_year.loc[years_filter]
        total_read_this_year: int = int(this_read_year_by_saved_year_years_only.sum())

        this_read_year_by_saved_year = pd.concat(
            [
                this_read_year_by_saved_year,
                pd.Series([total_read_this_year], index=["Total"]),
            ]
        )

        pocket_data_archived_summary = pd.concat(
            [pocket_data_archived_summary, this_read_year_by_saved_year.to_frame().T]
        )

    pocket_data_archived_summary = pocket_data_archived_summary.astype("int")

    pocket_data_archived_summary.set_index("read_year", inplace=True)

    return pocket_data_archived_summary


if __name__ == "__main__":
    filename: str = ".\\data\\Pocket_Saves_2023-11-24T221010.csv"
    archive_data: pd.DataFrame = summarize_pocket_archived_articles(filename=filename)

    print(f"\nArchive Data\n{archive_data}")
