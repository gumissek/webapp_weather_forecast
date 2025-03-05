#author https://github.com/gumissek/webapp_weather_forecast
import datetime
import os
import smtplib
from forms import WeatherForm, EmailForm
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
import requests

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY', '12345')

URL_WEATHER = 'https://api.openweathermap.org/data/2.5/forecast'
API_KEY_WEATHER = os.getenv('API_KEY_WEATHER','a0bdd1c7a07b99650e30e7b60768fceb')
MY_MAIL = os.getenv('MY_MAIL', 'pythonkurskurs@gmail.com')
MY_MAIL_PASSWORD = os.getenv('MY_MAIL_PASSWORD', 'svvbtqswtoxdbchw')


@app.route('/', methods=['POST', 'GET'])
def home():
    weather_form = WeatherForm()
    if weather_form.validate_on_submit():
        location = request.form['location'].title()
        return redirect(url_for('weather_page', location=location))
    return render_template('index.html', form=weather_form)


@app.route('/weather', methods=['POST', 'GET'])
def weather_page():
    email_form = EmailForm()
    location = request.args.get('location')
    body = {
        'q': location.strip(),
        'appid': API_KEY_WEATHER
    }
    try:
        response = requests.get(url=URL_WEATHER, params=body)
        response.raise_for_status()
        data = response.json()['list']

    except requests.exceptions.HTTPError:
        flash(f'There is no location called: {location}\nTry again!')
        return redirect(url_for('home'))
    except KeyError:
        flash(f'There is no location called: {location}\nTry again!')
        return redirect(url_for('home'))
    else:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        weather_data = [{'date': element['dt_txt'], 'temp': round(element['main']['temp'] - 273.15, 1),
                         'temp_max': round(element['main']['temp_max'] - 273.15, 1),
                         'temp_min': round(element['main']['temp_min'] - 273.15, 1),
                         'weather': element['weather'][0]['main'],
                         'weather_id': element['weather'][0]['id'],
                         'description': element['weather'][0]['description']} for element in data]

        weather_today = [element for element in weather_data if
                         element['date'].split(' ')[0] == today]

        weather_rest_days = [element for element in weather_data if
                             element['date'].split(' ')[0] != today]

        is_rain = False

        for element in weather_today:
            if element['weather_id'] < 800:
                is_rain = True
        if email_form.validate_on_submit():
            email = request.form['email']
            with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
                connection.starttls()
                connection.login(MY_MAIL, MY_MAIL_PASSWORD)
                connection.sendmail(from_addr=MY_MAIL, to_addrs=email,
                                    msg=f'Subject:Weather for {today} \n\nIs it going to rain: {is_rain}')
                flash('Email has been sent :3')

        return render_template('weather.html', email_form=email_form, location=location, today=today,
                               weather_data_today=weather_today, weather_data_rest=weather_rest_days)


if __name__ == '__main__':
    app.run(debug=False, port=5001)
