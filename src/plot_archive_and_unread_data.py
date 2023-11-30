import os
from typing import Optional

import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from src.config.config_main import cfg


def plot_archive_and_unread_data(
    archive_data: pd.DataFrame,
    unread_data: pd.DataFrame,
    filename: Optional[str] = None,
) -> None:
    """Create line graph of read per year/archive and unread remaining per checked date"""

    # Create the figure and axes
    fig, axs = plt.subplots(
        2, 1, figsize=(cfg.PLOT.FIGURE_SIZE.HORIZ, cfg.PLOT.FIGURE_SIZE.VERT)
    )

    # Increase space between sub-plots
    plt.subplots_adjust(hspace=0.45)

    # Plot the data
    axs[0].plot(archive_data["archive_date"], archive_data["archive_count"])
    axs[1].plot(unread_data["check_date"], unread_data["unread_count"])

    # Set the titles and labels
    axs[0].set_title(cfg.PLOT.ARCHIVE.TITLE)
    axs[0].set_xlabel(cfg.PLOT.ARCHIVE.X_AXIS_TITLE)
    axs[0].set_ylabel(cfg.PLOT.ARCHIVE.Y_AXIS_TITLE)

    axs[1].set_title(cfg.PLOT.UNREAD.TITLE)
    axs[1].set_xlabel(cfg.PLOT.UNREAD.X_AXIS_TITLE)
    axs[1].set_ylabel(cfg.PLOT.UNREAD.Y_AXIS_TITLE)

    # Set Number of Horizontal Axis Labels
    number_of_unread_x_ticks: int = 6
    unread_earliest_date: dt.datetime = min(unread_data["check_date"])
    unread_latest_date: dt.datetime = max(unread_data["check_date"])
    unread_date_label_spacing: dt.timedelta = (
        unread_latest_date - unread_earliest_date
    ) / (number_of_unread_x_ticks - 1)
    unread_date_labels: list[dt.datetime] = [
        x * unread_date_label_spacing + unread_earliest_date
        for x in range(number_of_unread_x_ticks)
    ]
    axs[1].set_xticks(ticks=unread_date_labels)

    # Set lower bounds of Y-Axes to zero
    axs[0].set_ylim(bottom=0)
    axs[1].set_ylim(bottom=0)

    # Format Y-Axes Labesl to use "," for thousands separator
    axs[0].get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    axs[1].get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    # Add data labels to Archive Data Graph, skipping all but last point for latest year
    for point_no, (x, y) in enumerate(
        zip(archive_data["archive_date"], archive_data["archive_count"])
    ):
        if (point_no + 1) < archive_data.shape[0] and x.year == archive_data.at[
            point_no + 1, "archive_date"
        ].year:
            continue
        axs[0].text(
            x,
            y + 100,
            f"{y}",
            fontsize=cfg.PLOT.DATA_LABEL.FONT_SIZE,
            rotation=cfg.PLOT.DATA_LABEL.ROTATION,
        )

    # Add data labels to Unread Data Graph, skipping duplicate lables (same day, count)
    for point_no, (x, y) in enumerate(
        zip(unread_data["check_date"], unread_data["unread_count"])
    ):
        if (
            (point_no + 1) < unread_data.shape[0]
            and x.date() == unread_data.at[point_no + 1, "check_date"].date()
            and y == unread_data.at[point_no + 1, "unread_count"]
        ):
            continue
        axs[1].text(
            x,
            y + 10,
            f"{y}",
            fontsize=cfg.PLOT.DATA_LABEL.FONT_SIZE,
            rotation=cfg.PLOT.DATA_LABEL.ROTATION,
        )

    # Save the plot
    folder: str = cfg.PLOT.FOLDER
    if not filename:
        filename = dt.datetime.strftime(
            dt.datetime.now(), cfg.PLOT.SAVE_IMAGE_FILE_FORMAT
        )
    filepath: str = os.path.join(folder, filename)
    plt.savefig(filepath)

    # Show the plot
    plt.show()
