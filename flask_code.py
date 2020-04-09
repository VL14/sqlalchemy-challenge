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
    f"Welcome To The Climate Starter Homepage<br/><br/>"
    f"The following routes are available:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start_date<br/>"
    f"/api/v1.0/start_date/end_date<br/><br/>"
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

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
    #Return JSON list of min temp, avg temp, and max temp for give start or start-end range
    #When given start only, calculate tmin, tavg, tmax for all dates greater than and equal to start date
    #When given start and end dates, calculate tmin, tavg, and tmax for dates between the start and end date inclusive

    if type(start == str) and (end == None):
        session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    elif type(start == str) & type(end == str):
        session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        print("Start and End values have not been set")

# Runs Flask as an independent program (not a library like pandas)
if __name__ == "__main__":
    app.run(debug=True)
