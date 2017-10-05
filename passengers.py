


class passengerDist:

    #This is set to true if testdata is used, in order to properly read the passenger count dictionaries
    testData = False

    #Direction PR -> CS
    #PR has ID 0 and index 0 in the list of passenger counts
    passengersA = {}

    #Direction CS -> PR
    #same goes here for the indices of passenger counts
    passengersB = {}

    lastDeparturesA = [0] * 9

    lastDeparturesB = [0] * 9

    def __init__(self): {}

    def createFromTestFile(self, file): {}

    #The empirical data instance requires two files
    def createFromEmpiricalData(self, fileA, fileB):
        openA = open(fileA)
        for line in openA:
            sp = line.split(",")
            self.passengersA[sp[0]] = list(map(lambda x : int(x), sp[1:10]))


        openB = open(fileB)
        for line in openB:
            sp = line.split(",")
            self.passengersB[sp[0]] = list(reversed(list(map(lambda x: int(x), sp[1:10])))) #the list has to be reversed due to the order of the stations

    #returns a quantity of passengers for a given stop at a given time
    #the last arrival is stored for each stop in each direction
    def getPassengers(self, seconds, stationId): {}

    def secsToTimeSegment(self, seconds): {}

asd = passengerDist()
asd.createFromEmpiricalData("processeddata/12a.csv", "processeddata/12b.csv")

