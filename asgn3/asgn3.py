'''
  Myanna Harris
  Jasmine Jans
  9-23-16
  asgn3.py

  Find minimum edit distance and alignment

  To run:
  python asgn3.py word1 word2
'''
import sys

def minEditDistance(str1, str2):
    if str1 is None or str2 is None:
        return "strings can't be None"
    n = len(str1)
    m = len(str2)
    if n < 1:
        return m
    if m < 1:
        return n

    # create initialized empty matrices (list of lists)
    distance = [[0 for i in range(0,m+1)]for k in range(0,n+1)]
    ptr = [[[" " for j in range(0,3)] for i in range(0,m+1)]for k in range(0,n+1)]

    # Initialization:
    # the zeroth row and col is the distance from the empty string
    distance[0][0] = 0
    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + 1
        ptr[i][0][0] = "U"
    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + 1
        ptr[0][j][2] = "L"

    # Recurrence relation
    for i in range(1,n+1):
        for j in range(1,m+1):
            sub = 2
            if str1[i-1] == str2[j-1]:
                sub = 0
            delete = distance[i-1][j]+1
            substitute = distance[i-1][j-1]+sub
            insert = distance[i][j-1]+1
            distance[i][j] = min(delete,
                                 substitute,
                                 insert)
            
            # U = UP - Deletion
            # D = DIAG - Substitution
            # L = LEFT - Insertion
            minDist = distance[i][j]
            if minDist == delete:
                ptr[i][j][0] = "U"
            if minDist == substitute:
                ptr[i][j][1] = "D"
            if minDist == insert:
                ptr[i][j][2] = "L"

    # Termination
    return distance, ptr

# N = nothing
# I = insert
# D = delete
# S = substitution
def getAlignment(table, ptr, i, j, s, str1, str2):
    if i == 0 and j == 0:
        return s

    sTemp = s
    if ptr[i][j][1] == "D":
        if i != 0 and j != 0 and str1[i-1] == str2[j-1]:
            sTemp = "N" + s
        else:
            sTemp = "S" + s

        return getAlignment(table, ptr, i-1, j-1, sTemp, str1, str2)
    else:
        if ptr[i][j][0] == "U":
            if ptr[i][j][2] == "L" and table[i][j-1] <= table[i-1][j]:
                sTemp = "I" + s
                return getAlignment(table, ptr, i, j-1, sTemp, str1, str2)
            else:
                sTemp = "D" + s
                return getAlignment(table, ptr, i-1, j, sTemp, str1, str2)
        elif ptr[i][j][2] == "L":
            sTemp = "I" + s
            return getAlignment(table, ptr, i, j-1, sTemp, str1, str2)

def printAlignmentStrings(alignmentStr, str1, str2):
    aStr = ""
    out = ""
    i = 0
    for s in alignmentStr:
        if s != "N":
            aStr = aStr + s + " "
        else:
            aStr = aStr + "  "
        if s == "I":
            out = out + "* "
        else:
            out = out + str1[i] + " "
            i += 1
    print aStr
    print out

    out = ""
    i = 0
    for s in alignmentStr:
        out = out + "| "
    print out

    out = ""
    i = 0
    for s in alignmentStr:
        if s == "D":
            out = out + "* "
        else:
            out = out + str2[i] + " "
            i += 1
    print out

def printAlignment(table, ptr, str1, str2):
    print "Alignment: "
    alignmentStr = ""
    alignmentStr = getAlignment(table, ptr, len(str1), len(str2), alignmentStr, str1, str2)
    print ""
    printAlignmentStrings(alignmentStr, str1, str2)

def main(argv):
    if len(argv) < 2:
        print "Need two words"
        return 0
    
    dist, ptr = minEditDistance(argv[0], argv[1])
    print ""
    print "Minimum edit distance: " + str(dist[len(argv[0])][len(argv[1])])
    print ""
    for row in dist:
        print row
    print ""
    printAlignment(dist, ptr, argv[0], argv[1])
    print ""
    for row2 in ptr:
        print row2

if __name__ == '__main__':
    main(sys.argv[1:])
