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

