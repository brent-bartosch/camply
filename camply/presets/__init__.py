"""
Camply Presets Module

Provides pre-configured campgrounds and date ranges for quick searches.

IMPORTANT: Recreation.gov releases new dates at 10 AM Eastern Time daily.
Schedule your monitoring scripts to run at 10:00:01 AM ET for best results.
"""

from camply.presets.campgrounds import (
    CAMPGROUNDS,
    get_campground,
    get_campground_ids,
    list_campgrounds,
)
from camply.presets.dates import (
    DATE_PRESETS,
    RELEASE_TIME_ET,
    RELEASE_TIME_PT,
    get_booking_window_end,
    get_newly_available_dates,
    get_next_release_dates,
    get_summer_weekends,
    get_date_preset,
)

__all__ = [
    # Campgrounds
    "CAMPGROUNDS",
    "get_campground",
    "get_campground_ids",
    "list_campgrounds",
    # Dates
    "DATE_PRESETS",
    "RELEASE_TIME_ET",
    "RELEASE_TIME_PT",
    "get_booking_window_end",
    "get_newly_available_dates",
    "get_next_release_dates",
    "get_summer_weekends",
    "get_date_preset",
]
