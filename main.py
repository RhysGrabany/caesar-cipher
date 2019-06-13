#!/usr/bin/python3

import argparse

def decrypt():
    pass

def encrypt():
    pass

def readFile(args):
    file_words = []

    with args.input as fileI:
        for line in fileI:
            for word in line.split():
                file_words.append(word)

    return file_words


def writeFile(args, out):
    with args.output as fileO:
        for word in out:
            fileO.write(word + " ")
            



# Arguments used in this program for input, output, steps, encrypt, and decrypt
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--decrypt", default=False, required=False, action="store_true", help="Decypted an input file")
ap.add_argument("-e", "--encrypt", default=False, required=False, action="store_true", help="Encrypted an input file")
ap.add_argument("-i", "--input", default=False, required=False, type=argparse.FileType('r'), dest="input", help="Input a file to be encrypted or decrypted")
ap.add_argument("-o", "--output", default="out.txt", required=False, type=argparse.FileType('w'), dest="output", help="File output, default is: out.txt")
ap.add_argument("-s", "--step", default=False, required=False, type=int, help="How many steps to the encryption desired")

arguments = ap.parse_args()

# Load some arguments into variables that need to be used now
# input, and output can be left until later
decrypt = arguments.decrypt
encrypt = arguments.encrypt
step = arguments.step

stepCheck = False
if isinstance(step, int):
    stepCheck = True

# check if encrypt and decrypt are used together
if (decrypt and encrypt):
    ap.error("Only allowed either encrypt or decrypt one at a time")
# 
if (decrypt and stepCheck):
    ap.error("Program automatically decrypts, no need for step")

print(arguments.input, arguments.output)

input_words = readFile(arguments)

print(input_words)

writeFile(arguments, input_words)




