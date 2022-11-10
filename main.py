"""
This is a main worker file
It collect data from api call
and validate it.
Finally add into excel file
"""

import time
import datetime as dt
import yaml
import pandas as pd
import device_api as api
import event_trigger as et
#import GUI as gui


final_dict = {}
#global fcount
fcount = -1

#Reading configuration
file = 'config.yml'
data = yaml.safe_load(open(file))
device_com_port = data['Device']
port = device_com_port['port']

def final_data():
    """
    This will parse dictionary for gtw_info and stored separately in parent dict
    :return: final_data in dictionary
    """
    raw_gw = (api.dev_api())
    raw_gw_dict = raw_gw[1] # it is response code and dictionary of response body
    count = 1
    #find fcount and check it is greater than previous fcount
    fcount_api = raw_gw_dict['fcnt']
    global fcount, final_dict

    if fcount_api <= fcount:
        print('Fcount is the same')
    else:
        for gw in raw_gw_dict['gtw_info']:
            raw_gw_dict['gtw-' + str(count)] = gw['gtw_id']
            raw_gw_dict['gtw-' + str(count)+'-rssi'] = gw['rssi']
            raw_gw_dict['gtw-' + str(count)+'-snr'] = gw['snr']
            count += 1
        del raw_gw_dict['gtw_info']
        final_dict.update(raw_gw_dict)
        fcount = fcount_api
    return final_dict

def location(location_name):
    #This is user entered field
    #location = 211
    final_dict['location'] = str(location_name)
    final_dict ["timestamp_current"] = str(dt.datetime.now())


def csv_writer():
    global final_dict
    #print(final_dict)
    final_data_dict = pd.DataFrame([final_dict])
    final_data_dict.to_csv('gw.csv', mode='a', index= False, header= None)
    try:
        gw_number = list(final_dict.items())[-3]
        print("Maximum detected GW = {}".format((gw_number)[0]))
    except:
        print("No GW is available")

    finally:
        final_dict = {}
        #print('Done')

"""This function will trigger event on device using serial connection
and write to CSV.
"""
def device_csv(location_name):
    try:
        et.open_com(port)
        for i in range(5):
            et.ser_read()
            time.sleep(5) # Usually 60 seconds but as timeout of event trigger is 20 seconds we are keeping here \
            # remaining 40 seconds. 15 seconds goes for CSV parsing and writing
            location(location_name) #Location name
            final_data() # To call an api and stored in final_dict
            #print(final_data())
            csv_writer() #write to Csv File
    #due to internet outage or connection drop we must close serial port
    finally:
        et.close_com()

if __name__=='__main__':
    location_name = input("Enter location name= ")
    print('Test begins in the room {}'.format(str(location_name)))
    start_time = dt.datetime.now()
    device_csv(location_name)
    end_time = dt.datetime.now()
    print('Total Time = {}'.format(end_time-start_time))