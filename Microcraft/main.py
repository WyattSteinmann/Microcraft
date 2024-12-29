from ursina import *
from socks_engine import *

app = Ursina()

eng = Engine()
eng.start()

def update():
    eng.update_engine()
def input(key):
    inputClass.input_engine(key, eng.player)

app.run()