# sqlalchemy-challenge

## Tools Used
- SQLAlchemy
- Python
- Pandas 
- Matplotlib

## Summary
You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you need to do some climate analysis on the area.

## Climate Analysis and Exploration

* Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.

* Use SQLAlchemy to connect to your sqlite database.

* Use SQLAlchemy to reflect your tables into classes.

### Precipitation Analysis

* Retrieve the last 12 months of precipitation data.

* Load the query results into a Pandas DataFrame.

* Plot the results.

* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Calculate the total number of stations.

* Find the most active stations.

  * List the stations and observation counts in descending order.

  * Which station has the highest number of observations?

* Retrieve the last 12 months of temperature observation data (TOBS).

  * Filter by the station with the highest number of observations.

  * Plot the results as a histogram.

## Climate App

Design a Flask API based on the queries that you have just developed.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
