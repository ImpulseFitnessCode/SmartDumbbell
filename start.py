from IMU import IMU
from driver import Driver
from test_data import TestData

imu = IMU()

def test_model():
   driver = Driver(imu)
   driver.start() 

def create_test_data():
    td = TestData(imu)

    td.genTestData()
    td.processTestData()
    td.writeTestData()

    td = TestData(imu, 15)

    td.genTestData()
    td.processTestData()
    td.writeTestData('test_data.json')

test_model()