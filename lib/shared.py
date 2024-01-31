from datetime import datetime, timedelta
from functools import lru_cache

import pandas as pd


# def update_datetime(row) -> datetime:
#     # print("====================", type(row["event_start"]))
#     # print("====================", type(timedelta(seconds=row["belief_horizon_in_sec"])))
#     return row["event_start"] + timedelta(seconds=row["belief_horizon_in_sec"])


file = "./weather.csv"
df = pd.read_csv(file)
df["event_start"] = pd.to_datetime(df["event_start"])
# df["exact_time"] = df.apply(update_datetime, axis=1)


@lru_cache(maxsize=None)  # cache the result
def get_seperated_data() -> dict:
    # get tempterature data
    temperature_data = df.loc[
        df["sensor"] == "temperature",
        ["event_start", "event_value", "belief_horizon_in_sec"],
    ]

    #  get irradiance data
    irradiance_data = df.loc[
        df["sensor"] == "irradiance",
        ["event_start", "event_value", "belief_horizon_in_sec"],
    ]

    # get wind speed data
    wind_speed_data = df.loc[
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
    data = get_seperated_data()

    # get date from datetime
    date = then.date()

    affected_rows_temp = data["temperature"][
        data["temperature"]["event_start"].dt.date == date
    ]
    affected_rows_irradiance = data["irradiance"][
        data["irradiance"]["event_start"].dt.date == date
    ]
    affected_rows_wind_speed = data["wind_speed"][
        data["wind_speed"]["event_start"].dt.date == date
    ]

    # get belief horizon minimums
    temp_min = affected_rows_temp["belief_horizon_in_sec"].min()
    irradiance_min = affected_rows_irradiance["belief_horizon_in_sec"].min()
    wind_speed_min = affected_rows_wind_speed["belief_horizon_in_sec"].min()

    # get the event_value for the minimum belief horizon
    temp_val = affected_rows_temp[
        affected_rows_temp["belief_horizon_in_sec"] == temp_min
    ]["event_value"].values[0]
    irradiance_val = affected_rows_irradiance[
        affected_rows_irradiance["belief_horizon_in_sec"] == irradiance_min
    ]["event_value"].values[0]
    wind_speed_val = affected_rows_wind_speed[
        affected_rows_wind_speed["belief_horizon_in_sec"] == wind_speed_min
    ]["event_value"].values[0]

    most_recent_forecasts = {
        "temperature": str(temp_val) + " °C",
        "irradiance": str(round(irradiance_val, 2)) + " W/m^2",
        "wind_speed": str(wind_speed_val) + " m/s",
    }

    return most_recent_forecasts


def forecast_tomorrow(now: datetime) -> dict:
    data = get_seperated_data()

    warm = False
    sunny = False
    windy = False

    # get date from datetime
    date = now.date() + timedelta(days=1)

    affected_rows_temp = data["temperature"][
        data["temperature"]["event_start"].dt.date == date
    ]
    affected_rows_irradiance = data["irradiance"][
        data["irradiance"]["event_start"].dt.date == date
    ]
    affected_rows_wind_speed = data["wind_speed"][
        data["wind_speed"]["event_start"].dt.date == date
    ]

    # get the average event_value for the day
    temp_val = affected_rows_temp["event_value"].mean()
    irradiance_val = affected_rows_irradiance["event_value"].mean()
    wind_speed_val = affected_rows_wind_speed["event_value"].mean()

    # check if the average temperature is above 20 degrees
    if temp_val > 20:
        warm = True

    # check if the average irradiance is above 200 W/m^2
    if irradiance_val > 200:
        sunny = True

    # check if the average wind speed is above 5 m/s
    if wind_speed_val > 5:
        windy = True

    tomorrow_forecasts = {
        "warm": warm,
        "sunny": sunny,
        "windy": windy,
    }

    return tomorrow_forecasts
