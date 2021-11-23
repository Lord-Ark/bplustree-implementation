from remove import removeTree,removeTable
from relAlg import project,select,join
from buildTree import build
from display import displayTable
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

    global selectoutputquestion1                # writing the value of select relation in the global variable
    selectoutputquestion1 = selectionRelName

    outputrel = project(selectionRelName,outputAttlist)

    global outputrelquestion1                   #  writing the value of project relation in the global variable
    outputrelquestion1 = outputrel

    displayTable(outputrel)

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

    displayTable(outputrel)
    
    return

def question3():
    # Find the address of the suppliers who supplied ‘p15’.
    
    build('Suppliers', 'sid', 2)
    build('Supply', 'pid', 2)

    selectOutputRel = select('Supply','pid','=','p15')

    joinrelName = join(selectOutputRel,'sid','Suppliers','sid')
    
    outputrel = project(joinrelName,['address'])

    displayTable(outputrel)

    return 

def question4():
    # What is the cost of ‘p20’ supplied by ‘Kiddie’?

    selectsupplyoutput = select('Supply','pid','=','p20')

    selectsuppliersoutput = select('Suppliers','sname','=','Kiddie')

    joinresult = join(selectsupplyoutput,'sid',selectsuppliersoutput,'sid')

    projectresult = project(joinresult,['cost'])

    displayTable(projectresult)

    return

def question5():

    # For each supplier who supplied products with a cost of 47 or higher, list his/her name, product name and the cost.

    selectcostsupply = select('Supply','cost','>=',47)

    joinresult = join('Suppliers','sid',selectcostsupply,'sid')

    doublejoinresult = join('Products','pid',joinresult,'pid')

    outputresult = project(doublejoinresult,['sname','pname','cost'])

    displayTable(outputresult)
    
    return

question3()