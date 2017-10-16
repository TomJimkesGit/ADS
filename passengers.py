
import math
import numpy

class passengerDist:

    #constructor
    def __init__(self):
        # This is set to true if testdata is used, in order to properly read the passenger count dictionaries
        self.testData = False

        # Direction PR -> CS
        # PR has ID 0 and index 0 in the list of passenger counts
        self.passengersA = {}

        # Direction CS -> PR
        # same goes here for the indices of passenger counts
        self.passengersB = {}

        self.disembarkingA = {"6:00": [0] * 9, "7:00": [0] * 9, "9:00": [0] * 9, "16:00": [0] * 9, "18:00": [0] * 9}
        self.disembarkingB = {"6:00": [0] * 9, "7:00": [0] * 9, "9:00": [0] * 9, "16:00": [0] * 9, "18:00": [0] * 9}

        # the references for ids
        self.idRefs = {
            "P+R Uithof": 0,
            "WKZ": 1,
            "UMC": 2,
            "Heidelberglaan": 3,
            "Padualaan": 4,
            "Kromme Rijn": 5,
            "Galgenwaard": 6,
            "Vaartscherijn": 7,
            "Centraal Station Centrumzijde": 8
        }

        self.lastArrivalsA = ["6:00"] * 9

        self.lastArrivalsB = ["6:00"] * 9

    #PUBLIC FUNCTIONS

    #If a testfile is used, this function is called to instatiate the classvariables
    def createFromTestFile(self, csvFile):
        #Do use segments of 15 minutes to make programming easier
        self.testData = True

        file = open(csvFile)
        # init passenger dics
        self.passengersA = {"6:00": [0] * 9, "7:00": [0] * 9, "9:00": [0] * 9, "16:00": [0] * 9, "18:00": [0] * 9}
        self.passengersB = {"6:00": [0] * 9, "7:00": [0] * 9, "9:00": [0] * 9, "16:00": [0] * 9, "18:00": [0] * 9}

        #these will be used to calculate the fractions of leaving passengers
        disemA = {"6:00": [0] * 9, "7:00": [0] * 9, "9:00": [0] * 9, "16:00": [0] * 9, "18:00": [0] * 9}
        disemB = {"6:00": [0] * 9, "7:00": [0] * 9, "9:00": [0] * 9, "16:00": [0] * 9, "18:00": [0] * 9}


        for line in file:
            sp = line.split(";")
            if sp[1] == "0":
                self.passengersA[str(sp[2]) + ":00"][self.idRefs[sp[0]]] = int(float(sp[4]))
                disemA[str(sp[2]) + ":00"][self.idRefs[sp[0]]] = int(float(sp[5]))
            elif sp[1] == "1":
                self.passengersB[str(sp[2]) + ":00"][self.idRefs[sp[0]]] = int(float(sp[4]))
                disemB[str(sp[2]) + ":00"][self.idRefs[sp[0]]] = int(float(sp[5]))

        #instantiate the disembarking dictionaries
        self.getDisembarkingRatios(disemA, 0)
        self.getDisembarkingRatios(disemB, 1)

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

        #Fill the disembarking dics for the empirical data
        self.disembarkingA = {"6:00": [0, 0.143, 0.034, 0.00, 1.84, 0.157, 1.316, 2.661, 100],
                           "7:00": [0, 0, 0.064, 0.005, 19.170, 0.154, 3.955, 8.454, 100],
                           "9:00": [0, 0.143, 0.034, 0.00, 1.84, 0.157, 1.316, 2.661, 100],
                           "16:00": [0, 0.305, 0.018, 0.00, 0.0682, 0.075, 0.902, 3, 100],
                           "18:00": [0, 0.143, 0.034, 0.00, 1.84, 0.157, 1.316, 2.661, 100]}

        self.disembarkingB = {"6:00": [100, 97.734, 79.790, 64.240, 51.796, 5.285, 6.256, 8.676, 0],
                              "7:00": [100, 97.472, 80.021, 64.845, 53.836, 2.677, 3.472, 3.625, 0],
                              "9:00": [100, 97.734, 79.790, 64.240, 51.796, 5.285, 6.256, 8.676, 0],
                              "16:00": [100, 99.745, 69.401, 52.3, 43.090, 14.989, 10.572, 13.861,0],
                              "18:00": [100, 97.734, 79.790, 64.240, 51.796, 5.285, 6.256, 8.676, 0]}

    #returns a quantity of passengers for a given stop at a given time
    #the last arrival is stored for each stop in each direction
    #direction == 0 --> A, direction == 1 --> B
    def embarkingPassengers(self, seconds, stationId, direction):
        hours = math.floor(seconds / 3600)
        minutes = math.floor((seconds - hours * 3600) / 60)
        hours += 6

        #If there is a remainder of more than half a minute, we add it to the minutes/hours
        if seconds % 60 > 30:
            if minutes < 59:
                minutes += 1
            else:
                minutes = 0
                hours += 1

        #get passengers for previous
        lastTime = self.lastArrivalsA[stationId] if (direction == 0) else self.lastArrivalsB[stationId]
        lastTimeHours = int(lastTime.split(":")[0])
        lastTimeMinutes = int(lastTime.split(":")[1])
        lastTimeSegment = self.toTimeSegment(lastTimeHours, lastTimeMinutes)

        timeSegment = self.toTimeSegment(hours, minutes)

        # set the correct dict to update the new last arrival time
        arrivalsRef = self.lastArrivalsB
        if (direction == 0):
            arrivalsRef = self.lastArrivalsA

        boardingPassengers = 0

        #if the time segments are equal, the result is simple
        if(lastTimeSegment == timeSegment):
            remainderCur = self.remainder(lastTimeHours, lastTimeMinutes, hours, minutes)
            boardingPassengers = self.getPassengers(remainderCur[0] * 60 + remainderCur[1], timeSegment, stationId, direction)
        else:
            #if they differ,we need to take samples from the different segments
            boardingPassengers = self.spreadSegments(lastTimeHours, lastTimeMinutes, lastTimeSegment, hours, minutes, timeSegment, stationId, direction)


        #update the last arrival time

        arrivalsRef[stationId] = ":".join([str(hours), (str(minutes) + "0" if (minutes < 10) else str(minutes))])

        return boardingPassengers

    #Returns a PERCENTAGE of passengers that will disembark
    def disembarkingPassengers(self, hours, minutes, stationId, direction):
        timeSegment = self.disembarkingTimeSegment(hours, minutes)
        dicRef = self.disembarkingA if direction == 0 else self.disembarkingB
        return dicRef[stationId][timeSegment]


    #PRIVATE FUNCTIONS

    # n.o. samples to be taken from a certain distribution
    # hours2 and minutes2 are later
    # returns a tuple
    def remainder(self, hours, minutes, hours2, minutes2):
        remHours = hours2 - hours

        if (hours == hours2):
            remMinutes = minutes2 - minutes
        else:
            remMinutes = minutes2 + (60 - minutes)

        return [remHours, remMinutes]

    #get the ratios for disembarking passengers
    def getDisembarkingRatios(self, disem, direction):
        if direction == 0:
            embRef = self.passengersA
            disembRef = self.disembarkingA
        else:
            embRef = self.passengersB
            disembRef = self.disembarkingB

        #in the case of direction B, we have to start summing at the end of the list
        for key, value in disem.items():
            for n in range(0, 9):
                if(direction == 0):
                    embarkingTotal = sum(embRef[key][0:(n+1)])
                    disembarkingTotal = disem[key][0] if n == 0 else sum(disem[key][0:n])
                else:
                    embarkingTotal = sum(embRef[key][n + 1:9])
                    disembarkingTotal = disem[key][0] if n == 0 else sum(disem[key][n + 1:9])

                if embarkingTotal == 0 or disembarkingTotal == 0 or disem[key][n] == 0:
                    disembRef[key][n] = 0
                else:
                    #The max is 100 per cent, but this can be exceded due to rounding errors
                    disembRef[key][n] = min(100, disem[key][n] / (embarkingTotal - disembarkingTotal) * 100)

    def spreadSegments(self, lastHours, lastMinutes, lastSegment, hours, minutes, segment, stationId, direction):
        # set the correct dict to obtain passenger information
        passengersRef = self.passengersB
        if (direction == 0):
            passengersRef = self.passengersA
        startIndex = list(passengersRef).index(lastSegment)
        endIndex = list(passengersRef).index(segment)

        #first calc the remainders for the head and tail distributions
        remainderLast = self.remainder(lastHours, lastMinutes, int(segment.split(":")[0]), int(segment.split(":")[1]))
        remainderCur = self.remainder(int(segment.split(":")[0]), int(segment.split(":")[1]), hours, minutes)

        # now add the passengers from both segments to get the total amount of passengers for the head and tail
        boardingPassengers = self.getPassengers(remainderCur[0] * 60 + remainderCur[1], segment, stationId, direction)
        boardingPassengers += self.getPassengers(remainderLast[0] * 60 + remainderLast[1], lastSegment, stationId,direction)

        print(boardingPassengers)

        #we need to draw from segments inbetween the indices and add these totals to the global total
        for index in range(startIndex + 1, endIndex):
            boardingPassengers += self.getPassengers(-1, list(passengersRef)[index], stationId, direction)

        return boardingPassengers

    #returns the number of passengers
    #if samples is set to -1, we take samples for each discrete step in the timesegment
    def getPassengers(self, samples, timeSegment, stationId, direction):

        print(samples)

        # set the correct dict to obtain passenger information
        passengersRef = self.passengersB
        if (direction == 0):
            passengersRef = self.passengersA

        #average arrivals per minute
        denominator = 15

        #if the testdata is used, the denominator depends on the segment (the amanount of minutes in the segment
        if self.testData:
            if timeSegment == "6:00":
                denominator = 60
            elif timeSegment == "7:00":
                denominator = 120
            elif timeSegment == "9:00":
                denominator = 4200
            elif timeSegment == "16:00":
                denominator = 120
            else:
                denominator = 210

        #take samples for each discrete step
        if samples == -1:
            samples = denominator

        lambd = (passengersRef[timeSegment][stationId] / denominator)
        return sum(list(numpy.random.poisson(lambd, samples)))

    #time 0 is 6:00
    #returns the segment
    def toTimeSegment(self, hours, minutes):
        if self.testData:  #if the simulation is inst. with testdata, the segments differ
            return self.disembarkingTimeSegment(hours, minutes)
        else:
            mins = math.floor(minutes / 15) * 15
            mins = str(mins) if (mins > 0) else "00"
            return ":".join([str(hours), mins])

    #Timesegments for disembarking passengers
    #These are the same for testdata
    def disembarkingTimeSegment(self, hours, minutes):
        if hours < 7:
            return "6:00"
        elif hours < 9:
            return "7:00"
        elif hours < 16:
            return "9:00"
        elif hours < 18:
            return "16:00"
        else:
            return "18:00"


asd = passengerDist()
#asd.createFromEmpiricalData("processeddata/12a.csv", "processeddata/12b.csv")
asd.createFromTestFile("testdata/input-data-passengers-01.csv")


passe = asd.embarkingPassengers(55800, 3, 0)
print(asd.lastArrivalsA, asd.lastArrivalsB)
print(passe)

