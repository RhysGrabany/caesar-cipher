#!/usr/bin/python3

import argparse

def decrypt():
    pass

def encrypt():
    pass

def readFile():
    pass

def writeFile():
    pass


    
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--decrypt", default=False, required=False, action="store_true", help="Decypted an input file")
ap.add_argument("-e", "--encrypt", default=False, required=False, action="store_true", help="Encrypted an input file")
ap.add_argument("-i", "--input", default=False, required=False, type=argparse.FileType('r'), help="Input a file to be encrypted or decrypted")
ap.add_argument("-s", "--step", default=False, required=False, type=int, help="How many steps to the encryption desired")

arguments = vars(ap.parse_args())

decrypt = arguments["decrypt"]
encrypt = arguments["encrypt"]
fileI = arguments["input"] 
step = arguments["step"]

stepCheck = False
if isinstance(step, int):
    stepCheck = True


if (decrypt and encrypt):
    ap.error("Only allowed either encrypt or decrypt one at a time")
if (decrypt and stepCheck):
    ap.error("Program automatically decrypts, no need for step")





