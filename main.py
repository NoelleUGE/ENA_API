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



def job():
    print("I'm working...")
    tt = datetime.datetime.now().date()
    repertoire_du_jour = os.path.join(r'C:\Users\ENA\Desktop\API_donnees_collectees', str(tt))
    try:
        os.makedirs(repertoire_du_jour)
    except OSError:
        if not os.path.isdir(repertoire_du_jour):
            Raise
    subprocess.call("mainState.py", shell=True)


def exit():
    print('{} Now the system will exit '.format(datetime.datetime.now()))  # this works ok
    sys.exit()
    # crypte
    # envoi
    # remets vide les fichiers


schedule.every().day.at('07:00').do(job)
schedule.every(1).seconds.do(job)
schedule.every().minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at('19:00').do(exit)

while 1:
    schedule.run_pending()
    time.sleep(1)
