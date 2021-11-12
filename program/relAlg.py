import json
from buildTree import findInTree


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
    leafNodeReturn = json.loads( findInTree(rel, att, val))
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
    print(rel+' att- '+rel+' op->'+attList)


def join(rel1, att1, rel2, att2):
    print("rel1 is" + rel1)
    print("att1 is" + att1)
    print("rel2 is" + rel2)
    print("att2" + att2)


# """use this command after debug"""
# main()
# select("Products", "pname", "=", "drill")
select("Supply", 'pid', '=', 'p23')
#output > array[['p03','drill','black'],['p05','drill','green']]
# select("Products", "pid", "=", "p05")
#output > array [['p05','drill','green']]
