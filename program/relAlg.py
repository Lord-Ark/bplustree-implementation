

def load_data_from_pageLink():
    file_Products=open("../data/Products/pageLink.txt","r")
    file_Suppliers = open("../data/Suppliers/pageLink.txt", "r")
    file_Supply = open("../data/Supply/pageLink.txt", "r")
    print(file_Products.read())
    print(file_Suppliers.read())
    print(file_Supply.read())





def select(rel, att, op, val):

    print("The Input Information is"+"Rel"+rel+' att- '+att+' op->'+op+' val->'+val)

    """  < ,  <= , =,  > ,  >=                   op1 to op 5’"""
    if(op=="<"):
        print("function: op1")

    elif (op == "<="):
        print("function: op2")
    elif (op == "="):
        print("function: op3")
    elif (op == ">"):
        print("function:op4")
    elif (op == ">="):
        print("function: op5")



    print("vale is" + val)

def project(rel,attList):
    print(rel+' att- '+rel+' op->'+attList)



def join(rel1, att1, rel2, att2):
    print("rel1 is" + rel1)
    print("att1 is" + att1)
    print("rel2 is" + rel2)
    print("att2" + att2)


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

"""use this command after debug"""
# main()

load_data_from_pageLink()