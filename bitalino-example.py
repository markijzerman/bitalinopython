# code being tested with Python 3.7
from bitalino import BITalino
import time
import OSC


# This example will collect data for 5 sec.
macAddress = "/dev/tty.BITalino-DevB"

# Set OSC ip and port
ip = '127.0.0.1'
port = 4444
    
batteryThreshold = 30
acqChannels = [2] # acquired channel 2 is A3 op het bord.
samplingRate = 1000
nSamples = 10
digitalOutput = [1,1]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Set OSC settings
client = OSC.OSCClient()
client.connect((ip, int(port)))

# Read BITalino version
print(device.version())
    
# Start Acquisition
device.start(samplingRate, acqChannels)



while True:
    try:
        # Read samples
        fromBitalino = device.read(nSamples)
        print(fromBitalino)
        # Push to OSC
        msg = OSC.OSCMessage()
        msg.setAddress("/msg")
        msg.append(str(fromBitalino))
        client.send(msg)
        
    except KeyboardInterrupt:
        # Stop BT acquisition
        device.stop()
        # Close BT connection
        device.close()
        # Close OSC connection
        client.close()
        break