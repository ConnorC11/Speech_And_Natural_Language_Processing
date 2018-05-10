'''
  Myanna Harris
  9-11-16
  asgn2.py

  Normalize and check Zipf's Law on Jane Austen's novel, Emma.

  To run:
  python asgn2.py "path/to/austen-emma.txt"
'''
import sys
import re
import numpy as np
import matplotlib.pylab as plt

# normalize(filePath)
def normalize(file):
    f = open(file,'r')
    iter = re.finditer('(^|[^a-zA-Z])[a-zA-Z0-9]+([^a-zA-Z]|$)',f.read())
    f.close()
    fOut = open("list.txt","w")
    wordList = []
    for w in iter:
        s = (str(w.group(0))).strip()
        if len(s) > 0 and s != "s":
    #        print s
            fOut.write(s+"\n")
            wordList.append(s)
    fOut.close()
    return wordList

def makeDictionary(list):
    freqDict = {}
    for word in list:
        if freqDict.has_key(word):
            freqDict[word] += 1
        else:
            freqDict[word] = 1

    return freqDict

def plotZipfsLaw():
    x = np.linspace(1,100,1000)
    y = 1/x
    plt.loglog(x,y)

def plotFreq(dict):
    sortedTuples = sorted(dict.items(), key=lambda x:x[1],reverse=True)
    sortedFreq = []
    for tup in sortedTuples:
        sortedFreq.append(tup[1])
    x = np.linspace(1,len(sortedFreq)+1,len(sortedFreq))
    y = sortedFreq
    plt.loglog(x,y)

def main(argv):
    if len(argv) < 1:
        print "Need file path"
        return 0

    wordList = normalize(argv[0])
    wordDict = makeDictionary(wordList)
    plotZipfsLaw()
    plotFreq(wordDict)
    plt.title("Zipf's Law with Emma's word frequency vs rank")
    plt.xlabel("r/rank")
    plt.ylabel("(1/r)/frequency")
    plt.show()

if __name__ == '__main__':
    main(sys.argv[1:])
