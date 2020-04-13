from flask import Flask,request,render_template
import sys
import Adafruit_DHT
import sqlite3
import datetime
import time
import arrow

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
def weatherProcess():

    temperatures,humidities,timezone,from_date_str,to_date_str = get_records()
    time_adj_temperatures = []
    time_adj_humidities = []
   
    print ("QUERY STRING:= " , request.query_string)


    for record in temperatures:
        local_timedate = arrow.get(record[0],"YYYY-MM-DD HH:mm:ss").to(timezone)
        time_adj_temperatures.append([local_timedate.format('YYYY-MM-DD HH:mm:ss'),round(record[2],2)])
   
               
    for record in humidities:
        local_timedate = arrow.get(record[0],"YYYY-MM-DD HH:mm:ss").to(timezone)
        time_adj_humidities.append([local_timedate.format('YYYY-MM-DD HH:mm:ss'),round(record[2],2)])
   
   
    # print("from date =",from_date_str)
    #print("to date = " ,to_date_str)
   
    return render_template("weatherDb.html",timezone = timezone, temp=time_adj_temperatures,
            hum=time_adj_humidities,
            from_date = from_date_str,
            to_date = to_date_str,
            temp_items=len(temperatures),
            query_string= request.query_string, #This query string is used
            hum_items=len(humidities))



def get_records():
    from_date_str = request.args.get('from',time.strftime("%Y-%m-%d 00:00"))
    to_date_str   = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))
    range_h_form = request.args.get('range_h','');
    timezone = request.args.get('timezone','Etc/UTC');
    range_h_int = "nan" # initialize this variable

    #print("DATE found from =", from_date_str)
    #print("TO DATE =" , to_date_str)
    print(request.args)

    try:
        range_h_int = int(range_h_form)
    except:
        print("range_h_form not a number")


    if not validateDateTime(from_date_str):
        from_date_str = time.strftime("%Y-%m-%d 00:00")
    if not validateDateTime(to_date_str):
        to_date_str = time.strftime("%Y-%m-%d %H:%M")
    
    #create datetime object so that we can convert to UTC from the browser's local time
     
    from_date_obj = datetime.datetime.strptime(from_date_str,'%Y-%m-%d %H:%M')
    to_date_obj   = datetime.datetime.strptime(to_date_str,'%Y-%m-%d %H:%M')


     # If range_h is defined, we don't need the from and to times
    if isinstance(range_h_int,int):
         arrow_time_from = arrow.utcnow().shift(hours=-range_h_int)
         arrow_time_to   = arrow.utcnow()
         from_date_utc   = arrow_time_from.strftime("%Y-%m-%d %H:%M")
         to_date_utc     = arrow_time_to.strftime("%Y-%m-%d %H:%M")
         from_date_str   = arrow_time_from.to(timezone).strftime("%Y-%m-%d %H:%M")
         to_date_str     = arrow_time_to.to(timezone).strftime("%Y-%m-%d %H:%M")
    else:
            #Convert datetimes to UTC so we can retrieve the appropriate records from the database
         from_date_utc   = arrow.get(from_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")
         to_date_utc     = arrow.get(to_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")


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
   
    print("db date = " , from_date_str)
    return [temperatures,humidities,timezone,from_date_str,to_date_str]


            
def validateDateTime(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

