from .codes import codes
from .neighbors import nbrs

# Global data about neighboring countries
nbr_data = nbrs

# Global data to help with converting codes into readable country names
codes_data = codes

# If the country code x isn't recognised, we won't get data about its
# neighbors from nbr_data, so build an empty dict() as backup
noNeighbors = dict()
noNeighbors["neighbors"] = []

# get all the neighbors of a given place x
# returns an array
def getNeighbors(x):
    # pass in noNeighbors which will be returned if x is not found as a key
    return nbr_data.get(x, noNeighbors).get("neighbors")

# find a shortest path from start to end
# implements Dijkstra's algorithm
def getShortestPathUsingCodes(start, end):
    # We can switch on debug printing if we need to troubleshoot
    printDebug = False

    # collect together an array of possible beginnings of paths
    # from start
    # we will take these beginnings and 'grow' or extend them
    # adding neighbors at the end
    # and make new beginnings
    pathsToExtend = [[start]]

    # remember the best (shortest) path we have found so far
    # from start to each place
    bestPathTo = dict()
    bestPathTo[start] = [start]

    while True:
        if len(pathsToExtend) == 0:
            # we don't have any more paths to extend
            # so we can't do any more work
            break

        # take the first path to extend and be ready to extend it
        pathToExtend = pathsToExtend[0]
        # we won't try to extend this path again, remove it from paths
        pathsToExtend.pop(0)

        # work out where this path to extend might go next
        # get its end (the last place in the path)
        endOfPathToExtend = pathToExtend[len(pathToExtend) - 1]
        # where might we go next - what are the neighbors of the end
        possibleExtensions = getNeighbors(endOfPathToExtend)

        if printDebug:
            print("---- start extending ", pathToExtend)
        for possibleNextStep in possibleExtensions:
            # print('possible extension is ', ext)

            # is it already in our path?
            # avoid going round in circles - never revisit a place we have already been
            if possibleNextStep in pathToExtend:
                # print('do not extend with ',ext, 'because its already in ', pathToExtend)
                continue

            bestPathSoFarToExt = bestPathTo.get(possibleNextStep, "none")
            if (
                bestPathSoFarToExt != "none"
                and len(bestPathSoFarToExt) <= len(pathToExtend) + 1
            ):
                # we can't improve on what is already known
                # print('do not extend with ',ext, 'because we already know a better or matching path there ', bestPathSoFarToExt)
                continue

            # ok, we do want to extend the pathToExtend by attaching the possibleNextStep
            newPath = pathToExtend.copy()
            newPath.append(possibleNextStep)
            # print('newPath is ', newPath)

            bestPathTo[possibleNextStep] = newPath

            if possibleNextStep == end:
                # print(ext, ' == ', end)
                # print("found a path from start to end! ", newPath)
                break  # our work is done, don't add any more extensions

            # we may want to extend this newPath even further to get to end
            # so add newPath to the pathsToExtend
            pathsToExtend.append(newPath)

        if bestPathTo.get(end, "none") != "none":
            break  # our work is done, don't extend any more paths

        if printDebug:
            print("here are all our paths now")
            for path in pathsToExtend:
                print(path)

        # print('---- finished extending ', pathToExtend)

    # print('path from ', start, 'to ', end, ' is ', bestPathTo.get(end, 'none'))
    return bestPathTo.get(end, [])


def hasNameFromCode(code):
    for x in codes_data:
        if x["code"] == code:
            return True
    return False


def hasCodeFromName(name):
    for x in codes_data:
        if x["name"] == name:
            return True
    return False


def findNameFromCode(code):
    for x in codes_data:
        if x["code"] == code:
            return x["name"]
    return code


def findCodeFromName(name):
    for x in codes_data:
        if x["name"] == name:
            return x["code"]
    return name


def getShortestPathUsingNames(start, end):
    if not (hasCodeFromName(start)):
        return ["ERROR not recognised " + start]
    if not (hasCodeFromName(end)):
        return ["ERROR not recognised " + end]

    startCode = findCodeFromName(start)
    endCode = findCodeFromName(end)

    codePath = getShortestPathUsingCodes(startCode, endCode)

    return list(map(findNameFromCode, codePath))
