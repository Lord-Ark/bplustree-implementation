import json
import os
from buildTree import findInTree, checkBtreeOnRelAndAtt
from remove import removeTable


def write(text, page):
    with open(page, 'w') as f:
        json.dump(text, f)


def read(path):
    try:
        f = open(path)
        return json.load(f)
    except:
        return


def findLocationOfAtrrInTupple(rel, att):
    schema = read("../data/schemas.txt")
    if(schema):
        for item in schema:
            if (item[0] == rel and item[1] == att):
                return item[3]


def findInBtree(rel, att, val):
    # write a function to check if using B+ tree or
    leafNodeReturn = findInTree(rel, att, val)
    leafNode = leafNodeReturn['page']
    if(leafNode == ''):
        return {'btree': False, 'cost': 0, 'leaf': ''}
    else:
        return {'btree': True, 'cost': leafNodeReturn['cost'], 'leaf': leafNode}


def select(rel, att, op, val):
    array: list = []
    pos = findLocationOfAtrrInTupple(rel, att)
    cost = 0

    relationName = 'Select-'+rel+'-'+att
    if(os.path.isdir('../data/'+relationName)):
        removeTable(relationName)
        # delete the directory and free the page pool

    # check for the invalid arguments here using function
    findtreeoutput = findInBtree(rel, att, val)

    if(findtreeoutput['btree']):
        cost = cost + findtreeoutput['cost']
        leaf = findtreeoutput['leaf']
        pagesarray = []
        for item in leaf['nodevalue']:
            if(item['key'] == val):
                pagesarray = item['value']

        for page in pagesarray:
            pagedata = read("../data/"+rel+"/"+page)
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

        # for item in array:  # what to do with the result
        #     print(item)
        # resultexplanation = 'Result \n'
        # appendInQueryResult(resultexplanation, array,"../queryOutput/queryResult.txt")

        print("With B+_tree, the cost of searching "+att+" " +
              op+" " + str(val) + " on "+rel + " is " + str(cost)+"  pages")

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

        # for item in array:      # what to do with the result
        #     print(item)
        # resultexplanation = 'Result \n'
        # appendInQueryResult(resultexplanation, array,"../queryOutput/queryResult.txt")

        print("Without B+_tree the cost of searching '" + att +
              " " + op+" "+str(val)+"' on "+rel+" is "+str(cost)+" pages")

    if(not os.path.isdir('../data/'+relationName)):
        os.mkdir('../data/'+relationName)

    pagelink = []
    for x in range(0, len(array), 2):
        pagepool = read("../data/pagePool.txt")
        lpage = pagepool.pop()
        write(pagepool, "../data/pagePool.txt")
        # cost += 1
        tempFile = []
        tempFile.append(array[x])
        if(x+1 < len(array)):
            tempFile.append(array[x+1])
        write(tempFile, "../data/"+relationName+"/"+lpage)
        pagelink.append(lpage)

    write(pagelink, "../data/"+relationName+"/pageLink.txt")
    # schemaarray = []
    schema = read("../data/schemas.txt")
    if(schema):
        for item in schema:
            if (item[0] == rel):
                schemaitem = []
                schemaitem.append(relationName)
                schemaitem.append(item[1])
                schemaitem.append(item[2])
                schemaitem.append(item[3])
                schema.append(schemaitem)
                write(schema, "../data/schemas.txt")

    # print(relationName)
    return relationName

#


