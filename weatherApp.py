from flask import Flask,request,render_template
import sys
import Adafruit_DHT
import sqlite3
import datetime
import time

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


@app.route("/weather_db",methods=['GET'])
def weatherDb():
    from_date_str = request.args.get('from',time.strftime("%Y-%m-%d %H:%M"))
    to_date_str   = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))
    
    
    
    if not validateDateTime(from_date_str):
        from_date_str = time.strftime("%Y-%m-%d 00:00")
    if not validateDateTime(to_date_str):
        to_date_str = time.strftime("%Y-%m-%d %H %M")
    
    conn=sqlite3.connect('/var/www/web_app/weatherApp.db')
    curs=conn.cursor()
    #curs.execute("SELECT * FROM temperatures")
    curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ? ", (from_date_str,to_date_str))
    temperatures = curs.fetchall()
    #curs.execute("SELECT * FROM humidity")
    #humidities = curs.fetchall()
    curs.execute("SELECT * FROM humidity WHERE rDateTime BETWEEN ? AND ? ", (from_date_str,to_date_str)) 
    humidities = curs.fetchall()
    conn.close()
    return render_template("weatherDb.html",temp=temperatures,hum=humidities)


def validateDateTime(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %h:%M')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

