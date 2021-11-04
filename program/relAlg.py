
    
def select(rel, att, op, val):

    print("The Input Information is"+"Rel"+rel+' att- '+att+' op->'+op+' val->'+val)

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

main()