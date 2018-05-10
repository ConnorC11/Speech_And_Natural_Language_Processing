'''
  Myanna Harris
  Jasmine Jans
 10-10-16
  asgn4.py

  Implementation of Soundex finite state transducer

  To run:
  python asgn3.py name
'''
import sys
import re

def transducer(name):
    currIdx = 0

    # q0
    encodedForm = ""

    # q1
    encodedForm += name[0]
    currIdx += 1

    # q1
    encodedForm += q1(name, currIdx)

    return encodedForm

def q1(name, idx):
    # q1
    idx = dropLetters(name, idx)

    encodedForm = ""
    
    if idx > len(name) - 1:
        # q2
        encodedForm += "000"
    else:
        # q3-8
        encoding, idxNew = q3_8(name, idx)
        encodedForm += encoding
        idx = idxNew

        # q9
        idx = dropLetters(name, idx)
        if idx > len(name) - 1:
            # q10
            encodedForm += "00"
        else:
            # q11-16
            encoding, idxNew = q3_8(name, idx)
            encodedForm += encoding
            idx = idxNew

            # q17
            idx = dropLetters(name, idx)
            if idx > len(name) - 1:
                # q18
                encodedForm += "0"
            else:
                # q19-24
                encoding, idxNew = q3_8(name, idx)
                encodedForm += encoding
                idx = idxNew
    return encodedForm
        
def q3_8(name, idx):
    i = idx
    if re.match('[bfpv]', name[i]) is not None:
        # q3
        i += 1
        while i < len(name) and re.match('[bfpv]', name[i]) is not None:
            i += 1
        return ("1", i)
    elif re.match('[cgjkqszx]', name[i]) is not None:
        # q4
        i += 1
        while i < len(name) and re.match('[cgjkqszx]', name[i]) is not None:
            i += 1
        return ("2", i)
    elif re.match('[dt]', name[i]) is not None:
        # q5
        i += 1
        while i < len(name) and re.match('[dt]', name[i]) is not None:
            i += 1
        return ("3", i)
    elif re.match('[l]', name[i]) is not None:
        # q6
        i += 1
        while i < len(name) and re.match('[l]', name[i]) is not None:
            i += 1
        return ("4", i)
    elif re.match('[mn]', name[i]) is not None:
        # q7
        i += 1
        while i < len(name) and re.match('[mn]', name[i]) is not None:
            i += 1
        return ("5", i)
    elif re.match('[r]', name[i]) is not None:
        # q8
        i += 1
        while i < len(name) and re.match('[r]', name[i]) is not None:
            i += 1
        return ("6", i)

def dropLetters(name, idx):
    i = idx
    while i < len(name) and (re.match('[aeiouhwy]', name[i]) is not None):
        i += 1
    return i

def main(argv):
    if argv[0] is None or len(argv[0]) < 1:
        print("Need a name with at least one character")
    else:
        encodedForm = transducer(argv[0])
        print(encodedForm)

if __name__ == '__main__':
    main(sys.argv[1:])
