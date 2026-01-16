"""
Camply Presets Module

Provides pre-configured campgrounds and date ranges for quick searches.

IMPORTANT: Recreation.gov releases new dates at 10 AM Eastern Time daily.
Schedule your monitoring scripts to run at 10:00:01 AM ET for best results.

KEY INSIGHT: Book the FIRST night (Friday) to reserve an entire weekend.
When Friday enters the 6-month window, you can book Fri+Sat+Sun together.
"""

from camply.presets.campgrounds import (
    CAMPGROUNDS,
    get_campground,
    get_campground_ids,
    get_preferred_sites,
    list_campgrounds,
)
from camply.presets.dates import (
    DATE_PRESETS,
    RELEASE_TIME_ET,
    RELEASE_TIME_PT,
    WeekendBookingInfo,
    get_booking_window_end,
    get_newly_available_dates,
    get_next_release_dates,
    get_release_date,
    get_summer_weekends,
    get_summer_weekends_with_booking_info,
    get_upcoming_weekend_releases,
    get_todays_weekend_release,
    get_date_preset,
    print_booking_calendar,
)

__all__ = [
    # Campgrounds
    "CAMPGROUNDS",
    "get_campground",
    "get_campground_ids",
    "get_preferred_sites",
    "list_campgrounds",
    # Dates
    "DATE_PRESETS",
    "RELEASE_TIME_ET",
    "RELEASE_TIME_PT",
    "WeekendBookingInfo",
    "get_booking_window_end",
    "get_newly_available_dates",
    "get_next_release_dates",
    "get_release_date",
    "get_summer_weekends",
    "get_summer_weekends_with_booking_info",
    "get_upcoming_weekend_releases",
    "get_todays_weekend_release",
    "get_date_preset",
    "print_booking_calendar",
]
