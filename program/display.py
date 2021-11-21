
from buildTree import read
from buildTree import write

def traverseAllNode(rootpage):
    resultArray = []
    # global resultArray
    root = read("../index/"+rootpage)
    if(root['type'] == 'L'):
        # print(root)
        resultArray.append(root)
        return resultArray
    else:
        resultArray.append(root)
        # resultArray = resultArray +  append(root)
        for item in root['nodevalue']:
            leftArray = traverseAllNode(item['leftNode'])
            resultArray = resultArray +leftArray
            # resultArray.append(traverseAllNode(item['leftNode']))
            rightArray = traverseAllNode(item['rightNode'])
            resultArray = resultArray +rightArray
            # resultArray.append(traverseAllNode(item['rightNode']))
        return resultArray


def displayTree(filename):
    if(filename != ''):
        print('append the value and delete')
        allitem = traverseAllNode(filename)
        seen_pages = set()
        new_list = []
        for obj in allitem:
            if obj['page'] not in seen_pages:
                new_list.append(obj)
                seen_pages.add(obj['page'])

        f = open("../treePic/tree"+filename, "a")
        for item in new_list:
            f.write(str(item))
            f.write('\n')
        f.close()
            

# displayTree('pg08.txt')