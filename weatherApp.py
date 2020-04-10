from flask import Flask,request,render_template
import sys
import Adafruit_DHT
import sqlite3

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

@app.route("/weather_db")
def weatherDb():
    conn = sqlite3.connect('/var/www/web_app/weatherApp.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM temperatures")
    temp_vals = curs.fetchall()
    curs.execute("SELECT * FROM humidity")
    hum_vals = curs.fetchall()
    conn.close()
    return render_template("weatherDb.html",temp=temp_vals,hum=hum_vals)


@app.route("/lab_env_db")
def lab_env_db():
	conn=sqlite3.connect('/var/www/web_app/weatherApp.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures")
	temperatures = curs.fetchall()
	curs.execute("SELECT * FROM humidity")
	humidities = curs.fetchall()
	conn.close()
	return render_template("weatherDb.html",temp=temperatures,hum=humidities)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

