import os
from dotenv import load_dotenv
from fit_tool.profile.profile_type import Sport

load_dotenv()

GPX_INPUT_DIR = os.getenv("GPX_INPUT_DIR")
FIT_OUTPUT_DIR = os.getenv("FIT_OUTPUT_DIR")
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

# optional
STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

# default sport type is running
SPORT_TYPE = Sport.RUNNING
raw_sport_type = os.getenv("SPORT_TYPE")

if raw_sport_type == "running":
    SPORT_TYPE = Sport.RUNNING
elif raw_sport_type == "cycling":
    SPORT_TYPE = Sport.CYCLING
elif raw_sport_type == "hiking":
    SPORT_TYPE = Sport.HIKING
elif raw_sport_type == "swimming":
    SPORT_TYPE = Sport.SWIMMING
else:
    raise ValueError("Unknown sport type")
