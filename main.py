#!/usr/bin/python3

import argparse
import enchant
import string

def decryption(args):
    input_list = readFile(args)
    info = longest(input_list)[0]

    # All letters in the Eng alphabet
    letters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]
    freq_letters = "etaoinshrdlcumwfgypbvkjxqz"

    dictionaryUK = enchant.Dict("en_GB")
    dictionaryUS = enchant.Dict("en_US")


    for word in input_list:
        word_test = word.translate(word.maketrans("","", string.punctuation))
        if dictionaryUK.check(word_test) or dictionaryUS.check(word_test):
            encrypted = False
            continue
        else:
            encrypted = True
            break
    
    if not encrypted:
        writeFile(args, input_list)
        return

    decrypted = []

    stripped = info.translate(info.maketrans("","", string.punctuation))
    common = mostCommon(stripped)[0]

    freq_lett_in = 0
    encrypted = True
    while encrypted:

        if freq_lett_in >= len(freq_letters):
            break
        
        print(common)

        distance = index(letters[0], freq_letters[freq_lett_in]) - index(letters[0], common)
        print(distance)

        for word in input_list:
            decrypted_word = ""
            for letter in word:

                # Check if letter is Captial
                if ord(letter) > 64 and ord(letter) < 91:
                    # Make an index out of the decimal of the letter
                    alphabet = letters[0]
                    punctuation = False
                # Check if letter is lowercase
                elif ord(letter) > 96 and ord(letter) < 123:
                    alphabet = letters[1]
                    punctuation = False
                else:
                    decrypted_word += letter
                    punctuation = True
                    

                if not punctuation:
                    temp = index(letters[1], letter)

                    if (temp + distance) > (len(alphabet)-1):
                        remainder = (temp + distance) - len(alphabet)
                        decrypted_word += alphabet[remainder]
                    else:
                        decrypted_word += alphabet[temp+distance]
                else:
                    continue
            
            decrypted.append(decrypted_word)
        
        print(decrypted)
        
        encrypted = False
        for word in decrypted:
            word_test = word.translate(word.maketrans("","", string.punctuation))
            if dictionaryUK.check(word_test) or dictionaryUS.check(word_test):
                continue
            else:
                encrypted = True
                freq_lett_in += 1
                decrypted = []
                break


    if not encrypted:
        print("Decrypted")
        writeFile(args, decrypted)
    else:
        print("Can't be decrypted at this time")


# Method for encrypting the input file based on steps provided
def encryption(args, step):
    # Loading the input filr into list
    input_list = readFile(args)

    # All letters in the Eng alphabet
    letters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]
    
    # Encypted list before writing to file
    encrypted = []

    for word in input_list:
        encrypted_word = []
        
        for letter in word:

            # Check if letter is Captial
            if ord(letter) > 64 and ord(letter) < 91:
                
                # Make an index out of the decimal of the letter
                temp = ord(letter)-65
                alphabet = letters[0]
                punctuation = False

            # Check if letter is lowercase
            elif ord(letter) > 96 and ord(letter) < 123:
                temp = ord(letter)-97
                alphabet = letters[1]
                punctuation = False
            
            else:
                encrypted_word.append(letter)
                print(letter)
                punctuation = True
                

            if not punctuation:
                # Length check out-of-bound
                if ((temp + step) > (len(alphabet))-1) or ((temp + step) < 0):
                    
                    # Fixes out-of-bound indexes
                    remainder = int((temp + step) % len(alphabet))                    
                    encrypted_word.append(alphabet[remainder])
                else:
                    encrypted_word.append(alphabet[temp+step])
            else:
                continue
            
        # Add words to the encrypted list
        encrypted.append(encrypted_word)

    # Write to file
    writeFile(args, encrypted)

# Reads the input file and stores data in file_words and returns the list
def readFile(args):
    file_words = []

    with args.input as fileI:
        for line in fileI:
            for word in line.split():
                file_words.append(word)

    return file_words

# Writes input to file without the commas and brackets
def writeFile(args, out):
    
    with args.output as fileO:
        for word in out:
            for letter in word:
                print(word)
                fileO.write(" ".join(map(str, letter)))
            fileO.write(" ")

# Used to find the longest word to make decryption easier
def longest(in_list):

    size = 0

    for word in in_list:
        if len(word) > size:
            size = len(word)
            focus = word
        else:
            continue
        
    return focus, size


# Method to find the most common letter for frequency analysis
def mostCommon(in_word):

    end_letter = False
    ind = 0
    most_freq = 0
    comm_letter = 'a'

    while not end_letter:

        letter_focus = in_word[ind]
        freq = 0

        for letter in in_word:
            if letter is letter_focus:
                freq += 1
            else:
                continue
        
        if freq > most_freq:
            most_freq = freq
            comm_letter = letter_focus

        ind += 1
    
        if ind >= len(in_word):
            end_letter = True
        else:
            continue

    return comm_letter, most_freq

def index(word, letter):

    lowered_word = word.lower()
    lowered_letter = letter.lower()

    for i in range(0, len(lowered_word)):
        if lowered_word[i] == lowered_letter:
            return i
        else: 
            continue

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
elif (not decrypt and not encrypt):
    ap.error("Either encrypt or decrypt must be used")
# 
if (decrypt and not stepCheck):
    ap.error("Program automatically decrypts, no need for step")

encryption(arguments, step) if encrypt else decryption(arguments)

