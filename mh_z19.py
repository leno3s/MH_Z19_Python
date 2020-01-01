#!/usr/bin/env python3
import serial
import logging

class Connection:

    __GET = b"\xff\x01\x86\x00\x00\x00\x00\x00\x79"
    __ZERO_CALIB = b"\xff\x01\x87\x00\x00\x00\x00\x00\x78"
    __SPAN_CALIB = b"\xff\x01\x88\x07\x00\x00\x00\x00\xA0"

    __connection = None
    __device = None

    def __init__(self, device):
        """
        Create instance.

        Parameters
        ----------
        device : string
            File path for the device(e.g. "/dev/serial0").

        Note
        ----------
        This operation does not establish a connection. Please use connect(), and close() methods.
        """
        self.__device = device

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        """
        Create connection.
        """
        self.__connection = serial.Serial(self.__device, timeout=1.0)

    def zero_calibrate(self):
        """
        Execute zero calibration.

        See also
        -------
        https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf
        """
        self.__connection.write(self.__ZERO_CALIB)

    def span_calibrate(self):
        """
        Execute span calibration.

        See also
        -------
        https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf
        """
        self.__connection.write(self.__SPAN_CALIB)

    def get(self):
        """
        Get the data from sensor.

        Returns
        -------
        Instance of Data() when executed.
        """

        self.__connection.write(self.__GET)
        result = self.__connection.read(9)
        return Data(result)

    def close(self):
        """
        Close the connection.
        """

        self.__connection.close()


class Data:

    __raw = None

    def __init__(self, output):
        self.__raw = output

    def validate(self):
        """
        Validate the value from sensor.

        Returns
        -------
        Boolean value.
        Returns true if the value is validated.
        """

        checksum = 0xff - (sum(self.__raw[1:8]) & 0xff) + 1
        if checksum == self.__raw[8]:
            return True
        return False

    def get(self):
        """
        Get the CO2 concentration in decimal[ppm].

        Returns
        -------
        concentration : int

        See also
        -------
        https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf
        """

        concentration = self.__raw[2] * 0x100 + self.__raw[3]
        return concentration

    def get_bytes(self):
        """
        Get the raw bytes from sensor.

        Returns
        -------
        data as bytes
        """

        return bytes(self.__raw)