def project(rel, attList):
    posarray: list = []
    for item in attList:
        posarray.append(findLocationOfAtrrInTupple(rel, item))
    path = "../data/"+rel+"/tmp"
    cost = 0

    relationName = 'Projection'
    for atts in attList:
        relationName = relationName+'-'+atts
    relationName = relationName + '-'+rel

    if(os.path.isdir('../data/'+relationName)):
        removeTable(relationName)
        # delete the directory and free the page pool

    if(len(posarray) == len(attList)):
        os.mkdir(path)
        # only make directory if it doesn't exist
    else:
        return
    pagelink = "../data/"+rel+"/pageLink.txt"
    pageArray = read(pagelink)
    tempfiledata = []
    for i in range(len(pageArray)):
        pagedata = read("../data/"+rel+"/"+pageArray[i])
        cost = cost + 1
        for j in range(len(pagedata)):
            Tuples = pagedata[j]
            valuefortemp = []
            for k in range(len(posarray)):
                valuefortemp.append(Tuples[posarray[k]])
            tempfiledata.append(valuefortemp)

    tempall = []
    tempallpages = []
    for x in range(0, len(tempfiledata), 2):

        pagepool = read("../data/pagePool.txt")
        lpage = pagepool.pop()
        write(pagepool, "../data/pagePool.txt")
        cost += 1
        tempFile = []
        tempFile.append(tempfiledata[x])
        if(x+1 < len(tempfiledata)):
            tempFile.append(tempfiledata[x+1])
        write(tempFile, "../data/"+rel+"/tmp/"+lpage)
        tempallpages.append(lpage)
        tempall.append(tempFile)

    write(tempallpages, "../data/"+rel+"/tmp/pageLink.txt")

    resultArray = []
    for a in range(len(tempallpages)):
        item = read("../data/"+rel+"/tmp/"+tempallpages[a])
        for x in range(len(item)):
            if(x+1 < len(item) and item[x] == item[x+1]):
                item.remove(item[x+1])
        cost += 1
        for b in range(a+1, len(tempallpages)):
            nextItem = read("../data/"+rel+"/tmp/"+tempallpages[b])
            cost += 1
            for elem in item:
                for nextelem in nextItem:
                    if(elem == nextelem):
                        item.remove(nextelem)
        write(item, "../data/"+rel+"/tmp/"+tempallpages[a])
        resultArray.append(item)

    resultItems = []
    for item in resultArray:
        resultItems = resultItems + item

    if(not os.path.isdir('../data/'+relationName)):
        os.mkdir('../data/'+relationName)

    pagelink = []
    for x in range(0, len(resultItems), 2):
        pagepool = read("../data/pagePool.txt")
        lpage = pagepool.pop()
        write(pagepool, "../data/pagePool.txt")
        # cost += 1
        tempFile = []
        tempFile.append(resultItems[x])
        if(x+1 < len(resultItems)):
            tempFile.append(resultItems[x+1])
        write(tempFile, "../data/"+relationName+"/"+lpage)
        pagelink.append(lpage)

    write(pagelink, "../data/"+relationName+"/pageLink.txt")

    schema = read("../data/schemas.txt")
    if(schema):
        for item in schema:
            if (item[0] == rel):
                schemaitem = []
                if item[1] in attList:
                    schemaitem.append(relationName)
                    schemaitem.append(item[1])
                    schemaitem.append(item[2])
                    schemaitem.append(item[3])
                    schema.append(schemaitem)

    write(schema, "../data/schemas.txt")

    # Remove Temp files
    pagelink = read("../data/"+rel+"/tmp/pageLink.txt")

    # remove pages from rel and add in pagepool
    pagepool = read("../data/pagePool.txt")
    for pageno in pagelink:
        os.remove("../data/"+rel+"/tmp/"+pageno)
        pagepool.append(pageno)

    write(pagepool, "../data/pagePool.txt")
    os.remove("../data/"+rel+"/tmp/pageLink.txt")
    os.rmdir("../data/"+rel+"/tmp")

    # print(' Cost of projection  '+str(cost))

    return relationName


