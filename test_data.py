import json
import time

class TestData():
    imu = None
    test_data = []
    # Seconds
    time_frame = 30
    # Reads per second
    resolution = 0.1
    rep_interval = 5
    rep_length = 2.5

    processed_data = []
    data_size = 0
    # rep window size in seconds
    window_size = 5

    def __init__(self, imu, time_frame = None):
        self.imu = imu
        self.time_frame = time_frame if time_frame else self.time_frame
        self.data_size = (int)(self.time_frame / self.resolution)


    def genTestData(self):
        rep_started = False
        rep_start_time = 0
        rep_interval = (int)(self.rep_interval / self.resolution)
        rep_length = (int)(self.rep_length / self.resolution)

        for i in range(0, self.data_size):
            if rep_started and i % 10 == 0:
                print('%d / 10' % ((int)(i / 10) - (int)(rep_start_time / 10)))
            if i != 0 and i % rep_interval == 0:
                print('Start Rep')
                rep_started = True
                rep_start_time = i
            if rep_started and rep_start_time + rep_length < i:
                print('Stop Rep')
                rep_started = False

            data_piece = self.getDataPiece()
            data_piece['is_rep'] = int(rep_started)
            self.test_data.append(data_piece)

            time.sleep(self.resolution)


    def getDataPiece(self):
        p = self.imu.getPollingInterval()
        found_data = False
        while found_data == False:
            data = self.imu.getData()
            accel = data.get('accel')
            rot = data.get('fusionPose')
            if accel and rot:
                found_data = True
                # print("Accel - x:%f y:%f z:%f" % (accel[0], accel[1], accel[2]))
                # print("Rot - x:%f y:%f z:%f" % (rot[0], rot[1], rot[2]))
                return {
                    'accel': {'x': accel[0], 'y': accel[1], 'z': accel[2]},
                    'rot': {'x': rot[0], 'y': rot[1], 'z': rot[2]},
                }

            time.sleep(p / 1000)


    def processTestData(self):
        print('Post processing data...')
        t1 = time.clock()
        buffer_size = (int)(self.window_size / self.resolution)
        for i in range(buffer_size, self.data_size):
            window = self.test_data[i - buffer_size:i]
            expected = False
            rep_started = False
            for i, reading in enumerate(window[:-1]):
                prev = window[i]['is_rep']
                next = window[i+1]['is_rep']
                if prev == 0 and next == 1:
                    rep_started = True
                if rep_started and prev == 1 and next == 0:
                    expected = True

            processed_window = {
                'expected': int(expected),
                'ax': [read['accel']['x'] for read in window],
                'ay': [read['accel']['y'] for read in window],
                'az': [read['accel']['z'] for read in window],
                'rx': [read['rot']['x'] for read in window],
                'ry': [read['rot']['y'] for read in window],
                'rz': [read['rot']['z'] for read in window],
            }
            self.processed_data.append(processed_window)

        print(self.processed_data[10])
        print(len(self.processed_data))
        print('Processing took: ' + str(time.clock() - t1) + ' Seconds')


    def writeTestData(self, filename='train.json'):
        with open(filename, 'w') as file:
            json.dump(self.processed_data, file)
        print('Data written to train.json')



