import datetime
import os
from forms import WeatherForm
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
import requests

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY', '12345')

URL_WEATHER = 'https://api.openweathermap.org/data/2.5/forecast'
API_KEY_WEATHER = 'a0bdd1c7a07b99650e30e7b60768fceb'


@app.route('/', methods=['POST', 'GET'])
def home():
    weather_form = WeatherForm()
    if weather_form.validate_on_submit():
        body = {
            'q': request.form['location'].strip(),
            'appid': API_KEY_WEATHER
        }

        try:
            response = requests.get(url=URL_WEATHER, params=body)
            response.raise_for_status()
            data = response.json()['list']


        except requests.exceptions.HTTPError:
            flash(f'There is no city called: {request.form['location']}\nTry again!')
            return redirect(url_for('home'))
        except KeyError:
            flash(f'There is no city called: {request.form['location']}\nTry again!')
            return redirect(url_for('home'))
        else:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            weather_data = [{'date': element['dt_txt'], 'temp': round(element['main']['temp'] - 273.15, 1),
                             'temp_max': round(element['main']['temp_max'] - 273.15, 1),
                             'temp_min': round(element['main']['temp_min'] - 273.15, 1),
                             'weather':element['weather'][0]['main'],
                             'description': element['weather'][0]['description']} for element in data]
            weather_today = [element for element in weather_data if
                             element['date'].split(' ')[0] == today]
            weather_rest_days = [element for element in weather_data if
                                 element['date'].split(' ')[0] != today]
            return render_template('index.html', form=weather_form, weather_data_today=weather_today,
                                   weather_data_rest=weather_rest_days, location=request.form['location'].title(),today=today)

    return render_template('index.html', form=weather_form)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
