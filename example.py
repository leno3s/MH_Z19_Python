#!/usr/bin/env python3
import mh_z19
import time
import datetime

try:
    while True:
        with mh_z19.Connection("/dev/serial0") as con:
            data = con.get()
            if data.validate():
                print(str(datetime.datetime.today()) + "\t" + str(data.get()) + " ppm")
            else:
                print("Not valid.")
                continue
            time.sleep(5)
except KeyboardInterrupt:
    print("Interruption.")
