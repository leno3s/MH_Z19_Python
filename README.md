# MH\_Z19\_Python
  Simple class can be used for reading CO2 concentration from MH-Z19 sensor.

# Requirements
  * Python3.7
  * Pyserial 3.4

# Usage
  1. Instantiate the class with the device file as a constructor parameter.
  1. Call `connect()` method, then call `get()`, which will return CO2 concentration in ppm.
  1. After use, must be closed by `close()` method.

For example with `with` statement:
```python
import mh_z19
import time
import datetime

try:
    while True:
        with mh_z19.Connector("/dev/serial0") as con:
            data = con.get()
            if data.validate():
                print(str(datetime.datetime.today()) + "\t" + str(data.get()) + " ppm")
            else:
                print("Not valid.")
                continue
            time.sleep(5)
except KeyboardInterrupt:
    print("Interruption.")
```

# License
 MIT.
