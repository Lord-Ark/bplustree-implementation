def main():
    funcName= input("enter the function(number) you want to call: \n 1. Project \n 2. Select \n 3. Join \n  Enter Number: ")
    
    if funcName=='1':
        relName= input("Enter relation name: ")
        attList= input("Enter attribute name: ")
        project(relName,attList)

    elif funcName == '2':
        relName2= input("Enter relation name: ")
        attName= input("Enter attribute name: ")
        opVal= input("Enter operator value: ")
        val= input("Enter value: ")
        select(relName2,attName,opVal,val)
    
def select(rel, att, op, val):
    print(rel+' att- '+att+' op->'+op+' val->'+val)

def project(rel,attList):
    print(rel+' att- '+rel+' op->'+attList)

main()