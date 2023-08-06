#!/bin/python
import importlib,sys
import dorianUtils.Simulators as simu
from smallpower import smallPower
from smallpower import conf
importlib.reload(smallPower)
importlib.reload(simu)
# ==============================================================================
#                           MAIN SIMULATOR
simulatorBECKHOFF = smallPower.Simulator_beckhoff()
# simulatorBECKHOFF.start()
if conf.SIMULATOR:
    try:
        print("start server")
        simulatorBECKHOFF.server.start()
        print("server Online")
        simulatorBECKHOFF.feedingLoop()
    except:
        print("could not start the server")
    finally:
        print("server Offline")
        simulatorBECKHOFF.server.stop()
else:
    print('parameter conf.SIMULATOR: not set to True. Exit.' )
