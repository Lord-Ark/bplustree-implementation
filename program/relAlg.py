import json
import os
from buildTree import findInTree

def write(text, page):
    with open(page, 'w') as f:
        json.dump(text, f)

def read(path):
    f = open(path)
    return json.load(f)


def findLocationOfAtrrInTupple(rel, att):
    schema = read("../data/schemas.txt")
    for item in schema:
        if (item[0] == str.capitalize(rel) and item[1] == att):
            return item[3]


def check_if_use_B_tree(rel, att, val):
    # write a function to check if using B+ tree or
    leafNodeReturn = findInTree(rel, att, val)
    leafNode = leafNodeReturn['page']
    if(leafNode == ''):
        return False
    else:
        return True


def select(rel, att, op, val):
    array: list = []
    pos = findLocationOfAtrrInTupple(rel, att)
    cost = 0

    # check for the invalid arguments here using function

    if(check_if_use_B_tree(rel, att, val)):
        print("With B+_tree, the cost of searching "+att+" " +
              op+" "+val+" on "+rel + " is " + cost+"  pages")
        return
    else:
        pagelink = "../data/"+rel+"/pageLink.txt"
        pageArray = read(pagelink)
        for i in range(len(pageArray)):
            pagedata = read("../data/"+rel+"/"+pageArray[i])
            cost = cost + 1
            for j in range(len(pagedata)):
                Tuples = pagedata[j]
                valueforcom = Tuples[pos]
                if(op == '='):
                    if(valueforcom == val):
                        array.append(Tuples)
                elif(op == '>='):
                    if(valueforcom >= val):
                        array.append(Tuples)
                elif(op == '<='):
                    if(valueforcom <= val):
                        array.append(Tuples)
                elif (op == '<'):
                    if (valueforcom < val):
                        array.append(Tuples)
                elif (op == '>'):
                    if (valueforcom > val):
                        array.append(Tuples)

        for item in array:
            print(item)
        print("Without B+_tree the cost of searching '" + att +
              " " + op+" "+val+"' on "+rel+" is "+str(cost)+" pages")

        return


#
def project(rel, attList):
    posarray: list = []
    for item in attList:
        posarray.append(findLocationOfAtrrInTupple(rel, item))
    path = "../data/"+rel+"/tmp"
    cost = 0
    if(len(posarray) == len(attList)):
        os.mkdir(path)
    else:
        return;
    pagelink = "../data/"+rel+"/pageLink.txt"
    pageArray = read(pagelink)
    tempfiledata = []
    for i in range(len(pageArray)):
        pagedata = read("../data/"+rel+"/"+pageArray[i])
        cost = cost + 1
        for j in range(len(pagedata)):
            Tuples = pagedata[j]
            valuefortemp =[]
            for k in range(len(posarray)):
                valuefortemp.append(Tuples[posarray[k]])
            tempfiledata.append(valuefortemp)
    
    tempall=[]
    for x in range(0, len(tempfiledata), 2):
        
        pagepool = read("../data/pagePool.txt")
        lpage = pagepool.pop()
        write(pagepool,"../data/pagePool.txt")
        cost += 1
        tempFile=[]
        tempFile.append(tempfiledata[x])
        if(x+1 <= len(tempfiledata)):
            tempFile.append(tempfiledata[x+1])
        write(tempFile,"../data/"+rel+"/tmp/"+lpage)
        tempall.append(tempFile)

    for item in tempall:
        print(item)

    for item in tempall:
        for 

    print(' cost->  '+str(cost) )

    return;


def join(rel1, att1, rel2, att2):
    print("rel1 is" + rel1)
    print("att1 is" + att1)
    print("rel2 is" + rel2)
    print("att2" + att2)



# select("Supply", 'pid', '=', 'p23')
project("Products",["pid","pname"])
#output > array[['p03','drill','black'],['p05','drill','green']]
# select("Products", "pid", "=", "p05")
#output > array [['p05','drill','green']]
