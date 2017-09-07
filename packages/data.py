import matplotlib.pyplot as plt
import pandas as pd
import glob

def get_bike_data(quarterly_files = 'Indego_Trips_2*.csv', station_file = 'indego_stations.csv'):
    #initializes DF which will hold aggregated csv files
    trip_data = pd.DataFrame() 
    
    #use '*' to get all of the csv files in directory
    for f in glob.glob(quarterly_files): 
        #create dataframe for reading each quarter's csv
        df = pd.read_csv(f, low_memory = False, parse_dates = True) 

        #changes the column names for 2017Q2 to match the rest of the data
        if f =='Indego_Trips_2017Q2.csv':
            df = df.rename(columns ={'end_station': 'end_station_id',
                                'start_station': 'start_station_id'})
            #converts duration from min to seconds
            #df['duration'] = df['duration'].apply(lambda x: x*60)
            
        else:
            #converts duration from seconds to minutes (2017q2 is already in minutes)
            df['duration'] = df['duration'].apply(lambda x: x/60)
            

        #appends current csv to final DF    
        trip_data = trip_data.append(df) 
        
        #converts start and end times into datetime format
        trip_data['start_time'] = pd.to_datetime(trip_data['start_time'])
        trip_data['end_time'] = pd.to_datetime(trip_data['end_time'])


    #reads the 'stations' csv file and renames the columns 
    start_station_data = pd.read_csv(station_file, parse_dates=True, low_memory = False, dtype={'Station ID':float})
    start_station_data = start_station_data.rename(columns={'Station ID': 'start_station_id',
                                                            'Station Name': 'start_station_name',
                                                            'Go live date': 'start_active_date',
                                                            'Status': 'start_status'})

    end_station_data = pd.read_csv(station_file, parse_dates=True, low_memory = False)
    end_station_data = end_station_data.rename(columns={'Station ID': 'end_station_id',
                                                        'Station Name': 'end_station_name',
                                                        'Go live date': 'end_active_date',
                                                        'Status': 'end_status'})
    #merges trip data with the station data to get the start and end station names 
    merge_step_1 = pd.merge(trip_data, start_station_data)
    final_trip_data = pd.merge(merge_step_1, end_station_data)
    
    final_trip_data['count'] = 1

    return final_trip_data
