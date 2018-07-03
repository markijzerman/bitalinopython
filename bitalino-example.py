# code being tested with Python 3.7
from bitalino import BITalino
import time
import OSC #SO to Machiel yo
import math


# This example will collect data for 5 sec.
macAddress = "/dev/tty.BITalino-DevB"

# Set OSC ip and port
ip = '127.0.0.1'
port = 4444
    
batteryThreshold = 30
acqChannels = [0, 1, 2, 3, 4] # get A1, A2, A3, A4, A5
samplingRate = 100 # only 100 or 1000?
nSamples = 1
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
        print(fromBitalino[0])
        # implement transfer function from http://bitalino.com/datasheets/REVOLUTION_EDA_Sensor_Datasheet.pdf
        fromBitalino = device.read(nSamples)
        ADC_EDA = fromBitalino[0][6]
        EDA_uS = ((ADC_EDA / 2**6) * 3.3) / 0.132
        # print(EDA_uS)

        ADC_ECG = fromBitalino[0][5]
        ECG = (((ADC_ECG / 2**6) * 3.3) / 1100) * 1000
        # print(ECG)

        # Push EDA to OSC
        msg = OSC.OSCMessage()
        msg.setAddress("/a3")
        msg.append(EDA_uS)
        client.send(msg)

        # Push ECG to OSC
        msg = OSC.OSCMessage()
        msg.setAddress("/a2")
        msg.append(ECG)
        client.send(msg)
        
    except KeyboardInterrupt:
        # Stop BT acquisition
        device.stop()
        # Close BT connection
        device.close()
        # Close OSC connection
        client.close()
        break