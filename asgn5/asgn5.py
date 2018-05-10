'''
  Myanna Harris
  Jasmine Jans
  10-26-16
  asgn5.py

  N-Gram generator

  To run:
  python asgn5.py 
'''

import nltk
from nltk.corpus import brown
import random

def preparingCorpus(lists):
    newLists = [[] for i in range(0,len(lists))]

    wordIdxDict = {}
    currDictIdx = 0

    wordCountTotal = 0

    for i in range(0,len(lists)):
        newLists[i].append("<s>")
        wordCountTotal += 1
        if not wordIdxDict.has_key("<s>"):
            wordIdxDict["<s>"] = currDictIdx
            currDictIdx += 1
        
        for k in range(0, len(lists[i])):
            asciiWord = lists[i][k].encode('ascii', 'ignore')
            if not (k > len(lists[i])-3 and
                (asciiWord == '.' or asciiWord == '?'
                  or asciiWord == '!' or asciiWord == ':'
                  or asciiWord == ';' or asciiWord == "''")):
                
                newLists[i].append(asciiWord)
                wordCountTotal += 1
                if not wordIdxDict.has_key(asciiWord):
                    wordIdxDict[asciiWord] = currDictIdx
                    currDictIdx += 1
                
        newLists[i].append("</s>")
        wordCountTotal += 1
        if not wordIdxDict.has_key("</s>"):
            wordIdxDict["</s>"] = currDictIdx
            currDictIdx += 1

    return (newLists, wordIdxDict, wordCountTotal)

def makeUnigramStructure(lists, wordIdxDict, wordCountTotal):
    unigramMatrix = [0 for i in range(0, len(wordIdxDict.keys()))]

    unigramFreq = {}

    for i in range(0,len(lists)):
        for k in range(0, len(lists[i])):
            word = lists[i][k]
            wordIdx = wordIdxDict[word]
            unigramMatrix[wordIdx] += 1

            if not unigramFreq.has_key(word):
                unigramFreq[word] = 1
            else:
                unigramFreq[word] += 1

    for i in range(0,len(unigramMatrix)):
        unigramMatrix[i] /= float(wordCountTotal)
            
    return (unigramMatrix, unigramFreq)

def makeBigramStructure(lists, wordIdxDict, unigrams, unigramFreq):
    bigramMatrix = [[0 for i in range(0, len(wordIdxDict.keys()))]
                    for k in range(0, len(wordIdxDict.keys()))]

    bigramIdxDict = {}
    currDictIdx = 0

    bigramCountTotal = 0

    bigramFreq = {}

    for i in range(0,len(lists)):
        for k in range(1, len(lists[i])):
            prevWord = lists[i][k-1]
            word = lists[i][k]
            prevWordIdx = wordIdxDict[prevWord]
            wordIdx = wordIdxDict[word]
            bigramMatrix[wordIdx][prevWordIdx] += 1

            if not bigramIdxDict.has_key(prevWord +" "+ word):
                bigramIdxDict[prevWord +" "+ word] = currDictIdx
                currDictIdx += 1

            if not bigramFreq.has_key(prevWord +" "+ word):
                bigramFreq[prevWord +" "+ word] = 1
            else:
                bigramFreq[prevWord +" "+ word] += 1

    for i in range(0,len(bigramMatrix)):
        for k in range(0, len(bigramMatrix[i])):
            unigramWords = ""
            for key, value in bigramIdxDict.items():
                if value == k:
                    unigramWords = key.split()
                    break
            unigramWord = unigramWords[0]
            bigramMatrix[i][k] /= float(unigramFreq[unigramWord])
            
    return (bigramMatrix, bigramIdxDict, bigramFreq)

def makeTrigramStructure(lists, wordIdxDict, bigrams, bigramIdxDict, bigramFreq):
    trigramMatrix = [[0 for i in range(0, len(bigramIdxDict.keys()))]
                    for k in range(0, len(wordIdxDict.keys()))]

    trigramIdxDict = {}
    currDictIdx = 0

    trigramFreq = {}

    for i in range(0,len(lists)):
        for k in range(2, len(lists[i])):
            prevWords = lists[i][k-2]+ " " + lists[i][k-1]
            word = lists[i][k]
            prevWordsIdx = bigramIdxDict[prevWords]
            wordIdx = wordIdxDict[word]
            trigramMatrix[wordIdx][prevWordsIdx] += 1

            if not trigramIdxDict.has_key(prevWords +" "+ word):
                trigramIdxDict[prevWords +" "+ word] = currDictIdx
                currDictIdx += 1

            if not trigramFreq.has_key(prevWords +" "+ word):
                trigramFreq[prevWords +" "+ word] = 1
            else:
                trigramFreq[prevWords +" "+ word] += 1

    for i in range(0,len(trigramMatrix)):
        for k in range(0, len(trigramMatrix[i])):
            bigramWords = ""
            for key, value in bigramIdxDict.items():
                if value == k:
                    bigramWords = key.split()
                    break
            bigram = bigramWords[0] + " " + bigramWords[1]
            trigramMatrix[i][k] /= float(bigramFreq[bigram])
            
    return (trigramMatrix, trigramIdxDict, trigramFreq)

