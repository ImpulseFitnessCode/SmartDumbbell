import sys, getopt

import RTIMU
import os.path
import time

SETTINGS_FILE = "IMUSettings"

class IMU():
    imu = None
    s = None
    poll_interval = 1000

    def __init__(self):
        print("Using settings file " + SETTINGS_FILE + ".ini")
        if not os.path.exists(SETTINGS_FILE + ".ini"):
          print("Settings file does not exist, will be created")

        self.s = RTIMU.Settings(SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(self.s)
        print("IMU Name: " + self.imu.IMUName())

        if (not self.imu.IMUInit()):
            print("self.IMU Init Failed")
            sys.exit(1)
        else:
            print("self.IMU Init Succeeded");

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        # self.imu.setCompassEnable(True)
        self.poll_interval = self.imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % self.poll_interval)


    def getPollingInterval(self):
        return self.poll_interval

    def getData(self):
        # print(self.imu)
        data = {}
        if self.imu.IMURead():
            data = self.imu.getIMUData()
        return data



