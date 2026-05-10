import pandas as pd
import json
import requests
import datetime
import time
import pytz

ist = pytz.timezone("Asia/Kolkata")
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)

hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
timestamps = []

for hour in hours:
    dt = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, hour, 0, 0)
    dt_ist = ist.localize(dt)
    timestamps.append(int(dt.timestamp()))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.flightradar24.com",
    "Origin": "https://www.flightradar24.com",
    "Accept": "application/json"
}

airport = ["sxr","ixc","atq","del","ded","jai","udr","lko","vns","ixd","pat","bho","idr","amd","stv","bdq","rpr","bbi","ccu","ixb","gau","bom","pnq","isk","nag","hyd","vtz","goi","blr","ixe","cok","trv","maa","ixm","agx","ixz"]
arr_dep = "arrivals"

id = []
equipment = []
flight_no = []
airline = []
origin = []
origin_code = []
destination = []
destination_code = []
status = []
delayed_color = []
estimated_departure = []
actual_departure = []
estimated_arrival = []
actual_arrival = []

for air in airport:
    for tme in timestamps:
        url = f"https://api.flightradar24.com/common/v1/airport.json?code={air}&plugin[]=&plugin-setting[schedule][mode]={arr_dep}&plugin-setting[schedule][timestamp]={tme}&page=-1&limit=100&fleet=&token="
        data = requests.get(url, headers=headers)
        details = data.json()
        time.sleep(1)
        try:
            flt_records = details['result']['response']['airport']['pluginData']['schedule']['arrivals']['data']
            for record in range(len(flt_records)):
                iden = flt_records[record]['flight']['identification']['id']
                if not iden:
                    id.append("Regional Airline")
                else:
                    id.append(iden)
                try:
                    flight_no.append(flt_records[record]['flight']['identification']['number']['default'])
                except:
                    flight_no.append("Not found")
                try:
                    status.append(flt_records[record]['flight']['status']['text'])
                except:
                    status.append("Not found")
                try:
                    delayed_color.append(flt_records[record]['flight']['status']['icon'])
                except:
                    delayed_color.append("Not found")
                try:
                    equipment.append(flt_records[record]['flight']['aircraft']['model']['text'])
                except:
                    equipment.append("Not found")
                try:
                    airline.append(flt_records[record]['flight']['airline']['name'])
                except:
                    airline.append("Not found")
                try:
                    origin.append(flt_records[record]['flight']['airport']['origin']['name'])
                except:
                    origin.append("Not found")
                try:
                    origin_code.append(flt_records[record]['flight']['airport']['origin']['code']['iata'])
                except:
                    origin_code.append("Not found")
                try:
                    destination.append(details['result']['response']['airport']['pluginData']['details']['name'])
                except:
                    destination.append("Not found")
                try:
                    destination_code.append(air.upper())
                except:
                    destination_code.append("Not found")
                est_dep = (flt_records[record]['flight']['time']['scheduled']['departure'])
                if isinstance(est_dep, int):    
                    estimated_departure.append(datetime.datetime.fromtimestamp(est_dep, tz=ist).strftime("%H:%M"))
                else:
                    estimated_departure.append("Unkown")
                act_dep = (flt_records[record]['flight']['time']['real']['departure'])
                if isinstance(act_dep, int):
                    actual_departure.append(datetime.datetime.fromtimestamp(act_dep, tz=ist).strftime("%H:%M"))
                else:
                    actual_departure.append("Unkown")
                est_arr = (flt_records[record]['flight']['time']['scheduled']['arrival'])
                if isinstance(est_arr, int):
                    estimated_arrival.append(datetime.datetime.fromtimestamp(est_arr, tz=ist).strftime("%H:%M"))
                else:
                    estimated_arrival.append("Unkown")
                act_arr = (flt_records[record]['flight']['time']['real']['arrival'])
                if isinstance(act_arr, int):
                    actual_arrival.append(datetime.datetime.fromtimestamp(act_arr, tz=ist).strftime("%H:%M"))
                else:
                    actual_arrival.append("Unkown")
        except (KeyError, TypeError):
            error = "error"


