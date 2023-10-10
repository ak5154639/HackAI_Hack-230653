from uagents import Agent, Context
from cs50 import SQL
import requests
from decouple import config


db = SQL("sqlite:///db.sqlite3")

whether_agent = Agent(name="whether_agent", seed="whether_agent recovery phrase")

# Mailgun API endpoint and API key
# mailgun_url = "https://api.mailgun.net/v3/sandboxd76437bf0ed44fb383c4bc30ec33c7d3.mailgun.org/messages"
# api_key = "api:0d910673b0c44757a5303320cfd9d972-5465e583-2b06261b"
# api_key = "api:5465e583-2b06261b"


# def SendMail(email):
#     return requests.post(
# 		"https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
# 		auth=("api", "YOUR_API_KEY"),
# 		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
# 			"to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
# 			"subject": "Hello",
# 			"text": "Testing some Mailgun awesomeness!"})

from mailjet_rest import Client


api_key = '9bef5a8dd974e6cfabc11f7dfb07c98b'
api_secret = 'a48a5bf58838271fc573a8827adb18e0'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def sendAlert(userId):
    row = db.execute("SELECT * FROM TemperatureAlert_alerttrack WHERE user_id=?", userId)


    if not row:
        row = db.execute("SELECT * FROM auth_user WHERE id=?", userId)[0]
        (email, name) = (row["email"], row["first_name"])
        data = {
            'Messages': [
                {
                "From": {
                    "Email": "samarbisht123465@gmail.com",
                    "Name": "Aniket"
                },
                "To": [
                    {
                    "Email": email,
                    "Name": name
                    }
                ],
                "Subject": "Temperature Alert",
                "TextPart": "This is email from Temperature Alert App you registered for",
                "HTMLPart": f"<h3>Dear {name}, Temperature in your area is out of your preferred range.",
                "CustomID": email
                }
            ]
        }
        result = mailjet.send.create(data=data)


        if result.status_code == 200:
            print(f"Email sent successfully to ther user {name}.")
            db.execute("INSERT INTO TemperatureAlert_alerttrack (user_id, sent) VALUES(?, True)", userId)
        else:
            print(f"Email sending failed with status code {result.status_code}:")
            print(result.text)

    else:
        row = row[0]
        if not row["sent"]:
            email = db.execute("SELECT * FROM auth_user WHERE id=?", userId)[0]
            (email, name) = (row["email"], row["first_name"])
            data = {
                'Messages': [
                    {
                    "From": {
                        "Email": "samarbisht123465@gmail.com",
                        "Name": "Aniket"
                    },
                    "To": [
                        {
                        "Email": email,
                        "Name": name
                        }
                    ],
                    "Subject": "Temperature Alert",
                    "TextPart": "This is email from Temperature Alert App you registered for",
                    "HTMLPart": f"<h3>Dear {name}, Temperature in your area is out of your preferred range.",
                    "CustomID": email
                    }
                ]
            }
            result = mailjet.send.create(data=data)

            if result.status_code == 200:
                print(f"Email sent successfully to the user {name}.")
                db.execute("UPDATE TemperatureAlert_alerttrack SET sent=True WHERE user_id=?", userId)
            else:
                print(f"Email sending failed with status code {result.status_code}:")
                print(result.text)


@whether_agent.on_interval(period = 5.0)
async def onInterval(ctx: Context):
    data = db.execute("SELECT user_id, lower_temperature, upper_temperature, city FROM TemperatureAlert_tempdata;")
    for row in data:
        result = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config('WEATHER_API_KEY')}&q={row['city']}").json()
        
        if result["current"]["temp_c"] < row['lower_temperature'] or result["current"]["temp_c"] > row['upper_temperature']:
            sendAlert(row['user_id'])

    

if __name__ == "__main__":
    whether_agent.run()