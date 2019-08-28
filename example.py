#!/usr/bin/env python3
import mh_z19
import time
import datetime

try:
    while True:
        with mh_z19.MH_Z19("/dev/serial0") as con:
            co2 = con.get()
            print(str(datetime.datetime.today()) + "\t" + str(co2) + " ppm")
            time.sleep(5)
except KeyboardInterrupt:
    print("Interruption.")
