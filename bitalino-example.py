# code being tested with Python 3.7
from bitalino import BITalino
import time

# This example will collect data for 5 sec.
macAddress = "/dev/tty.BITalino-DevB"
# running_time = 5
    
batteryThreshold = 30
acqChannels = [2] # acquired channel 2 is A3 op het bord.
samplingRate = 1000
nSamples = 10
digitalOutput = [1,1]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())
    
# Start Acquisition
device.start(samplingRate, acqChannels)

while True:
    try:
        # Read samples
        print(device.read(nSamples))
        
    except KeyboardInterrupt:
        # Stop acquisition
        device.stop()
        # Close connection
        device.close()
        break