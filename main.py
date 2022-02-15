# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# pip install schedule
import datetime
import sys
from _ast import Raise

import schedule
import time
import main
import subprocess
import os

import mainState
import recup_token
global token24h
token24h = ""

def lancement():
    print("lancement du module de récupération du jeton")
    global token24h
    token24h = recup_token.fct_recup_token()


def recup_data_api():
    global token24h

    if len(token24h) > 1:

        print("I'm working...")
        tt = datetime.datetime.now().date()
        repertoire_du_jour = os.path.join(r'C:\Users\ENA\Desktop\API_donnees_collectees', str(tt))
        try:
            os.makedirs(repertoire_du_jour)
        except OSError:
            if not os.path.isdir(repertoire_du_jour):
                Raise
        #subprocess.call("mainState.py", shell=True)
        print(token24h)
        mainState.func_main_list_vehicle(token24h)
        #mainState.ecrit_dans_csv()


def exit():
    print('{} Now the system will exit '.format(datetime.datetime.now()))  # this works ok
    sys.exit()
    # crypte
    # envoi
    # remets vide les fichiers


#token24h = lancement()
#recup_data_api(token24h)


schedule.every().day.at('18:06').do(lancement)
print(token24h)
schedule.every().day.at('18:06').do(recup_data_api)
schedule.every(1).seconds.do(recup_data_api)
schedule.every().minutes.do(recup_data_api)
schedule.every().hour.do(recup_data_api)
schedule.every().day.at('18:07').do(exit)


while 1:
    schedule.run_pending()
    time.sleep(1)

