# SkyCast Weather Prototype

Get current weather and forecast data for a city or address [here](https://goo.gl/XUpm4R)

Features
* Returns current weather temperature, humidity, chance for precipitation, and regional alerts for a location
* Returns historical high/low temperature data and historical atmospheric pressure records as a time-variant plot
* User registration and query history
* Embedded Google Map to display search location (helping you confirm the correct locale)

Default Search Example Queries:
* Portland (ambiguous search)
* Portland, OR (state specifier)
* Portland, ME (state specifier)
* Lisbon (potentially ambiguous, but will return the most likely location in Portugal)
* Lisbon, Portugal (country specifier)

Time Machine Search Example Query:
![ExampleTimeMachine](/static/img/example_search_time_machine.PNG)

Time Machine Search Example Result:
![ExampleTimeMachine](/static/img/example_search_time_machine_return.PNG)


Notes:
* The Google API will perform a best-guess search if a location is ambiguous, i.e. Dublin, California, USA versus Dublin, Ireland. It is recommended that you specify regions with comma separators
* The Dark Sky API returns a lot of data that may not necessarily be useful to the average inquirer, such as ozone. The code can be easily modified to return these values. There is also a 1000 request limit per day for a free DarkSky API account, which is why the time machine results only plot one day out of each month instead of every day in a year.
* Replace API details (e.g. YOUR_KEY and username) in the getTimeMachine and getCurrentForecast scripts
* Replace Google Map API key in results.html template (where YOUR_KEY is located)
* Change database information for your database (DBMS, database, username, password) in settings.py

APIs:

[Google Maps](https://developers.google.com/maps): parses location inputs and returning latitude/longitude coordinates

[Dark Sky](https://developer.forecast.io): returns hourly, daily, and current weather data

[Plotly](https://plot.ly/): visualizes historical weather data

Built with:

[Django](https://www.djangoproject.com/)

[AngularJS](https://angularjs.org/)

Hosted on [PythonAnywhere](https://www.pythonanywhere.com/)