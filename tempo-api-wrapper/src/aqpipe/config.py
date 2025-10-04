AQ_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WX_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

TIMEOUT_S = 20
MAX_CONNECTIONS = 100
MAX_KEEPALIVE = 40
TIMEZONE = "UTC"

# Air Quality API
HOURLY_AQ_VARS = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "carbon_dioxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "aerosol_optical_depth",
    "dust",
    "uv_index",
    "uv_index_clear_sky",
]

# Historical Weather API
HOURLY_WX_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_100m",
    "wind_direction_100m",
]

HW_PAST_DAYS = 7  # 1 week
AQ_PAST_DAYS = 7
AQ_FORECAST_DAYS = 0
