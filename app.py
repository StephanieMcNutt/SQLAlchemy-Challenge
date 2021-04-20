
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import flask
from flask import Flask , jsonify


#Create Engine & Database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
#Table References
Measurement = Base.classes.measurement
Station = Base.classes.station
#Session
session = Session(engine)

#Flask
app = Flask(__name__)

#Routes
#Home Page-All available routes
@app.route("/")
def home():
    return (f"Home Page <br/>"          
           f" routes <br/>"           
           f"/api/v1.0/precipitation <br/>"           
           f"/api/v1.0/stations <br/>"           
           f"/api/v1.0/tobs <br/>")

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_query = session.query(Measurement.prcp , Measurement.date).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    prdict = {date : x for date , x in prcp_query}
    return jsonify(prdict)
    
#Stations
@app.route("/api/v1.0/stations")
def station():
    st_query = session.query(Station.station).all()
    st_list = list(np.ravel(st_query))
    return jsonify (st_list)

#Tobs
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobs_query))
    return jsonify (tobs_list)


#Temp
@app.route ("/api/v1.0/<start>/<end>")
def temps(start,end):
    temp_query = session.query(Measurement).filter(Measurement.date>= start).filter(Measurement.date<=end)
    found =[] 
    for row in temp_query:
        found.append(row.tobs) 
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))
           
            

if __name__ == "__main__":
   app.run(debug=True)




