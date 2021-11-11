import json;


def read(path):
    f = open(path)
    return json.load(f)

def findLocationOfAtrrInTupple(rel, att):
    schema = read("../data/schemas.txt")
    for item in schema:
        if (item[0] == str.capitalize(rel) and item[1] == att):
            return item[3]


def check_if_use_B_tree():
    # write a function to check if use B+ tree
    result=None
    return result

def select(rel, att, op, val):

    array: list=[]







    file_Suppliers = read("../data/Suppliers/pageLink.txt")
    file_Supply = read("../data/Supply/pageLink.txt")

    pos = findLocationOfAtrrInTupple("Products",att)
    if(rel=="Products"):
        file_Products = read("../data/Products/pageLink.txt")
        for i in range(len(file_Products)):

            pagedata= read("../data/Products/"+file_Products[i])
            for j in range(len(pagedata)):
                Tuples=pagedata[j]
                valueforcom = Tuples[pos]
                if(op == '='):
                    if(valueforcom == val):
                        array.append(Tuples)
                if(op == '>='):
                    if(valueforcom >= val):
                        array.append(Tuples)
                if(op == '<='):
                    if(valueforcom <= val ):
                        array.append(Tuples)

                if (op == '<'):
                    if (valueforcom < val):
                        array.append(Tuples)
                if (op == '>'):
                    if (valueforcom > val):
                        array.append(Tuples)




                #pageNumber_in_Tuples=Tuples[0]
                #val_in_Tuples=Tuples[1]
                #att_in_Tuples=Tuples[2]
                #if((val_in_Tuples==val) and (att_in_Tuples==att)):
                #    value=pageNumber_in_Tuples










    # if use B+ tree, print att+op+val+rel+val
    if(pos!=None):
        print("With B+_tree, the cost of searching "+att+" "+op+" "+val+" on "+rel +" is " + array+"  pages")


    # if not use B+ tree, print att+op+val+rel+val
    else:
        print("Without B+_tree the cost of searching"+att+op+val+"on"+rel+"is"+array+"pages")


#
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
select("Products","pname","=","drill")
#output > array[['p03','drill','black'],['p05','drill','green']]
select("Products","pid","=","p05")
#output > array [['p05','drill','green']]
