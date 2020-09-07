import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/<start>'>temps start</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>temps start end</a><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all measurements for precipitation within last year
    results = session.query(Measurement.date,Measurement.prcp).filter(and_(Measurement.date >= '2016-08-23',Measurement.date <='2017-08-23')).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all measurements for precipitation
    results = session.query(Station.id,Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all measurements for precipitation
    results = session.query(Measurement.date, Measurement.tobs).filter(and_(Measurement.station == 'USC00519281',Measurement.date >= '2016-08-23',Measurement.date <='2017-08-23')).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start>")
def temps_start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()

    session.close()

 # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start,end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(and_(Measurement.date>=start,Measurement.date<=end)).all()

    session.close()

 # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

if __name__ == "__main__":
    app.run(debug=True)