def makeQuadgramStructure(lists, wordIdxDict, trigrams, trigramIdxDict, trigramFreq):
    quadgramMatrix = [[0 for i in range(0, len(trigramIdxDict.keys()))]
                    for k in range(0, len(wordIdxDict.keys()))]

    for i in range(0,len(lists)):
        for k in range(3, len(lists[i])):
            prevWords = lists[i][k-3]+" " +lists[i][k-2]+" " +lists[i][k-1]
            word = lists[i][k]
            prevWordsIdx = trigramIdxDict[prevWords]
            wordIdx = wordIdxDict[word]
            quadgramMatrix[wordIdx][prevWordsIdx] += 1

    for i in range(0,len(quadgramMatrix)):
        for k in range(0, len(quadgramMatrix[i])):
            trigramWords = ""
            for key, value in trigramIdxDict.items():
                if value == k:
                    trigramWords = key.split()
                    break
            trigram = trigramWords[0] + " " + trigramWords[1] + " " + trigramWords[2]
            quadgramMatrix[i][k] /= float(trigramFreq[trigram])
            
    return quadgramMatrix

def continuousProbabilityUni(ngrams):
    continuousProbs = [0 for i in range(len(ngrams))]
    
    for i in range(len(continuousProbs)):
        if i == 0:
            continuousProbs[i] = ngrams[i]
        elif i == len(continuousProbs)-1:
            continuousProbs[i] = 1
        else:
            continuousProbs[i] = continuousProbs[i-1]+ngrams[i]

    return continuousProbs

def continuousProbability(ngrams):
    continuousProbs = [[0 for i in range(len(ngrams[0]))] for j in range(len(ngrams))]
    
    for i in range(len(continuousProbs[0])):
        for j in range(len(continuousProbs)):
            if j == 0:
                continuousProbs[j][i] = ngrams[j][i]
            elif j == len(continuousProbs)-1:
                continuousProbs[j][i] = 1
            else:
                continuousProbs[j][i] = continuousProbs[j-1][i] + ngrams[j][i]

    return continuousProbs

    
def makeUnigramSentence(unigrams, wordIdxDict):
    continuousProbs = continuousProbabilityUni(unigrams)

    sentence = ""
    word = ""
    
    while word != "<s>":
        randomNum = random.random()
        index = 0

        for i in range(0, len(unigrams)):
            if randomNum <= continuousProbs[i]:
                index = i
                break

        for key, value in wordIdxDict.items():
            if value == index:
                word = key
                break

    sentence += word

    while word != "</s>":
        randomNum = random.random()
        index = 0

        for i in range(0, len(unigrams)):
            if randomNum <= continuousProbs[i]:
                index = i
                break
        
        for key, value in wordIdxDict.items():
            if value == index and key != "<s>":
                word = key
                break
                    
        if (word != "<s>"):   
            sentence += " " + word
        else:
            word = ""
    
    return sentence

def makeBigramSentence(bigrams, wordIdxDict):
    continuousProbs = continuousProbability(bigrams)

    sentence = ""
    word1 = ""
    word2 = ""
    
    while word1 != "<s>":
        randomNum1 = random.randint(0,len(bigrams[0])-1)
        randomNum2 = random.random()
        index1 = 0
        index2 = 0

        for j in range(0, len(bigrams)):    
            if randomNum2 <= continuousProbs[j][randomNum1]:
                index1 = randomNum1
                index2 = j
                break

        for key, value in wordIdxDict.items():
            if value == index1:
                word1 = key
            if value == index2:
                word2 = key

    sentence += word1 + " " + word2

    while word2 != "</s>":
        randomNum1 = random.randint(0,len(bigrams[0])-1)
        randomNum2 = random.random()
        index1 = 0
        index2 = 0

        for j in range(0, len(bigrams)):    
            if randomNum2 <= continuousProbs[j][randomNum1]:
                index1 = randomNum1
                index2 = j
                break

        for key, value in wordIdxDict.items():
            if value == index1 and key != "<s>":
                word1 = key
            if value == index2 and key != "<s>":
                word2 = key

        if (word1 != "<s>" and word2 != "<s>" and word1 != "</s>"):   
            sentence += " " + word1 + " " + word2
        else:
            word1 = ""
            word2 = ""
    
    return sentence
    

