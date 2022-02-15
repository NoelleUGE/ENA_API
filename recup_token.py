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

global token24H

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

def fct_recup_token():
    ##1°###### Get the token with post request #################

    url_token = 'https://lapin.stg.navya.cloud/auth/token'
    # url_token = 'https://lapin-preprod.navya.cloud/auth/token'
    params = {'username': 'projet-ena-api@univ-eiffel.fr', 'password': 'c9Vt7Ejg4ZMHHH3!'}

    token = requests.post(url_token, data=params)
    token24H = token.text
    print(token24H)

    vehicleList = api_pb2._VEHICLESTATEMESSAGE
    return token24H


if __name__ == '__main__':
    # Script2.py executed as script
    # do something
    jetonJournée = fct_recup_token()
