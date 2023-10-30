import requests
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime, timedelta
from pytz import utc, timezone
from dotenv import load_dotenv

load_dotenv()

aware_utc_now = datetime.now(utc)
send_grid_api_key = os.environ.get('SEND_GRID_API_KEY')
recipients = os.environ.get('RECIPIENTS')
sender = os.environ.get('SENDER')
call_number = os.environ.get('CALL_NUMBER')
points = os.environ.get('POINTS')
subject = os.environ.get('SUBJECT')
hours_from_now = 48
trigger_temperature = 32


def check_temperature():
    response = requests.get(
        f"https://api.weather.gov/gridpoints/{points}/forecast/hourly")
    weather_data = response.json()

    alert_times = []
    formatted_alert_times = []
    eastern = timezone('US/Eastern')

    for period in weather_data["properties"]["periods"]:
        start_time = datetime.fromisoformat(
            period["startTime"].replace("Z", "+00:00"))
        if aware_utc_now + timedelta(hours=hours_from_now) > start_time and period["temperature"] <= trigger_temperature:
            alert_times.append(start_time.isoformat())

    if alert_times:
        msg = EmailMessage()
        for time_str in alert_times:
            aware_time = datetime.fromisoformat(time_str).astimezone(eastern)
            formatted_time = aware_time.strftime('%B %d, %I:%M %p')
            formatted_alert_times.append(formatted_time)

        html_content = f'''\
            <html>
            <body>
                <p>A freeze is forecasted for the following date(s):</p>
                <ul>
                {''.join([f"<li>{time}</li>" for time in formatted_alert_times])}
                </ul>
                <p>Please take the following precautions:</p>
                <ul>
                <li>Keep heat set to 60 degrees Fahrenheit or higher</li>
                <li>Cover front and rear spigots</li>
                </ul>
                <p>In case of a burst pipe:</p>
                <ul>
                <li>Turn off water at the main shut-off valve</li>
                <li>Call <a href="tel:{call_number}">{call_number}</a> and listen for prompts to reach an on-call manager</li>
                <li>If the sprinkler system has activated, call 911</li>
                </ul>
                <p>This is an auto-generated email using the 48-hour weather forecast. Please reply to report an issue.</p>
            </body>
            </html>
            '''

        msg.add_alternative(html_content, subtype='html')
        msg["Subject"] = subject
        msg["From"] = sender
        msg["Bcc"] = recipients

        with smtplib.SMTP("smtp.sendgrid.net", 587) as server:
            server.login("apikey", send_grid_api_key)
            server.send_message(msg)


if __name__ == "__main__":
    check_temperature()
