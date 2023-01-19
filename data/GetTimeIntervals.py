from datetime import datetime, timedelta
import pandas as pd
import re
import sys

stops_path = 'gtfs/stops.txt'
stop_times_path = 'gtfs/stop_times.txt'
routes_path = 'gtfs/routes.txt'

stops = pd.read_csv(open(stops_path))
stop_times = pd.read_csv(open(stop_times_path))
routes = pd.read_csv(open(routes_path))

current_time = datetime.now() #get current time
time_interval = 15 #time interval in min
weekday = current_time.weekday() # from 0 to 6 from Monday to Sunday
current_calendar_type = ''
if weekday <= 4:
    current_calendar_type = 'T0'
elif weekday == 5:
    current_calendar_type = 'T2'
else:
    current_calendar_type = 'T3'

current_stop_coords = (48.0239008179695,7.72459516291335) #get it from click

stop_id = stops[stops['stop_lat'] == current_stop_coords[0]]['stop_id'].item() #extract bus stop id
#stop_id = re.search(r'\w+:\d+:\d+',stop_id).group() #extract more general id (to get all bus stops at the place)

stop_times_prop_arrival = stop_times[pd.to_numeric(stop_times['arrival_time'].str[:2].values) < 24] #eliminate not proper records
stop_times['arrival_time'] = pd.to_datetime(stop_times_prop_arrival['arrival_time'], format='%H:%M:%S').dt.time #change type to time

up_time = (current_time + timedelta(minutes=time_interval)).time() #get time in defined interval in min

buses_current_timeinterval = stop_times[(stop_times['arrival_time'] > current_time.time())&(stop_times['arrival_time'] < up_time)] #get all the records in given interval
all_ids = buses_current_timeinterval['stop_id'].str.contains(stop_id) #get mask for getting records with proper id
buses_interval_location = buses_current_timeinterval[all_ids] #get records in the given interval and with proper id
#sorted_interval = buses_interval_location.sort_values('arrival_time')

#take only nesessary columns
time_interval = buses_interval_location[['arrival_time', 'trip_id']]
try:
    time_interval = time_interval.groupby(by=['arrival_time']).sum()
except:
    sys.exit('No buses within {}'.format(str(time_interval)))

final_table = pd.DataFrame(columns=['bus', 'in_time'])

for time, trips in time_interval['trip_id'].iteritems():
    trip_by_time = trips.split('H')[0]

    cal_type = re.search(r'' + re.escape(current_calendar_type), trip_by_time)
    if cal_type is not None:
        bus = re.findall(r'-(\d+)-', trip_by_time)[0]
        in_time = datetime.combine(current_time.date(), time) - current_time
        in_time = str(in_time).split('.', 2)[0]
        final_table.loc[len(final_table)] = [bus, in_time]

print(final_table)



