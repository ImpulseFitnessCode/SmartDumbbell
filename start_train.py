from model import Model

def train():
    m = Model()

    m.create()
    m.load_data()
    m.train()
    m.test()
    m.save_model()

def load():
    m = Model()
    m.load_model()
    m.load_data()
    m.test()

# train()
load()