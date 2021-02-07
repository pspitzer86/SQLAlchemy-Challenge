# Import Dependencies

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# 1. import Flask and creating file path to sqlite file

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

# Create welcome home page with all potential paths

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

# Create precipitation path

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB

    session = Session(engine)

    #Return a list of rain data including the date and prcp of each date
    # then close session

    rain_data = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of HI_rain

    HI_rain = []
    for date, prcp in rain_data:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        HI_rain.append(rain_dict)

    # Make resulting dictionary into a JSON

    return jsonify(HI_rain)

# Create station path

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB

    session = Session(engine)

    # Query out all unique station names and close session

    all_stations = session.query(Station.station).distinct().all()

    session.close()

    # Make resulting station list into a JSON

    return jsonify(all_stations)

# Create temperature data path

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB

    session = Session(engine)

    # Find the most recent date in the data, split it into its parts
    # of the date, and calculate the date one year prior to the most recent date

    recent_date = session.query(func.max(Measurement.date)).scalar()

    split_date = recent_date.split('-')

    query_date = dt.date(int(split_date[0]), int(split_date[1]), int(split_date[2])) - dt.timedelta(days=365)

    # Find the most active station by querying out the station name along
    # with a count of how many measurementd were made by each station
    # ordered descending

    most_active = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

    active_station = most_active[0][0]

    # Query out the data for the most active station within the past year
    # in the data using the calculated date for one year prior and close session

    most_active_info = session.query(Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station == active_station).all()

    session.close()

    # List out all the temperature data from the query and make it into a JSON

    all_tobs = list(np.ravel(most_active_info))

    return jsonify(all_tobs)
    
# Create start path

@app.route("/api/v1.0/<start>")
def temp_stats(start):

    # Create our session (link) from Python to the DB

    session = Session(engine)

    # Query out the max temp, min temp, avg temp between a date entered
    # into by user and all dates greater than entered date and close session

    temps_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                  filter(Measurement.date >= start).all()

    session.close()

    # Grab the max temp, min temp, avg temp from the tuple to be made into a JSON

    statline = [temps_start[0][0], temps_start[0][1], round(temps_start[0][2],2)]

    return jsonify(statline)

# Create start/end path

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_2(start, end):

    # Create our session (link) from Python to the DB

    session = Session(engine)

    # Query out the max temp, min temp, avg temp between a start date
    # end date range entered by the user and close session

    temps_start_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                  filter(Measurement.date >= start).\
                  filter(Measurement.date <= end).all()

    session.close()

    # Grab the max temp, min temp, avg temp from the tuple to be made into a JSON

    statline = [temps_start_end[0][0], temps_start_end[0][1], round(temps_start_end[0][2],2)]

    return jsonify(statline)

# Main function to call the app

if __name__ == '__main__':
    app.run(debug=False)

