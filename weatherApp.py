from flask import Flask,request,render_template
import sys
import Adafruit_DHT

app = Flask(__name__)
app.debug = True #degugging enabled

@app.route("/")
def hello():
    return "Hello World"

@app.route("/weather")
def weatherDhtSens():
    humVal,tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,19)
    if humVal is not None and tempVal is not None:
        return render_template("weatherApp.html",temp=tempVal,hum = humVal)
    else:
        return render_template("no_sensor.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