def makeTrigramSentence(trigrams, bigramIdxDict, wordIdxDict):
    continuousProbs = continuousProbability(trigrams)

    sentence = ""
    word1 = ""
    word2 = ""
    word1b = ""
    
    while word1 != "<s>":
        randomNum1 = random.randint(0,len(trigrams[0])-1)
        randomNum2 = random.random()
        index1 = 0
        index2 = 0

        for j in range(0, len(trigrams)):    
            if randomNum2 <= continuousProbs[j][randomNum1]:
                index1 = randomNum1
                index2 = j
                break

        for key, value in wordIdxDict.items():
            if value == index2:
                word2 = key
                break
                
        for key, value in bigramIdxDict.items():
            key1, key2 = key.split()
            if value == index1:
                word1 = key1
                word1b = key2
                break

    sentence += word1 + " " + word1b + " " + word2

    while word2 != "</s>" and word1 != "</s>" and word1b != "</s>":
        randomNum1 = random.randint(0,len(trigrams[0])-1)
        randomNum2 = random.random()
        index1 = 0
        index2 = 0

        for j in range(0, len(trigrams)):    
            if randomNum2 <= continuousProbs[j][randomNum1]:
                index1 = randomNum1
                index2 = j
                break

        for key, value in bigramIdxDict.items():
            key1, key2 = key.split()
            if value == index1 and key1 != "<s>" and key2 != "<s>" and key1 != "</s>" and key2 != "</s>":
                word1 = key1
                word1b = key2
                break

        for key, value in wordIdxDict.items():
            if value == index2 and key != "<s>":
                word2 = key
                break
                
        if (word1 != "<s>" and word1b != "<s>" and word2 != "<s>"
            and word1 != "</s>" and word1b != "</s>"):   
            sentence += " " + word1 + " " + word1b + " " + word2
        else:
            word1 = ""
            word1b = ""
            word2 = ""
        
    return sentence

def makeQuadgramSentence(quadgrams, trigramIdxDict, wordIdxDict):
    continuousProbs = continuousProbability(quadgrams)

    sentence = ""
    word1 = ""
    word2 = ""
    word1b = ""
    word1c = ""
    
    while word1 != "<s>":
        randomNum1 = random.randint(0,len(quadgrams[0])-1)
        randomNum2 = random.random()
        index1 = 0
        index2 = 0

        for j in range(0, len(quadgrams)):    
            if randomNum2 <= continuousProbs[j][randomNum1]:
                index1 = randomNum1
                index2 = j
                break

        for key, value in wordIdxDict.items():
            if value == index2:
                word2 = key
                break
                
        for key, value in trigramIdxDict.items():
            key1, key2, key3 = key.split()
            if value == index1:
                word1 = key1
                word1b = key2
                word1c = key3
                break

    sentence += word1 + " " + word1b + " " + word1c + " " + word2

    while word2 != "</s>" and word1 != "</s>" and word1b != "</s>" and word1c != "</s>":
        randomNum1 = random.randint(0,len(quadgrams[0])-1)
        randomNum2 = random.random()
        index1 = 0
        index2 = 0

        for j in range(0, len(quadgrams)):    
            if randomNum2 <= continuousProbs[j][randomNum1]:
                index1 = randomNum1
                index2 = j
                break

        for key, value in trigramIdxDict.items():
            key1, key2, key3 = key.split()
            if (value == index1 and key1 != "<s>" and key2 != "<s>"
                and key3 != "<s>" and key1 != "</s>" and key2 != "</s>" and key3 != "</s>"):
                word1 = key1
                word1b = key2
                word1c = key3
                break

        for key, value in wordIdxDict.items():
            if value == index2 and key != "<s>":
                word2 = key
                break

        if (word1 != "<s>" and word1b != "<s>" and word1c != "<s>" and word2 != "<s>"
            and word1 != "</s>" and word1b != "</s>" and word1c != "</s>"):   
            sentence += " " + word1 + " " + word1b + " " + word1c + " " + word2
        else:
            word1 = ""
            word1b = ""
            word1c = ""
            word2 = ""
        
    return sentence

def main():
    news = brown.sents(categories='editorial')
    # add sentence markers to sentences for news
    # wordIdxDict =  dictionary telling the index for each word
    #   for future use in N-gram structures
    # wordCountTotal = number of total words in the corpus
    news = [news[i] for i in range(0, 30)]
    news, wordIdxDict, wordCountTotal = preparingCorpus(news)
    #print(news)

    unigrams, unigramFreq = makeUnigramStructure(news, wordIdxDict, wordCountTotal)

    bigrams, bigramIdxDict, bigramFreq = makeBigramStructure(news, wordIdxDict, unigrams, unigramFreq)

    trigrams, trigramIdxDict, trigramFreq = makeTrigramStructure(news, wordIdxDict, bigrams, bigramIdxDict, bigramFreq)
    
    quadgrams = makeQuadgramStructure(news, wordIdxDict, trigrams, trigramIdxDict, trigramFreq)

    count = 0
    while(count<5):
        print(makeUnigramSentence(unigrams, wordIdxDict))
        count+=1

    count = 0
    while(count<5):
        print(makeBigramSentence(bigrams, wordIdxDict))
        count+=1

    count = 0
    while(count<5):
        print(makeTrigramSentence(trigrams, bigramIdxDict, wordIdxDict))
        count+=1

    count = 0
    while(count<5):
        print(makeQuadgramSentence(quadgrams, trigramIdxDict, wordIdxDict))
        count+=1


if __name__ == '__main__':
    main()
