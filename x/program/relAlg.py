def main():
    name= input("enter name: ")
    select(name)
def select(rel, att, op, val):

    print("rel is "+rel)
    print("att is " + att)
    print("op is " + op)
    print("val is " + val)


def project(rel,attlist):
    print("rel is"+ rel)
    print("attlist is"+ attlist)


def join(rel1, att1, rel2, att2):
    print("rel1 is" + rel1)
    print("att1 is" + att1)
    print("rel2 is" + rel2)
    print("att2" + att2)

