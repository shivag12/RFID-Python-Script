#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import random
import time

continue_reading = True

cardnotdetected = None

#Storing Last UId value
lastcarduid = None
#Storing the UId value
uid1 = None
#Recording the time of last card detected
lastimecard = None
#Card timeout period 
cardtimeout = 1.0

#Temporary description values
location = ["Indianapolis","NewYork","Bangalore","Chennai","Tirchy","Hyderabad"]

#Temporary Chemical names.
chemicalname = ["Chloromethane","Amino Acid"]

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    #print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
#print "Welcome to the MFRC522 data read example"
#print "Press Ctrl-C to stop."
countstatus = 0
ntflag = True


# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:    
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    

    # If a card is found
    #if status == MIFAREReader.MI_OK:
        #print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if(status == 2):
        countstatus = status + countstatus        

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        
        uid1 = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        
                
        if(lastcarduid != uid1):
            if(uid[0] == 134):
                # Print Para-aminobenzoic acid
                print('{ "cardID": "'+uid1+'","ChemicalName":"'+chemicalname[0]+'","Location":"B3142-Lab1"}')
            elif(uid[0] == 224):
                print('{ "cardID": "'+uid1+'","ChemicalName":"'+chemicalname[1]+'","Location":"B3142-Lab1"}')
                
        elif(time.clock()-lastimecard > cardtimeout):
            if(uid[0] == 134):
                # Print Para-aminobenzoic acid
                print('{ "cardID": "'+uid1+'","ChemicalName":"'+chemicalname[0]+'","Location":"B3142-Lab1"}')
            elif(uid[0] == 224):
                print('{ "cardID": "'+uid1+'","ChemicalName":"'+chemicalname[1]+'","Location":"B3142-Lab1"}')            
                 
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
        lastcarduid = uid1
        lastimecard = time.clock()
        countstatus = 0
        ntflag = False

    elif(countstatus > 4):
        if(lastcarduid != None and ntflag==False):
            if(lastcarduid[:3] == '134'):
                print('{ "cardID": "'+lastcarduid+'","ChemicalName":"'+chemicalname[0]+'","Location":"Out of Self"}')
                countstatus = 0
                ntflag = True
            elif(lastcarduid[:3] == '224'):
                print('{ "cardID": "'+lastcarduid+'","ChemicalName":"'+chemicalname[1]+'","Location":"Out of Self"}')
                countstatus = 0
                ntflag = True
                
            
            

