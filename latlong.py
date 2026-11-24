from machine import Pin, I2C, UART
import time

GPS = UART(1,
           baudrate = 9600,
           tx=machine.Pin(8),
           rx=machine.Pin(9)
)

myNMEA = ""
GNGGA = ""  
GNGSA = ""
GNGSV = ""
GNRMC = ""
GNVTG = ""

while not GPS.any():
    pass

# Reading old data left in UART
while GPS.any():
    junk = GPS.read() # Loop ends once GPS.read() is empty (new line)
    
try:
    while True:
        if GPS.any():
            myChar = GPS.read(1).decode('utf-8')
            myNMEA = myNMEA + myChar
            if myChar == '\n':
                # --- GNGGA --- #
                if myNMEA[1:6] == "GNGGA":
                    GNGGA = myNMEA
                    GNGGAarray = GNGGA.split(',')
                    if int(GNGGAarray[6]) != 0:
                        latRaw = GNGGAarray[2]
                        lonRaw = GNGGAarray[4]
                        numSat = int(GNGGAarray[7])
                        latDD  = int(latRaw[0:2]) + float(latRaw[2:])/60
                        lonDD  = int(lonRaw[0:3]) + float(lonRaw[3:])/60
                        if GNGGAarray[3] == 'S':
                            latDD = -latDD
                        if GNGGAarray[5] == 'W':
                            lonDD = -lonDD
                        print("LAT, LON, numSat ", latDD, lonDD, numSat)

                # --- GNGSA --- #
                if myNMEA[1:6] == "GNGSA":
                    GNGSA = myNMEA
                    GNGSAarray = GNGSA.split(',')

                # --- GNGSV --- #
                if myNMEA[1:6] == "GNGSV":
                    GNGSV = myNMEA
                    GNGSVarray = GNGSV.split(',')
                    if GNGGA != "":
                        if int(GNNGGA[6]) == 0:
                            print("Acquiring Fix: ", GNGSVarray[3], "Satellites in view")

                # --- GNRMC --- #
                if myNMEA[1:6] == "GNRMC":
                    GNRMC = myNMEA
                    GNRMCarray = GNRMC.split(',')
                    knots = float(GNRMCarray[7])
                    heading = float(GNRMCarray[8])
                    print(knots, "Knots at a heading of: ", heading)

                # --- GNVTG --- #
                if myNMEA[1:6] == "GNVTG":
                    GNVTG = myNMEA
                    GNVTGarray = GNVTG.split(',')

                myNMEA = ""

except KeyboardInterrupt:
    print("\n Program Interrupted!")

finally:
    print("\n . . . Cleaning up UART")
    GPS.deinit()
    print("Cleanly Exited UART")
