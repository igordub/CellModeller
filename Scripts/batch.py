import os
import sys
import subprocess
import string
import shutil

from CellModeller.Simulator import Simulator

max_cells = 50000
cell_buffer = 256

def simulate(modfilename, platform, device, steps=1000):
    (path,name) = os.path.split(modfilename)
    modname = str(name).split('.')[0]
    sys.path.append(path)
    sim = Simulator(modname, 0.025, clPlatformNum=platform, clDeviceNum=device, saveOutput=True)
    # while len(sim.cellStates) < max_cells-cell_buffer:
    while (sim.stepNum <= steps) and (len(sim.cellStates) < max_cells-cell_buffer):
        sim.step()

def main():
    # Get module name to load
    if len(sys.argv)<2:
        print("Please specify a model (.py) file")
        exit(0)
    else:
        moduleName = sys.argv[1]

    # Get OpenCL platform/device numbers
    if len(sys.argv)<3:
        # User input of OpenCL setup
        import pyopencl as cl
        # Platform
        platforms = cl.get_platforms()
        print("Select OpenCL platform:")
        for i in range(len(platforms)):
            print(('press '+str(i)+' for '+str(platforms[i])))
        platnum = int(eval(input('Platform Number: ')))

        # Device
        devices = platforms[platnum].get_devices()
        print("Select OpenCL device:")
        for i in range(len(devices)):
            print(('press '+str(i)+' for '+str(devices[i])))
        devnum = int(eval(input('Device Number: ')))
    else:
        platnum = int(sys.argv[2])
        devnum = int(sys.argv[3])
    
    # Check number of steps for simulation 
    if len(sys.argv)<4:
        # Simualte indefinitely
        steps = 1000000
    else:
        steps = int(sys.argv[4])

    # Set up complete, now run the simulation
    simulate(moduleName, platnum, devnum,steps=steps)

# Make sure we are running as a script
if __name__ == "__main__": 
    main()
