from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Database setup
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

# Reflect database into new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app with a name
app = Flask(__name__)

# Create session link
session = Session(engine)

# Define routes
@app.route("/")
def home():
    return(
    f"<br/>Welcome To The Hawaii Historical Temperature API!<br/><br/><br/>"
    f"The following routes are available:<br/>"
    f"1.) /api/v1.0/precipitation - "
    f"precipitation by date, 2010-01-01 to 2017-08-23<br/>"
    f"2.) /api/v1.0/stations - "
    f"weather stations, ID and station<br/>"
    f"3.) /api/v1.0/tobs - "
    f"temperature observations for most active station, USC00519281, for 12 mos<br/>"
    f"4.) /api/v1.0/start_date OR "
    f"/api/v1.0/start_date/end_date - "
    f"minimum, average, and maximum temperatures for user-defined start or start/end range<br/><br/>"
    f" *Start and end dates should be entered in this format: yyyy-mm-dd"
    )
@app.route("/api/v1.0/precipitation")
def precip():
    #Convert query results to a dictionary using 'date' as the key and 'prcp' as the value
    precip_results = session.query(Measurement.date, Measurement.prcp).all()
    precip_data = []
    for date, prcp in precip_results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        precip_data.append(precip_dict)

    session.close()
    
    #Return JSON of dictionary
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    #Return JSON list of stations from the dataset
    stations_list = session.query(Measurement.id, Measurement.station).group_by(Measurement.station).all()

    session.close()

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def temp():
    #Query the dates and temp observations of most active station for the last year of data
    #Return JSON list of temp observations (tobs) for the previous year
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').filter_by(station='USC00519281').     order_by(Measurement.date).all()

    session.close()

    return jsonify(tobs)   

@app.route("/api/v1.0/test/<start>")
@app.route("/api/v1.0/test/<start>/<end>")
def start(start="2016-08-23", end="2017-08-23"):
    #Return JSON list of min temp, avg temp, and max temp for give start or start-end range
    #When given start only, calculate tmin, tavg, tmax for all dates greater than and equal to start date
    #When given start and end dates, calculate tmin, tavg, and tmax for dates between the start and end date inclusive

    if (start is not None) and (end is None):
        start = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

        return jsonify(start)

    elif (start is not None) &(end is not None):
        start_end = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        return jsonify(start_end)
    else:
        print("Start and End values have not been set")

# Runs Flask as an independent program (not a library like pandas)
if __name__ == "__main__":
    app.run(debug=True)
