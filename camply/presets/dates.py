"""
Date Presets

Pre-configured date ranges for common camping search patterns.
Accounts for the 6-month rolling booking window on Recreation.gov.

IMPORTANT: Recreation.gov releases new dates at 10 AM Eastern Time daily.
Schedule your monitoring scripts to run at 10:00:01 AM ET for best results.
"""

import logging
from datetime import date, time, timedelta
from typing import Callable, Dict, List, Optional, Tuple

from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

# Recreation.gov booking window (reservations open 6 months ahead)
BOOKING_WINDOW_MONTHS = 6

# Recreation.gov release time: 10 AM Eastern Time (7 AM Pacific)
# This is when new dates become available daily
RELEASE_TIME_ET = time(10, 0, 0)  # 10:00:00 AM Eastern
RELEASE_TIME_PT = time(7, 0, 0)   # 7:00:00 AM Pacific


def get_booking_window_end() -> date:
    """
    Get the last bookable date (today + 6 months).

    Recreation.gov opens reservations on a rolling 6-month basis.
    New dates are released at 10 AM Eastern Time daily.

    Example: On Jan 15, you can book through July 15.

    Returns:
        The last date currently available for booking
    """
    return date.today() + relativedelta(months=BOOKING_WINDOW_MONTHS)


def get_newly_available_dates(days_ahead: int = 7) -> List[Tuple[date, date]]:
    """
    Get dates that are opening for booking in the next N days.

    Perfect for catching prime spots as they release. Popular campgrounds
    often book up within hours of opening.

    Args:
        days_ahead: Number of days to look ahead (default: 7)

    Returns:
        List of (start_date, end_date) tuples for single-night stays
        on newly available dates

    Example:
        Today is Jan 15, booking window ends July 15.
        This returns dates from July 15 to July 22 (next 7 days of releases).
    """
    booking_end = get_booking_window_end()

    dates = []
    for i in range(days_ahead):
        target = booking_end + timedelta(days=i)
        # Each date is a single-night stay (checkout next day)
        dates.append((target, target + timedelta(days=1)))

    return dates


def get_summer_weekends(
    year: Optional[int] = None,
    only_bookable: bool = True,
    end_month: int = 9,
    end_day: int = 30,
) -> List[Tuple[date, date]]:
    """
    Generate all Friday-Sunday weekends from June through late September.

    Args:
        year: Target year (defaults to current/next based on current date)
        only_bookable: If True, filter to dates within 6-month booking window
        end_month: Month to end search (default: 9 for September)
        end_day: Day of month to end search (default: 30)

    Returns:
        List of (friday, monday) tuples representing weekend stays
        (checkout on Monday)

    Example:
        Today is Jan 15 (booking window ends July 15).
        Returns all June weekends + early July (within window).
        Later dates excluded until they enter the booking window.
    """
    today = date.today()
    if year is None:
        # If we're past September, target next year
        year = today.year if today.month < 10 else today.year + 1

    booking_window_end = get_booking_window_end()

    weekends = []
    current = date(year, 6, 1)
    end = date(year, end_month, end_day)

    while current < end:
        # Find next Friday (weekday 4)
        days_to_friday = (4 - current.weekday()) % 7
        if days_to_friday == 0 and current.weekday() != 4:
            days_to_friday = 7
        friday = current + timedelta(days=days_to_friday)

        if friday < end:
            monday = friday + timedelta(days=3)  # Checkout Monday

            # Filter by booking window if requested
            if only_bookable:
                if friday <= booking_window_end:
                    weekends.append((friday, monday))
            else:
                weekends.append((friday, monday))

        current = friday + timedelta(days=7)

    return weekends


def get_next_release_dates(days_ahead: int = 14) -> List[Tuple[date, date]]:
    """
    Get dates that will be released in the upcoming days.

    Perfect for scheduling daily runs at 10 AM ET to catch new releases.
    Each day at 10 AM ET, one new date (6 months out) becomes bookable.

    Args:
        days_ahead: Number of upcoming release days to include (default: 14)

    Returns:
        List of (start_date, end_date) tuples for the dates being released

    Example:
        Today is Jan 15. Run at 10 AM ET to catch July 15.
        Tomorrow at 10 AM ET, July 16 releases.
        This returns the next 14 days of releases (July 15-28).
    """
    booking_end = get_booking_window_end()

    dates = []
    for i in range(days_ahead):
        target = booking_end + timedelta(days=i)
        # Single night stay for each newly released date
        dates.append((target, target + timedelta(days=1)))

    return dates


# Registry of available date presets
DATE_PRESETS: Dict[str, Callable[[], List[Tuple[date, date]]]] = {
    "summer_weekends": get_summer_weekends,           # June-September weekends
    "newly_available": get_newly_available_dates,     # Dates opening this week
    "next_releases": get_next_release_dates,          # Next 14 days of releases
}


def get_date_preset(name: str) -> List[Tuple[date, date]]:
    """
    Get date ranges for a named preset.

    Args:
        name: Preset name (e.g., 'summer_weekends', 'memorial_day')

    Returns:
        List of (start_date, end_date) tuples

    Raises:
        ValueError: If preset name is not found
    """
    normalized = name.lower().replace("-", "_").replace(" ", "_")

    if normalized not in DATE_PRESETS:
        available = list(DATE_PRESETS.keys())
        raise ValueError(
            f"Unknown date preset: '{name}'. Available presets: {available}"
        )

    return DATE_PRESETS[normalized]()


def list_date_presets() -> List[str]:
    """List all available date preset names."""
    return list(DATE_PRESETS.keys())
