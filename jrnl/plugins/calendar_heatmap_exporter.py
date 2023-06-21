# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import calendar
from datetime import datetime
from typing import TYPE_CHECKING

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.text import Text

from jrnl.plugins.text_exporter import TextExporter
from jrnl.plugins.util import get_journal_frequency_as_dict

if TYPE_CHECKING:
    from jrnl.datatypes import NestedDict
    from jrnl.journals import Entry
    from jrnl.journals import Journal


class CalendarHeatmapExporter(TextExporter):
    """This Exporter displays a calendar heatmap of the journaling frequency."""

    names = ["calendar", "heatmap"]
    extension = "cal"

    @classmethod
    def export_entry(cls, entry: "Entry"):
        raise NotImplementedError

    @classmethod
    def print_calendar_heatmap(cls, journal_frequency: NestedDict) -> str:
        """Returns a string representation of the calendar heatmap."""
        console = Console()
        cal = calendar.Calendar()
        curr_year = datetime.now().year
        curr_month = datetime.now().month
        curr_day = datetime.now().day
        with console.capture() as capture:
            for year, month_journaling_freq in journal_frequency.items():
                year_calendar = []
                for month in range(1, 13):
                    if month > curr_month and year == curr_year:
                        break
                    table = Table(
                        title=f"{calendar.month_name[month]} {year}",
                        style="white",
                        box=box.SIMPLE_HEAVY,
                        padding=0,
                    )

                    for week_day in cal.iterweekdays():
                        table.add_column(
                            "{:.3}".format(calendar.day_name[week_day]), justify="right"
                        )

                    month_days = cal.monthdayscalendar(year, month)
                    for weekdays in month_days:
                        days = []
                        for _, day in enumerate(weekdays):
                            if day == 0:  # Not a part of this month, just filler.
                                day_label = Text(str(day or ""), style="white")
                            elif (
                                day > curr_day
                                and month == curr_month
                                and year == curr_year
                            ):
                                break
                            else:
                                journal_frequency_for_day = (
                                    month_journaling_freq[month][day] or 0
                                )
                                # TODO: Make colors configurable?
                                if journal_frequency_for_day == 0:
                                    day_label = Text(
                                        str(day or ""), style="red on black"
                                    )
                                elif journal_frequency_for_day == 1:
                                    day_label = Text(
                                        str(day or ""), style="black on yellow"
                                    )
                                elif journal_frequency_for_day == 2:
                                    day_label = Text(
                                        str(day or ""), style="black on green"
                                    )
                                else:
                                    day_label = Text(
                                        str(day or ""), style="black on white"
                                    )

                            days.append(day_label)
                        table.add_row(*days)

                    year_calendar.append(Align.center(table))

                # Print year header line
                console.rule(str(year))
                console.print()
                # Print calendar
                console.print(Columns(year_calendar, padding=1, expand=True))
        return capture.get()

    @classmethod
    def export_journal(cls, journal: "Journal"):
        """Returns dates and their frequencies for an entire journal."""
        journal_entry_date_frequency = get_journal_frequency_as_dict(journal)
        return cls.print_calendar_heatmap(journal_entry_date_frequency)
