# **Project Name:** TemperatureAlert
## Description:
##### User will register on this web app. And can set preferrd temperature range and city so that we can send alert message to the user whenever the current teperature of selected city goes out of tha range.
##### Our agent will fetch current temperature for every user's city and check if goes out of bound and the will send alert mail on an interval of 5 minutes.


## Instructions to run the project:
- Clone the repository and move to the directory by executing following commands in terminal
```
git clone https://github.com/ak5154639/TemperatureAlert.git
cd TemperatureAlert
```

- Open two terminal windows in same folder

*Make sure you have already installed python and sqlite3*

- Then install packages used in this project
```
pip install -r requirements.txt
```

- Run python commands to migrate databases
```
python manage.py makemigrations
python manage.py migrate
```

- Run python server
```
python manage.py runserver
```

- In other terminal in the directory i.e, root directory of the project run `agent.py`
```
python agent.py
```

### **Now we can got the the local host server at which out djangoapp is running. And create an account and by deafult selected city will be delhi and preferred range will be 0-100 which can be chenge in the `ChangeCity` tab on topleft corner of app.**

### *Try setting prefferd temperature to check the alert. whenever the current temperature of user's city will go beyond the prefferd range then user will get an alert email.*

*I have used API keys for mailing directly in programs so that judges can test it easily as i used the mail service which is rarely user by others so judges may face issue during testing my project.*
