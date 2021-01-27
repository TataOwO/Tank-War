import json
from os import listdir
from os.path import isfile, join
from operator import itemgetter

def getFile(extension):
    try:
        detect = [f for f in listdir(r"..\JSON") if isfile(join(r"..\JSON", f))]
    except:
        detect = [f for f in listdir("JSON") if isfile(join("JSON", f))]

    count = 0
    for name in range(len(detect)):
        name = detect[count].split(".")
        if name[1].lower() == extension:
            # print(name[0])
            detect[count] = name[0]
            count += 1
        else:
            detect.pop(count)
    return detect
    
def sorting(inputFile):
    for count,blockName in enumerate(inputFile["mapBlocks"]):
        blockData = inputFile["mapBlocks"][blockName]
        if blockData["X"] != None:
            # print(list(zip(*sorted(zip( blockData["X"], blockData["Y"] ),key=itemgetter(0,1)))))
            blockData["X"], blockData["Y"] = list(zip(*sorted(zip( blockData["X"], blockData["Y"] ),key=itemgetter(0,1))))
            inputFile["mapBlocks"][blockName].update(blockData)
    return inputFile

def main():
    file = getFile("json")
    sc = json.load(open(file))
    sc = sorting(sc)

    with open(file, "w") as writeIn:
        writeIn.write(json.dumps(sc, indent=4))

if __name__ == '__main__':
    main()
    input()