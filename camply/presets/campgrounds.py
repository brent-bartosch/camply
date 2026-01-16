"""
Campground Presets

Pre-configured campgrounds for quick searches. Add your favorites here
or override with ~/.camply/campgrounds.yaml
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

logger = logging.getLogger(__name__)

# Default campgrounds registry
# These are built-in presets that ship with camply
# "preferred_sites" is an ordered list of campsite IDs (most preferred first)
BUILT_IN_CAMPGROUNDS: Dict[str, Dict[str, Any]] = {
    "kirk_creek": {
        "id": 233116,
        "name": "Kirk Creek",
        "provider": "RecreationDotGov",
        "location": "Big Sur, CA",
        "url": "https://www.recreation.gov/camping/campgrounds/233116",
        # Preferred sites can be added after running: camply list-campsites --campground 233116
        # Sites closer to the ocean/with better views go first
        "preferred_sites": [],  # e.g., [88888, 88889, 88890] - add your favorites
    },
    # Add more built-in campgrounds here
}

# User config file location
USER_CAMPGROUNDS_FILE = Path.home() / ".camply" / "campgrounds.yaml"


def _load_user_campgrounds() -> Dict[str, Dict[str, Any]]:
    """Load user-defined campgrounds from ~/.camply/campgrounds.yaml"""
    if not USER_CAMPGROUNDS_FILE.exists():
        return {}

    try:
        with open(USER_CAMPGROUNDS_FILE, "r") as f:
            data = yaml.safe_load(f)
            if data and "campgrounds" in data:
                return data["campgrounds"]
            return {}
    except Exception as e:
        logger.warning(f"Error loading user campgrounds: {e}")
        return {}


def _get_all_campgrounds() -> Dict[str, Dict[str, Any]]:
    """Merge built-in and user campgrounds (user overrides built-in)"""
    campgrounds = BUILT_IN_CAMPGROUNDS.copy()
    user_campgrounds = _load_user_campgrounds()
    campgrounds.update(user_campgrounds)
    return campgrounds


# Public interface - this gets updated with user campgrounds
CAMPGROUNDS = _get_all_campgrounds()


def refresh_campgrounds() -> None:
    """Reload campgrounds from user config file"""
    global CAMPGROUNDS
    CAMPGROUNDS = _get_all_campgrounds()


def get_campground(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a campground by its preset name.

    Args:
        name: Preset name (e.g., 'kirk_creek')

    Returns:
        Campground dict with id, name, provider, etc. or None if not found
    """
    # Refresh in case user config changed
    refresh_campgrounds()

    # Normalize name (lowercase, underscores)
    normalized = name.lower().replace("-", "_").replace(" ", "_")

    if normalized in CAMPGROUNDS:
        return CAMPGROUNDS[normalized]

    # Try partial match
    for key, campground in CAMPGROUNDS.items():
        if normalized in key or normalized in campground.get("name", "").lower():
            return campground

    return None


def get_campground_ids(names: Union[str, List[str]]) -> List[int]:
    """
    Get campground IDs from preset names.

    Args:
        names: Single name or list of preset names

    Returns:
        List of campground IDs

    Raises:
        ValueError: If a preset name is not found
    """
    if isinstance(names, str):
        names = [names]

    ids = []
    for name in names:
        campground = get_campground(name)
        if campground is None:
            available = list(CAMPGROUNDS.keys())
            raise ValueError(
                f"Unknown campground preset: '{name}'. "
                f"Available presets: {available}"
            )
        ids.append(campground["id"])

    return ids


def get_preferred_sites(name: str) -> List[Union[int, str]]:
    """
    Get the ranked list of preferred campsites for a campground.

    Sites are returned in preference order (most preferred first).
    Use this to prioritize which sites to book when multiple are available.

    Args:
        name: Preset campground name

    Returns:
        List of campsite IDs in preference order, or empty list if none set

    Example:
        >>> sites = get_preferred_sites('kirk_creek')
        >>> # Returns [88888, 88889, 88890] if configured
        >>> # First available site in this list is the best match
    """
    campground = get_campground(name)
    if campground is None:
        return []
    return campground.get("preferred_sites", [])


def list_campgrounds() -> List[Dict[str, Any]]:
    """
    List all available campground presets.

    Returns:
        List of campground dicts with preset_name added
    """
    refresh_campgrounds()
    result = []
    for name, campground in CAMPGROUNDS.items():
        entry = campground.copy()
        entry["preset_name"] = name
        result.append(entry)
    return result


def create_user_config_template() -> str:
    """
    Generate a template for ~/.camply/campgrounds.yaml

    Returns:
        YAML string template
    """
    template = """# Camply Campground Presets
# Add your favorite campgrounds here for quick access
#
# Usage: camply campsites -p kirk_creek --date-preset summer_weekends
#
# IMPORTANT: Recreation.gov releases new dates at 10 AM Eastern Time!
# Schedule your scripts to run at 10:00:01 AM ET for best results.
#
# To sync from Google Sheets (future feature):
# sync_url: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv

campgrounds:
  # Example: Kirk Creek in Big Sur
  kirk_creek:
    id: 233116
    name: Kirk Creek
    provider: RecreationDotGov
    location: Big Sur, CA
    url: https://www.recreation.gov/camping/campgrounds/233116
    # Ranked list of preferred campsites (most wanted first)
    # Run: camply list-campsites --campground 233116
    # to see available site IDs, then add your favorites:
    preferred_sites: []
    # Example with rankings:
    # preferred_sites:
    #   - 88888  # Best ocean view
    #   - 88889  # Second best view
    #   - 88890  # Still good

  # Add more campgrounds below:
  # plaskett_creek:
  #   id: 233362
  #   name: Plaskett Creek
  #   provider: RecreationDotGov
  #   location: Big Sur, CA
  #   url: https://www.recreation.gov/camping/campgrounds/233362
  #   preferred_sites: []
"""
    return template


def ensure_user_config_exists() -> Path:
    """
    Create user config directory and template if they don't exist.

    Returns:
        Path to the user config file
    """
    config_dir = USER_CAMPGROUNDS_FILE.parent
    config_dir.mkdir(parents=True, exist_ok=True)

    if not USER_CAMPGROUNDS_FILE.exists():
        template = create_user_config_template()
        with open(USER_CAMPGROUNDS_FILE, "w") as f:
            f.write(template)
        logger.info(f"Created campground presets file: {USER_CAMPGROUNDS_FILE}")

    return USER_CAMPGROUNDS_FILE
