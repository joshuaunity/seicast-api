from datetime import datetime, timedelta
from shared import forecast_then

data = "2021-04-27 22:00:00+00:00"
# convert to datetime object
data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S%z")


def get_forecast(data):
    result = forecast_then(data)
    return result


print(get_forecast(data))
