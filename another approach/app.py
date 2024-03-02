from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import pickle
from flask_cors import cross_origin

app = Flask(__name__, template_folder="template")
model = pickle.load(open("votingmodel.pkl", "rb"))
print("Model Loaded")

@app.route("/", methods=["POST","GET"])
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST',"GET"])
@cross_origin()
def predict():
    return render_template("predictor.html")

@app.route("/res", methods=['POST',"GET"])
@cross_origin()
def res():
    try:
        print(request.method=="POST")
        data = request.json
        print(data)
        year = int(data.get('year'))
        doy = int(data.get('doy'))
        minTemp =float( data.get('mintemp'))
        maxTemp = float(data.get('maxtemp'))
        Temp = float(data.get('temp'))
        temprange = float(data.get('temprange'))
        dew = float(data.get('dew'))
        windSpeed2m = float(data.get('windspeed2m'))
        windSpeed10m = float(data.get('windspeed10m'))
        winddDir2m = float(data.get('winddir2m'))
        winddDir10m = float(data.get('winddir10m'))
        specifichumidity = float(data.get('specifichumidity'))
        relativehumidity = float(data.get('relativehumidity'))
        pressure = float(data.get('pressure'))
        earthskintemp = float(data.get('earthskintemp'))
        print(type(year))
        print(year)
        input_lst = [year,doy, Temp, dew, earthskintemp, temprange, maxTemp , minTemp  , 
					specifichumidity , relativehumidity, pressure , windSpeed2m ,winddDir2m, windSpeed10m , winddDir10m ]
        
        print(input_lst)
        for i in input_lst:
            print(i,type(i))
        pred = model.predict([input_lst, input_lst, input_lst])
        print(pred)
        output = abs(round(pred[0], 2))
        print(f"{output = }")

        prediction_text = str(output)
        return jsonify({'prediction_text': prediction_text})
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=True)