my_data ={
    "Id":id,
    "Equipment":equipment,
    "Flight_no":flight_no,
    "Airline":airline,
    "Origin":origin,
    "Origin code":origin_code,
    "Destination":destination,
    "Destination code":destination_code,
    "Status":status,
    "Delayed symbol":delayed_color,
    "Scheduled Departue": estimated_departure,
    "Actual Departure": actual_departure,
    "Scheduled Arrival": estimated_arrival,
    "Actual Arrival": actual_arrival
}

df = pd.DataFrame(my_data)
df = df.drop_duplicates()
df.to_excel("arrival flight data.xlsx",index=False)

#Total Flight per Airline
airline_count = df['Airline'].value_counts()
print(airline_count, airline_count.sum())

#Total flights per origin
total_flight = df['Origin'].value_counts()
print(total_flight)
    
#Airline distribution by origin
airline_dist = df[['Origin','Airline']].value_counts()
print(airline_dist)

#Flight counts by Origin and Destination
flt = df[['Origin','Destination']].value_counts()
print(flt)

#Delayed flight per route
flt = df.groupby(['Delayed symbol','Origin','Destination']).size()
print(flt)

#Average delay per route
df['Actual Arrival'] = pd.to_datetime(df['Actual Arrival'], format='%H:%M', errors='coerce')
df['Scheduled Arrival'] = pd.to_datetime(df['Scheduled Arrival'], format="%H:%M",errors='coerce')
df['Delay'] = (df['Actual Arrival']-df['Scheduled Arrival']).dt.total_seconds()/60
data = df.groupby(['Origin','Destination'])['Delay'].mean()
for (origin, dest), avg in data.items():
    print(f"{origin} → {dest}: {avg:.2f} minutes")

#Average delay per airline
df['Actual Arrival'] = pd.to_datetime(df['Actual Arrival'], format='%H:%M', errors='coerce')
df['Scheduled Arrival'] = pd.to_datetime(df['Scheduled Arrival'], format="%H:%M",errors='coerce')
df['Delay'] = (df['Actual Arrival']-df['Scheduled Arrival']).dt.total_seconds()/60
data = df.groupby('Airline')['Delay'].mean()
for air, avg in data.items():
    print(f"{air} average delayed time is {avg:.2f} minutes")

#Average delay per origin
df['Actual Arrival'] = pd.to_datetime(df['Actual Arrival'], format='%H:%M', errors='coerce')
df['Scheduled Arrival'] = pd.to_datetime(df['Scheduled Arrival'], format="%H:%M",errors='coerce')
df['Delay'] = (df['Actual Arrival']-df['Scheduled Arrival']).dt.total_seconds()/60
data = df.groupby('Origin')['Delay'].mean()
for origin, avg in data.items():
    print(f"{origin} average delayed time is {avg:.2f} minutes")

#Equipment usage
data = df["Equipment"].value_counts()
print(data)

#Correlation between equipment type and delay
df['Actual Arrival'] = pd.to_datetime(df['Actual Arrival'], format='%H:%M', errors='coerce')
df['Scheduled Arrival'] = pd.to_datetime(df['Scheduled Arrival'], format='%H:%M', errors='coerce')
df['Delay'] = (df['Actual Arrival'] - df['Scheduled Arrival']).dt.total_seconds() / 60
equipment_delay = df.groupby("Equipment")["Delay"].mean()
equipment_dummy = pd.get_dummies(df['Equipment'], prefix="Equip")
corr_data = pd.concat([equipment_dummy, df['Delay']], axis=1)
corr_mat = corr_data.corr()
print("Correlation with delay:\n", corr_mat["Delay"].sort_values(ascending=False))

