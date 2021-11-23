from remove import removeTree,removeTable
from relAlg import project,select,join
from buildTree import build
import json
import os

outputrelquestion1 = 'Projection-sname-Select-Suppliers-sid'
selectoutputquestion1 = 'Select-Suppliers-sid'

def read(path):
    try:
        f = open(path)
        return json.load(f)
    except:
        return

def appendInQueryResult(resultexplanation, results):
    page = "../queryOutput/queryResult.txt"
    with open(page, 'a') as f:
        f.write(resultexplanation)
        f.write('\n')
        json.dump(results, f)
        f.write("\n\n\n")
        f.write("------------------------------------------------------------")
        f.write("\n")

def main():
    funcName = input(
        "enter the function(number) you want to call: \n 1. Project \n 2. Select \n 3. Join \n  Enter Number: ")

    if funcName == '1':
        relName = input("Enter relation name: ")
        attList = input("Enter attribute name: ")
        project(relName, attList)

    elif funcName == '2':
        relName2 = input("Enter relation name: ")
        attName = input("Enter attribute name: ")
        opVal = input("Enter operator value: ")
        val = input("Enter value: ")
        select(relName2, attName, opVal, val)

    elif funcName == '3':

        rel1 = input("Enter relation name1: ")
        att1 = input("Enter attribute name1: ")
        rel2 = input("Enter relation name2: ")
        att2 = input("Enter attribute name2: ")
        join(rel1, att1, rel2, att2)

def question1():
    # Find the name for the supplier ‘s23’ when a B+_tree exists on Suppliers.sid

    build('Suppliers', 'sid', 2)

    supplierval = 's23'
    relation = 'Suppliers'
    outputAttlist = ['sname']
    
    selectionRelName = select(relation, 'sid','=',supplierval)

    outputrel = project(selectionRelName,outputAttlist)

    global outputrelquestion1
    outputrelquestion1 = outputrel
    pagelink = "../data/"+outputrel+"/pageLink.txt"
    pageArray = read(pagelink)
    
    results=[]
    for pages in pageArray:
        pageitem = read("../data/"+outputrel+"/"+pages)
        results.append(pageitem)

    resultExplanation = 'Query result of => The name for the supplier where sid is "s23" with B+tree \n'
    appendInQueryResult(resultExplanation,results)

    return

def question2():
    # Find the name for the supplier ‘s23’ when a B+_tree does not exists 

    removeTree('Suppliers','sid')

    if(os.path.isdir('../data/'+outputrelquestion1)):
        removeTable(outputrelquestion1)
    if(os.path.isdir('../data/'+selectoutputquestion1)):
        removeTable(selectoutputquestion1)

    supplierval = 's23'
    relation = 'Suppliers'
    outputAttlist = ['sname']
    
    selectionRelName = select(relation, 'sid','=',supplierval)

    outputrel = project(selectionRelName,outputAttlist)

    pagelink = "../data/"+outputrel+"/pageLink.txt"
    pageArray = read(pagelink)
    
    results=[]
    for pages in pageArray:
        pageitem = read("../data/"+outputrel+"/"+pages)
        results.append(pageitem)

    resultExplanation = 'Query result of => The name for the supplier where sid is "s23" without B+tree \n'
    appendInQueryResult(resultExplanation,results)
    
    return

# question2()