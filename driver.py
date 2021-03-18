import time

from model import Model

class Driver():
    model = None
    imu = None
    # Reads per second
    resolution = 0.1

    window = [[] for _ in range(0, 6)]
    # rep window size in seconds
    window_size = 5 / resolution

    def __init__(self, imu):
        self.imu = imu
        self.model = Model()
        print('Creating driver...')
        self.model.load_model()


    def start(self):
        while True:
            data_piece = self.get_data_piece()
            self.add_to_window(data_piece)
            self.check_model()
            time.sleep(self.resolution)

    def check_model(self):
        if len(self.window[0]) >= self.window_size:
            pred = self.model.predict(self.window)
            print(pred)

    def add_to_window(self, item):
        for i, param in enumerate(self.window):
            if len(param) >= self.window_size:
                # Shift window
                param.pop(0)

            param.append(item[i])


    def get_data_piece(self):
        p = self.imu.getPollingInterval()
        found_data = False
        while found_data == False:
            data = self.imu.getData()
            accel = data.get('accel')
            rot = data.get('fusionPose')
            if accel and rot:
                found_data = True
                return [
                    accel[0], accel[1], accel[2],
                    rot[0], rot[1], rot[2]
                ]

            time.sleep(p / 1000)


