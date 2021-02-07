import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# 1. import Flask
from flask import Flask, jsonify

import os
import sys

print(os.path.dirname(__file__))

root_project_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, root_project_path)

hawaii_path = os.path.join(root_project_path, "Data/hawaii.sqlite")


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///"+hawaii_path)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
     )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a list of rain data including the date and prcp of each date
    rain_data = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of HI_rain
    HI_rain = []
    for date, prcp in rain_data:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        HI_rain.append(rain_dict)

    return jsonify(HI_rain)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    all_stations = session.query(Station.station).distinct().all()

    session.close()

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    recent_date = session.query(func.max(Measurement.date)).scalar()

    split_date = recent_date.split('-')

    query_date = dt.date(int(split_date[0]), int(split_date[1]), int(split_date[2])) - dt.timedelta(days=365)

    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()

    active_station = most_active[0]

    most_active_info = session.query(Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station == active_station).all()

    session.close()

    all_tobs = list(np.ravel(most_active_info))

    return jsonify(all_tobs)
    

@app.route("/api/v1.0/<start>")
def temp_stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temps_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                  filter(Measurement.date >= start).all()

    session.close()

    statline = [temps_start[0][0], temps_start[0][1], round(temps_start[0][2],2)]

    return jsonify(statline)


@app.route("/api/v1.0/<start>/<end>")
def temp_stats_2(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temps_start_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                  filter(Measurement.date >= start).\
                  filter(Measurement.date <= end).all()

    session.close()

    statline = [temps_start_end[0][0], temps_start_end[0][1], round(temps_start_end[0][2],2)]

    return jsonify(statline)


if __name__ == '__main__':
    app.run(debug=False)

