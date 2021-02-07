# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__Climate__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br\>"
        f"/api/v1.0/tobs<br\>"
        f"/api/v1.0/start<br\>"
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

    all_stations = session.query(Station.station).distinct.all()

    session.close()

    return jsonify(all_stations)




