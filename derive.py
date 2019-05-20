#! /usr/bin/python3

import sys
import string

def derive():
    slen = int(sys.argv[1].strip("-l"))
    file = sys.argv[2]
    dict = {}

    f = []

    for line in open(file , "r"):
        list = line.split()
        #print("Length of list: ", len(list)) #testing to see if lines were correctly transmitted to lists
        if (len(f) == 0):
            f.append(list[0])
        values = []
        for i in range (0, len(list)):
            #print("Current thing: ", list[i])
            if(i == 0):
                if(list[i] in dict):
                    nt = list[i]
                else:
                    dict[list[i]] = []
                    nt = list[i]
                    #print("Nonterminal: ", nt)
            elif(i == 1):
                pass
                #skips the "=" in the expressions
            else:
                values.append(list[i])
                #dict[nt].append(list[i])
        dict[nt].append(values)
        #This creates a dictionary with the lhs being the keys and the
        #definitions being a list of the rules for each NT symbol

    #Test below
    #for items, value in dict.items():
        #print(items, value)
    #for items in dict:
        #print(dict[items][0][0])
    #Checks to see if they values were assigned correctly

    worklist = f
    counter = 0
    while (len(worklist)!= 0):
        y = []
        y = worklist.pop(0)
        #makes y the first sentences in worklist and removes that sentence
        #from worklist
        if (len(y) <= slen): #checks to see if the sentence fits argv
            n = 0
            for i in range(0,len(y)):
                if (y[i] not in dict):
                    n = n + 1
            #Checks to see if there are any nonterminals
            if (n == len(y)):
                for iter in range(0, len(y)):
                    if (iter == len(y)-1):
                        print(y[iter])
                    else:
                        print(y[iter], end=" ")
            #Should print out the nonterminal symbols if that is all there is
            else:
                check = 0
                for iter2 in range(0,len(y)):
                    first_time = False
                    if (y[iter2] in dict):
                        if (first_time == False):
                            check = iter2
                            first_time = True
                #Finds the first NT symbol

                for i in range(0,len(dict[y[check]])):
                    tmp = []
                    for s in range(0,len(y)):
                        tmp.append(y[s])
                    tmp.pop(check)
                    check2 = check
                    for j in range(0, len(dict[y[check]][i])):
                        tmp.insert(check2, dict[y[check]][i][j])
                        check2 = check2 + 1
                    #for g in range(0,len(tmp)):
                    #    print("Tmp list: ", tmp[g])
                    #print("Getting appended")
                    worklist.append(tmp)




                #for j in range(0,len(dict[y[check]][i])):
                    #print("Value of i: ", i)
                    #print("Value of j: ", j)
                    #print("Dict call: ", dict[y[check]][i][j])
                    #create appending conditional
                    #if(len(tmp)==1):
                    #    tmp[check] = dict[y[check]][i][j]
                    #else:
                    #    tmp.append(dict[y[check]][i][j])
                #worklist.append(tmp)




if __name__ == '__main__':
    derive()
