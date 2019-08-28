#!/usr/bin/env python3
import mh_z19

with mh_z19.MH_Z19('/dev/serial0', timeout=1.0) as con:
    con.zero_calibrate()
