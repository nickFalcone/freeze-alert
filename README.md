# Freeze Alert
App to send an email when temperatures are forecast to fall below freezing.

## Setup

```
git clone git@github.com:nickFalcone/freeze-alert.git
cd freeze-alert/
python3 -m venv venv
pip install -r requirements.txt
```

Set the following environment variables in `.env`: 

```bash
# https://docs.sendgrid.com/ui/account-and-settings/api-keys
SEND_GRID_API_KEY="my.api.key"
# sender email needs to be verified with Send Grid
SENDER="sender@example.com"
RECIPIENTS="recipient1@example.com, recipient1@example.com"
CALL_NUMBER="8008675309"
# enter lat/long https://api.weather.gov/points/{latitude},{longitude} and use `forecastHourly` for office/pt1,pt2 values
# eg. https://api.weather.gov/gridpoints/AFG/380,355/forecast/hourly
POINTS="AFG/380,355"
SUBJECT="FREEZE ALERT"
```

Modify `hours_from_now` and `trigger_temperature` (Fahrenheit) values in `temperature_alert.py` as needed.


## Run

```bash
python3 temperature_alert.py
```