#!/usr/bin/env python

import UltraBorg
# Board #1, address 10

def main():
    address =12
    
    UB1 = UltraBorg.UltraBorg()
    UB1.i2cAddress = address
    UB1.Init()
    
    #UB1.SetServoPosition1(255)
    
    # Reading parameters (after Init)
    print(UB1.busNumber)                      # Shows which I²C bus the board is connected on
    print(UB1.foundChip)
    
    # Other functions
    UltraBorg.ScanForUltraBorg()            # Sweep the I²C bus for available boards
    UltraBorg.SetNewAddress(address)        # Configure the attached board with a new address
    #UB1.Help()

main()
