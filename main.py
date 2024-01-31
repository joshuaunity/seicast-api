import uvicorn
from datetime import datetime
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from lib.shared import forecast_then, forecast_tomorrow


app = FastAPI()


class NowAndThen(BaseModel):
    now: datetime
    then: datetime


@app.get("/", tags=["Personal"])
def welcome_page():
    info = "These are Josh's APIs"
    return info


@app.post("/forecast")
async def forecast(request: Request):
    request: dict = await request.json()
    now: datetime = request["now"]
    then: datetime = request["then"]
    now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S%z")
    then = datetime.strptime(then, "%Y-%m-%d %H:%M:%S%z")

    # check if input string is in the correct format
    if now is None or then is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, error="Incorrect date format"
        )

    # check if now is before then
    if now > then:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, error="Now must be before then"
        )

    # check if now is equal to then
    if now == then:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, error="Now cannot be equal to then"
        )

    # get the forecast
    forecast: dict = forecast_then(now, then)
    return JSONResponse(status_code=status.HTTP_200_OK, content=forecast)


@app.post("/tomorrow")
async def tomorrow(request: Request):
    request = await request.json()
    now = request["now"]
    now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S%z")

    # check if input string is in the correct format
    if now is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, error="Incorrect date format"
        )

    # get the forecast
    forecast: dict = forecast_tomorrow(now)
    return JSONResponse(status_code=status.HTTP_200_OK, content=forecast)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
