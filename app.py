from flask import Flask,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import pickle


app = Flask(__name__, template_folder="template")
model = pickle.load(open("votingmodel.pkl", "rb"))
print("Model Loaded")

@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")

@app.route("/predict",methods=['GET', 'POST'])
@cross_origin()
def predict():
	if request.method == "POST":
		# DATE
		year = int(request.form['year'])
		doy = int(request.form['doy'])
		# MinTemp
		minTemp = float(request.form['mintemp'])
		# MaxTemp
		maxTemp = float(request.form['maxtemp'])
        #Temperature
		Temp = float(request.form['temp'])
		# Temperature range
		temprange = float(request.form['temprange'])
		# Dewforest point
		dew = float(request.form['dew'])
		# Earth Skin Temperature
		earthskintemp = float(request.form['earthskintemp'])
		# Wind Speed 2meters
		windSpeed2m = float(request.form['windspeed2m'])
		# Wind Speed 10meters
		windSpeed10m = float(request.form['windspeed10m'])
		# Specific Humidity 
		specifichumidity = float(request.form['specifichumidity'])
		# Relative Humidity
		relativehumidity = float(request.form['relativehumidity'])
		# Surface Pressure 
		pressure = float(request.form['pressure'])
		# Wind  Direction 2meters
		winddDir2m = float(request.form['winddir2m'])
		# Wind Direction 10meters
		winddDir10m = float(request.form['winddir10m'])
		
		input_lst = [year,doy, Temp, dew, earthskintemp, temprange, maxTemp , minTemp  , 
					specifichumidity , relativehumidity, pressure , windSpeed2m ,winddDir2m, windSpeed10m , winddDir10m ]
		pred = model.predict([input_lst,input_lst,input_lst])
		output=abs(round(pred[0],2))
		return render_template("predictor.html",prediction_text='Rainfall Occurance: {} mm/day'.format(output))
	return render_template("predictor.html")

if __name__=='__main__':
	app.run(debug=True)