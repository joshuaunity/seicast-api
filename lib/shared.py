from datetime import datetime, timedelta
from functools import lru_cache

import pandas as pd


file = "./weather.csv"
df = pd.read_csv(file)
df["event_start"] = pd.to_datetime(df["event_start"])
# df["exact_time"] = df.apply(update_datetime, axis=1)


@lru_cache(maxsize=None)  # cache the result
def get_seperated_data() -> dict:
    # get tempterature data
    temperature_data: pd.DataFrame = df.loc[
        df["sensor"] == "temperature",
        ["event_start", "event_value", "belief_horizon_in_sec"],
    ]

    #  get irradiance data
    irradiance_data: pd.DataFrame = df.loc[
        df["sensor"] == "irradiance",
        ["event_start", "event_value", "belief_horizon_in_sec"],
    ]

    # get wind speed data
    wind_speed_data: pd.DataFrame = df.loc[
        df["sensor"] == "wind speed",
        ["event_start", "event_value", "belief_horizon_in_sec"],
    ]

    data = {
        "temperature": temperature_data,
        "irradiance": irradiance_data,
        "wind_speed": wind_speed_data,
    }

    return data


def forecast_then(now: datetime, then: datetime) -> dict:
    data: dict = get_seperated_data()

    # get date from datetime
    date: datetime = then.date()

    temp_date_condition: pd.Series = data["temperature"]["event_start"].dt.date == date
    irradiance_date_condition: pd.Series = (
        data["irradiance"]["event_start"].dt.date == date
    )
    wind_speed_date_condition: pd.Series = (
        data["wind_speed"]["event_start"].dt.date == date
    )

    # get affected rows
    affected_rows_temp: pd.DataFrame = data["temperature"][temp_date_condition]
    affected_rows_irradiance: pd.DataFrame = data["irradiance"][
        irradiance_date_condition
    ]
    affected_rows_wind_speed: pd.DataFrame = data["wind_speed"][
        wind_speed_date_condition
    ]

    # get belief horizon minimums
    temp_min_index: int = affected_rows_temp["belief_horizon_in_sec"].idxmin()
    irradiance_min_index: int = affected_rows_irradiance[
        "belief_horizon_in_sec"
    ].idxmin()
    wind_speed_min_index: int = affected_rows_wind_speed[
        "belief_horizon_in_sec"
    ].idxmin()

    # get the event_value for the minimum belief horizon
    temp_val: float = affected_rows_temp.loc[temp_min_index, "event_value"]
    irradiance_val: float = affected_rows_irradiance.loc[
        irradiance_min_index, "event_value"
    ]
    wind_speed_val: float = affected_rows_wind_speed.loc[
        wind_speed_min_index, "event_value"
    ]

    most_recent_forecasts = {
        "temperature": str(temp_val) + " °C",
        "irradiance": str(round(irradiance_val, 2)) + " W/m^2",
        "wind_speed": str(wind_speed_val) + " m/s",
    }

    return most_recent_forecasts


def forecast_tomorrow(now: datetime) -> dict:
    data = get_seperated_data()

    warm: bool = False
    sunny: bool = False
    windy: bool = False

    # get date from datetime
    date: datetime = now.date() + timedelta(days=1)

    affected_rows_temp: pd.DataFrame = data["temperature"][
        data["temperature"]["event_start"].dt.date == date
    ]
    affected_rows_irradiance: pd.DataFrame = data["irradiance"][
        data["irradiance"]["event_start"].dt.date == date
    ]
    affected_rows_wind_speed: pd.DataFrame = data["wind_speed"][
        data["wind_speed"]["event_start"].dt.date == date
    ]

    # get the average event_value for the day
    temp_val: float = affected_rows_temp["event_value"].mean()
    irradiance_val: float = affected_rows_irradiance["event_value"].mean()
    wind_speed_val: float = affected_rows_wind_speed["event_value"].mean()

    # check if the average temperature is above 20 degrees
    if temp_val > 20:
        warm = True

    # check if the average irradiance is above 200 W/m^2
    if irradiance_val > 200:
        sunny = True

    # check if the average wind speed is above 5 m/s
    if wind_speed_val >= 4:
        windy = True

    tomorrow_forecasts = {
        "warm": warm,
        "sunny": sunny,
        "windy": windy,
    }

    return tomorrow_forecasts
