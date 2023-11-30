import pandas as pd


def summarize_pocket_unread_articles(filename: str) -> tuple[pd.Series, int]:
    pocket_save_data: pd.DataFrame = pd.read_csv(filepath_or_buffer=filename)

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

    pocket_data_unread_by_year: pd.Series[int] = pd.Series([])
    for added_year in range(first_year_added, last_year_added + 1):
        this_year_added_count: int = pocket_save_data[
            (pocket_save_data["year_added"] == added_year)
            & (pocket_save_data["status"] == 0)
        ].shape[0]

        this_read_year_saved_year: pd.Series[int] = pd.Series(
            [this_year_added_count], index=[added_year]
        )
        if pocket_data_unread_by_year.shape[0] == 0:
            pocket_data_unread_by_year = this_read_year_saved_year
        else:
            pocket_data_unread_by_year = pd.concat(
                [
                    pocket_data_unread_by_year,
                    this_read_year_saved_year,
                ]
            )

    unread_article_count: int = pocket_data_unread_by_year.sum()

    return pocket_data_unread_by_year, unread_article_count


if __name__ == "__main__":
    FILENAME: str = ".\\data\\Pocket_Saves_2023-11-24T221010.csv"
    unread_data: pd.Series
    unread_count: int
    unread_data, unread_count = summarize_pocket_unread_articles(filename=FILENAME)

    print(f"\nUnread Data\n{unread_data}")
    print(f"\nUnread Count: {unread_count:,.0f}")
