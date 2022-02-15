# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 08:27:24 2021

@author: hoarau
"""
# importing the requests library

import base64
import datetime
import os

import pandas
import requests

import api_pb2


### INSTRUVTIONS FOR THE BEGINING #########################################################"
# download protobuf compiler named protoc in the internet, then put the file "protoc.exe"
# into this folder and execute the 4 following command lines
############################################################################################"

# src = r"C:\Users\ENA\PycharmProjects\pythonProjectAPI"  ##### TO CHANGE !!
# srcProto = r"C:\Users\ENA\PycharmProjects\pythonProjectAPI\api.proto"  ##### TO CHANGE !!


# protoc= cd C:\Users\ENA\PycharmProjects\pythonProjectAPI\protoc.exe  ##### TO EXECUTE
# protoc -I=. --python_out=. ./api.proto

##### VERIFICATION : IF THE PROTOC IS OK ? ############################
# (venv) C:\Users\hoarau\PycharmProjects\pythonProject>protoc --version
# libprotoc 3.17.3
######################################################################"

def func_main_list_vehicle():
    ##1°###### Get the token with post request #################

    url_token = 'https://lapin.stg.navya.cloud/auth/token'
    # url_token = 'https://lapin-preprod.navya.cloud/auth/token'
    params = {'username': 'projet-ena-api@univ-eiffel.fr', 'password': 'c9Vt7Ejg4ZMHHH3!'}

    token = requests.post(url_token, data=params)
    token24h = token.text
    print(token24h)

    vehicle_list = api_pb2._VEHICLESTATEMESSAGE

    ##2°###### send and receive with get method ###############

    # api-endpoint
    # url = "https://lapin.stg.navya.cloud/fleet/vehicle/all"
    url = "https://lapin.stg.navya.cloud/monitoring/state/vehicle/all"
    authorization = 'Bearer ' + token24h
    r = requests.get(url, headers={'Authorization': authorization})

    ##3°## DECODING#############################################
    # first of all, you had to create: modeTest.txt, restultats.txt, resultatsm.txt, modeTestm.txt

    data_decode = base64.b64decode(r.content)
    interest_message = api_pb2.UserStatesMessage.FromString(data_decode)

    ##4a°## writing in text#####################################
    """ 
    f = open('modeTest.txt', "wb")
    f.write(api_pb2.UserStatesMessage.SerializeToString(interestMessage))
    f.close()
    v = api_pb2.UserStatesMessage()
    # Read
    f = open('modeTest.txt', "rb")
    v.ParseFromString(f.read())
    f.close()
    # result file:
    resultats = open('resultats.txt', "a+")
    v_text = proto.MessageToString(v)
    resultats.write(v_text)
    resultats.close()
    """

    print(interest_message)

    ##4b°######### get fields in the message##################

    nb_big_item = len(interest_message.messages)
    len_item = len(interest_message.messages.__getitem__(1).states)
    d = {'timestamp': [], 'heurePC': [], 'idShuttle': [], 'hit_ratio': [], 'setupVersion': [], 'lat': [], 'lon': [],
         'orientation': [],
         'speed': [],
         'mileage': [], 'instMileage': [], 'indoorTemperature': [], 'outdoorTemperature': [], 'switchManual': [],
         'batteryLevel': [], 'batteryState': [], 'instConsumption': [], 'doorsState': [], 'vehicle__mode': [],
         'robot_mode': [], 'driving_direction': []}
    df = pandas.DataFrame(d)

    for i in range(0, nb_big_item):

        # mandatory fields
        timestamp = interest_message.messages.__getitem__(i).date.timestamp
        id_shuttle = interest_message.messages.__getitem__(i).vehicle_id

        # initializing the data
        hit_ratio = ''
        lat = ''
        lon = ''
        setupVersion = ''
        orientation = ''
        speed = ''
        mileage = ''
        instMileage = ''
        indoorTemperature = ''
        outdoorTemperature = ''
        switchManual = ''
        batteryLevel = ''
        batteryState = ''
        instConsumption = ''
        doorsState = ''
        vehicle_mode = ''
        robot_mode = ''
        driving_direction = ''

        for j in range(0, len_item):
            a = interest_message.messages.__getitem__(i).states.__getitem__(j)
            heure_pc = datetime.datetime.now().time()

            """ Example of a response"""
            """
            messages
            {
                vehicle_id: "VEHICLE-STUB-1"
                date {
                    timestamp: 1634738043871
                }
                states {
                    type: HIT_RATIO
                    hit_ratio {
                        value: 0.28298923034940315
                    }
                }

            """
            # /!\ # : when we call the type it return a number not the name (ex: state(0).type return -> 16 not -> 'HIT_RATIO'

            # verify if a field is present or missing
            if a.type == 16:
                hit_ratio = a.hit_ratio.value
            if a.type == 1:
                lat = a.geo_position.lat
            if a.type == 1:
                lon = a.geo_position.lon
            if a.type == 4:
                speed = a.speed.value
            if a.type == 5:
                mileage = a.mileage.value
            if a.type == 9:
                if a.temperature_sensor.type == 1:
                    indoorTemperature = a.temperature_sensor.temperature.value
                if a.temperature_sensor.type == 2:
                    outdoorTemperature = a.temperature_sensor.temperature.value
                if a.temperature_sensor.type == 3:
                    engineTemperature = a.temperature_sensor.temperature.value
            if a.type == 3:
                batteryLevel = a.battery_status.level
                batteryState = a.battery_status.state
            if a.type == 2:
                doorsState = a.door_status.state
            if a.type == 13:
                vehicle_mode = a.vehicle_mode.mode
            if a.type == 6:
                robot_mode = a.robot_mode.mode
            if a.type == 21:
                driving_direction = a.driving_direction.driving_direction
            else:
                continue

            ######## fiels not find in the data test####################
            # if (a.type==?):                                          #
            # orientation = a.orientation.value                        #
            # if (a.type == ?):                                        #
            # instMileage= a.instMileage.value                         #
            # if (a.type == ?):                                        #
            # switchManual = a.switchManual.value                      #
            # if (a.type == ?):                                        #
            # next_station = a.next_station.value                      #
            # if (a.type == ?):                                        #
            # instConsumption = a.instConsumption.value                #
            ############################################################

        # insert data in dataframe from pandas librairy
        df.loc[i] = [timestamp, heure_pc, id_shuttle, hit_ratio, setupVersion, lat, lon, orientation, speed, mileage,
                     instMileage,
                     indoorTemperature, outdoorTemperature, switchManual, batteryLevel, batteryState, instConsumption,
                     doorsState, vehicle_mode, robot_mode, driving_direction]

    return df

    pass


def ecrit_dans_csv(nom_doc, valeurs):
    tt = datetime.datetime.now().date()
    repertoire_du_jour = os.path.join(r'C:\Users\ENA\Desktop\API_donnees_collectees', str(tt))
    os.chdir(repertoire_du_jour)
    with open(nom_doc, 'a') as f:  # mode a for append
        valeurs.to_csv(f, header=f.tell() == 0)


if __name__ == '__main__':
    # Script2.py executed as script
    # do something
    df = func_main_list_vehicle()
    ecrit_dans_csv('resultatsDF.csv', df)

""" NOT USE """
"""

def funcMainMonitoringVehicle():
    # token24H='8cf71e35-07c8-4844-9795-58b2f4aed088'

    # api-endpoint
    URL_monitoring = "https://lapin.stg.navya.cloud/monitoring/state/vehicle/all"
    # URL_monitoring = "https://lapin.stg.navya.cloud/monitoring/event/vehicle/AWS-SIM-101"
    authorization = 'Bearer ' + token24H
    # request GET
    r_monitoring = requests.get(URL_monitoring, headers={'Authorization': authorization})
    # decode
    dataDecode_monitoring = base64.b64decode(r_monitoring.content)
    encodingMessage_monitoring = api_pb2.TemperatureSensor.FromString(dataDecode_monitoring)

    fm = open('modeTestm.txt', "wb")
    fm.write(api_pb2.TemperatureSensor.SerializeToString(encodingMessage_monitoring))
    fm.close()
    v_monitoring = api_pb2.TemperatureSensor()
    # Read
    fm = open('modeTestm.txt', "rb")
    v_monitoring.ParseFromString(fm.read())
    fm.close()

    resultats_monitoring = open('resultatsm.txt', "a+")
    v_text = protot.MessageToString(v)
    resultats_monitoring.write(v_text)
    resultats_monitoring.close()

    print(v_monitoring)  #
    return resultats_monitoring

    if __name__ == '__main__':
        # Script2.py executed as script
        # do something
        funcMainMonitoringVehicle()



"""
