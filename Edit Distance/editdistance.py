#!/usr/bin/python

class EditDistance():

    def __init__(self):
        """
        Do not change this
        """

    def calculateLevenshteinDistance(self, str1, str2):
        print(str1+" LD "+str2)
        cols = len(str2)
        rows = len(str1)
        arr = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            arr[i][0] = i
        for i in range(cols):
            arr[0][i] = i
        cost = 0
        for i in range(1, rows):
            for j in range(1, cols):
                if(str2[j - 1] == str1[i - 1]):
                    cost = 0
                else:
                    cost = 1
                arr[i][j] = (
                    min({arr[i][j - 1] + 1, arr[i - 1][j] + 1, arr[i - 1][j - 1] + cost}))
        return(arr[rows - 1][cols - 1])

    def calculateOSADistance(self, str1, str2):
        print(str1+" OSA "+str2)
        cols = len(str2)+1
        rows = len(str1)+1
        arr = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            arr[i][0] = i
        for i in range(cols):
            arr[0][i] = i
        for i in range(1, rows):
            for j in range(1, cols):
                if(str1[i - 1] == str2[j - 1]):
                    cost = 0
                else:
                    cost = 1
                arr[i][j] = (
                    min({arr[i][j - 1] + 1, arr[i - 1][j] + 1, arr[i - 1][j - 1] + cost}))
                if i > 1 and j > 1 and str1[i-1] == str2[j - 2] and str1[i - 2] == str2[j-1]:
                    arr[i][j] = (min({arr[i][j], arr[i - 2][j - 2]+1}))
        return(arr[rows - 1][cols - 1])

    def calculateDLDistance(self, str1, str2):
        print(str1+" DL "+str2)
        from collections import defaultdict
        cols = len(str2) +1
        rows = len(str1) +1
        alphabet = defaultdict(int)
        for i in range(len(str1)):
            alphabet[str1[i]]
        for i in range(len(str2)):
            alphabet[str2[i]]
        count=0
        for i in alphabet:
            alphabet[i]=count
            count+=1
        arr = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            arr[i][0] = i
        for i in range(cols):
            arr[0][i] = i
        dist1 = []
        dist2 = 0
        for i in range(len(alphabet)):
            dist1.append(0)

        for i in range(1, rows):
            dist2 = 0
            for j in range(1, cols):
                k = dist1[alphabet[str2[j - 1]]]
                l = dist2
                if(str2[j - 1] == str1[i - 1]):
                    cost = 0
                    dist2 = j
                else:
                    cost = 1
                arr[i][j] = (min({(arr[i][j - 1]) + 1, (arr[i - 1][j]) + 1, (arr[i - 1]
                                                                             [j - 1]) + cost, (((arr[k - 1][l - 1]) + (i - k - 1) + 1 + (j - l - 1)))}))
            dist1[alphabet[str1[i - 1]]] = i
        return arr[rows - 1][cols - 1]