def join(rel1, att1, rel2, att2):
    resultarray: list = []
    posatt1 = findLocationOfAtrrInTupple(rel1, att1)
    posatt2 = findLocationOfAtrrInTupple(rel2, att2)
    cost = 0
    outerRel = rel1
    innerRel = rel2
    innerAtt = att2
    outerAtt = att1
    outerRelPos = posatt1
    innerRelPos = posatt2
    btreeAvailable = False
    btreeOn = ''

    rootRel1 = checkBtreeOnRelAndAtt(rel1, att1)
    if(rootRel1 == ''):
        rootRel2 = checkBtreeOnRelAndAtt(rel2, att2)
        if(rootRel2 != ''):
            btreeAvailable = True
            innerRel = rel2
            innerRelPos = posatt2
            outerRel = rel1
            outerRelPos = posatt1
            innerAtt = att2
            outerAtt = att1
    else:
        btreeAvailable = True
        innerRel = rel1
        innerRelPos = posatt1
        outerRel = rel2
        outerRelPos = posatt2
        innerAtt = att1
        outerAtt = att2

    relationName = 'Join-'+outerRel+'-'+innerRel
    if(os.path.isdir('../data/'+relationName)):
        removeTable(relationName)
        print('deleting the existing directory' +
              relationName + 'and free the page pool')

    if(btreeAvailable):
        # outer loop on rel without btree and inner loop on rel with btree
        pagelinkRel = "../data/"+outerRel+"/pageLink.txt"
        pageArrayRel = read(pagelinkRel)
        pagelinkRelInner = "../data/"+innerRel+"/pageLink.txt"
        pageArrayRelInner = read(pagelinkRelInner)

        for pageRel in pageArrayRel:
            pagedataRel = read("../data/"+outerRel+"/"+pageRel)
            cost = cost + 1
            for tupleouter in pagedataRel:
                valueRelOuter = tupleouter[outerRelPos]
                findtreeoutput = findInBtree(innerRel, innerAtt, valueRelOuter)
                cost = cost + findtreeoutput['cost']
                leaf = findtreeoutput['leaf']
                pagesarray = []
                for item in leaf['nodevalue']:
                    if(item['key'] == valueRelOuter):
                        pagesarray = item['value']

                if(len(pagesarray) > 0):
                    for page in pagesarray:
                        pagedataInner = read("../data/"+innerRel+"/"+page)
                        cost = cost + 1
                        for tupleInner in pagedataInner:
                            valueforcom = tupleInner[innerRelPos]
                            if(valueRelOuter == valueforcom):
                                resultitem = []
                                for val in tupleouter:
                                    resultitem.append(val)
                                for x in range(len(tupleInner)):
                                    if(x != int(innerRelPos)):
                                        resultitem.append(tupleInner[x])
                                resultarray.append(resultitem)

        print('Cost of Joining '+rel1+' and '+rel2 +
              ' with B+ tree on '+innerRel+' is ' + str(cost) + ' I/Os')
    else:
        pagelinkRel1 = "../data/"+outerRel+"/pageLink.txt"
        pageArrayRel1 = read(pagelinkRel1)
        pagelinkRel2 = "../data/"+innerRel+"/pageLink.txt"
        pageArrayRel2 = read(pagelinkRel2)
        for pageRel1 in pageArrayRel1:
            pagedataRel1 = read("../data/"+outerRel+"/"+pageRel1)
            cost = cost + 1
            for TupleRel1 in pagedataRel1:
                valueRel1 = TupleRel1[posatt1]
                for pageRel2 in pageArrayRel2:
                    pagedataRel2 = read("../data/"+innerRel+"/"+pageRel2)
                    cost = cost + 1
                    for TupleRel2 in pagedataRel2:
                        valueRel2 = TupleRel2[posatt2]
                        if(valueRel1 == valueRel2):
                            resultitem = []
                            for val in TupleRel1:
                                resultitem.append(val)
                            # resultitem = resultitem + TupleRel1
                            for x in range(len(TupleRel2)):
                                if(x != int(innerRelPos)):
                                    resultitem.append(TupleRel2[x])
                            # in_first_tup = set(TupleRel1)
                            # in_second_tup = set(TupleRel2)
                            # in_second_but_not_in_first = in_second_tup - in_first_tup
                            resultarray.append(resultitem)


        print('Cost of Joining '+rel1+' and '+rel2 +
              ' without B+ tree is ' + str(cost) + ' I/Os')

    if(not os.path.isdir('../data/'+relationName)):
        os.mkdir('../data/'+relationName)

    schema = read("../data/schemas.txt")
    if(schema):
        position = 0
        for item in schema:
            if (item[0] == outerRel):
                schemaitem = []
                schemaitem.append(relationName)
                schemaitem.append(item[1])
                schemaitem.append(item[2])
                schemaitem.append(position)
                position += 1
                schema.append(schemaitem)

        for item in schema:
            if (item[0] == innerRel):
                if(item[1] != innerAtt):
                    schemaitem = []
                    schemaitem.append(relationName)
                    schemaitem.append(item[1])
                    schemaitem.append(item[2])
                    schemaitem.append(position)
                    position += 1
                    schema.append(schemaitem)

    write(schema, "../data/schemas.txt")

    pagelink = []
    for x in range(0, len(resultarray), 2):
        pagepool = read("../data/pagePool.txt")
        lpage = pagepool.pop()
        write(pagepool, "../data/pagePool.txt")
        # cost += 1
        tempFile = []
        tempFile.append(resultarray[x])
        if(x+1 < len(resultarray)):
            tempFile.append(resultarray[x+1])
        write(tempFile, "../data/"+relationName+"/"+lpage)
        pagelink.append(lpage)

    write(pagelink, "../data/"+relationName+"/pageLink.txt")

    return relationName

# join('Suppliers','sid','Supply','sid')
# select("Testsuppliers", 'sid', '=', 's10')
# project("Products",["color"])
#output > array[['p03','drill','black'],['p05','drill','green']]
# select("Suppliers", "sid", "=", "s23")
#output > array [['p05','drill','green']]
