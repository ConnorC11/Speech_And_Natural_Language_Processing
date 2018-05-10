import sys
import re

'''
  Myanna Harris and Jasmine Jans (mharris5@zagmail.gonzaga.edu submitter)
  CPSC 475
  10-10-16
  asgn4.py

  Implementation of Soundex as a finite state transducer (FST)
  See our attached diagram for details on how we implemented
  our FST. This code follows the format of an FST to implement
  the Soundex algorithm.

  To run:
  python asgn3.py name
'''
import sys
import re

'''
the initial function that starts our FST by following stages q0-q1
this functions sets up a new encodedForm string to be built upon given
the string to be encoded.
'''
def transducer(name):
    currIdx = 0

    # q0 - create an empty string to save new encoded string in
    encodedForm = ""

    # q1 - save the first letter of the given string
    encodedForm += name[0]
    currIdx += 1

    # q1 - calls a functions that details all other possible path calls from q1
    encodedForm += q1(name, currIdx)

    return encodedForm

'''
checks conditions to follow the correct path from q1 in our FST
given the string from user input
'''
def q1(name, idx):
    # q1 -  a stage from which you can follow almost all possible paths including
    #       dropping vowels, replacing letters and adding zeros
    idx = dropLetters(name, idx)

    encodedForm = ""

    if idx > len(name) - 1:
        # q2 - there are no more letters in the string, so add 3 0s
        encodedForm += "000"
    else:
        # q3-8 - determine the new index of the given string and the encoded digit
        #        of the current letter in the given string
        encoding, idxNew = q3_8(name, idx)
        encodedForm += encoding
        idx = idxNew

        # q9 - similair to q1, another stage from which you can follow almost
        #      all possible paths including dropping vowels, replacing letters
        #      and adding zeros
        idx = dropLetters(name, idx)
        if idx > len(name) - 1:
            # q10 - there are no more letters in the string so add 2 0s
            encodedForm += "00"
        else:
            # q11-16 - determine the new index of the given string and the encoded digit
            #          of the current letter in the given string
            encoding, idxNew = q3_8(name, idx)
            encodedForm += encoding
            idx = idxNew

            # q17 - similair to q9 and q1, another stage from which you can follow
            #       almost all possible paths inclusing dropping vowels, replacing
            #       letters and adding zeros
            idx = dropLetters(name, idx)
            if idx > len(name) - 1:
                # q18 - there are no more letters in the string so add one 0
                encodedForm += "0"
            else:
                # q19-24 - replace one more letter since then we reach 4 chars
                #          (1 letter and 3 digits) in our encoded string
                encoding, idxNew = q3_8(name, idx)
                encodedForm += encoding
                idx = idxNew
                
    return encodedForm

'''
Provides options to take paths to atages q3-q8 or similairly q11-q16 and q17-q24
where specific letters are replaced with their specified encoded digit.
returns the digit replacing the letter at the given index, and the new index
of the string after dealing with the current letter.
'''
def q3_8(name, idx):
    i = idx
    if re.match('[bfpv]', name[i]) is not None:
        # q3, q11, q19 - replace any b,f,p, or v with 1
        i += 1

        #given adjacent letter with same value, only keep one digit
        while i < len(name) and re.match('[bfpv]', name[i]) is not None:
            i += 1
        return ("1", i)
    elif re.match('[cgjkqszx]', name[i]) is not None:
        # q4, q12, q20 - replace any c,g,j,k,q,s,z, or x with 2
        i += 1

        #given adjacent letter with same value, only keep one digit
        while i < len(name) and re.match('[cgjkqszx]', name[i]) is not None:
            i += 1
        return ("2", i)
    elif re.match('[dt]', name[i]) is not None:
        # q5, q13, q21 - replace any d or t with 3
        i += 1
        
        #given adjacent letter with same value, only keep one digit
        while i < len(name) and re.match('[dt]', name[i]) is not None:
            i += 1
        return ("3", i)
    elif re.match('[l]', name[i]) is not None:
        # q6, q14, q22 - replace any l with 4
        i += 1

        #given adjacent letter with same value, only keep one digit
        while i < len(name) and re.match('[l]', name[i]) is not None:
            i += 1
        return ("4", i)
    elif re.match('[mn]', name[i]) is not None:
        # q7, q15, q23 - replace any m or n with 5
        i += 1
        
        #given adjacent letter with same value, only keep one digit
        while i < len(name) and re.match('[mn]', name[i]) is not None:
            i += 1
        return ("5", i)
    elif re.match('[r]', name[i]) is not None:
        # q8, q16, q24 - replace any r with 6
        i += 1
        
        #given adjacent letter with same value, only keep one digit
        while i < len(name) and re.match('[r]', name[i]) is not None:
            i += 1
        return ("6", i)

'''
drops vowels and h and w out of the string
returns the index of the given string after
skipping over the vowels
'''
def dropLetters(name, idx):
    #q1, q2, q17 - given a vowel, remove the vowel (in our case, skip over it)
    i = idx
    while i < len(name) and (re.match('[aeiouhwy]', name[i]) is not None):
        i += 1
    return i

'''
calls transducer with the user inputted "name"
'''
def main(argv):
    if argv[0] is None or len(argv[0]) < 1:
        print("Need a name with at least one character")
    else:
        encodedForm = transducer(argv[0])
        print(encodedForm)

if __name__ == '__main__':
    main(sys.argv[1:])
