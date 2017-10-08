
import math
import numpy

class passengerDist:

    #This is set to true if testdata is used, in order to properly read the passenger count dictionaries
    testData = False

    #Direction PR -> CS
    #PR has ID 0 and index 0 in the list of passenger counts
    passengersA = {}

    #Direction CS -> PR
    #same goes here for the indices of passenger counts
    passengersB = {}

    lastArrivalsA = ["6:00"] * 9

    lastArrivalsB = ["6:00"] * 9

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
    #direction == 0 --> A, direction == 1 --> B
    def boarding(self, seconds, stationId, direction):
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

        print(lastTime)
        print(lastTimeSegment)
        print(timeSegment)

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

    #returns the number of passengers
    def getPassengers(self, samples, timeSegment, stationId, direction):
        # set the correct dict to obtain passenger information
        passengersRef = self.passengersB
        if (direction == 0):
            passengersRef = self.passengersA

        #average arrivals per minute
        lambd = (passengersRef[timeSegment][stationId] / 15) #NOT STATIC!!!!
        return sum(list(numpy.random.poisson(lambd, samples)))

    #time 0 is 6:00
    #returns the segment
    def toTimeSegment(self, hours, minutes):
        if self.testData:  #if the simulation is inst. with testdata, the segments differ
            if hours < 7: return "6:00"
            elif hours < 9: return "7:00"
            elif hours < 16: return "9:00"
            elif hours < 18: return "16:00"
            else: return "18:00"
        else:
            mins = math.floor(minutes / 15) * 15
            mins = str(mins) if (mins > 0) else "00"
            return ":".join([str(hours), mins])

    #n.o. samples to be taken from a certain distribution
    #hours2 and minutes2 are later
    #returns a tuple
    def remainder(self, hours, minutes, hours2, minutes2):
        remHours = hours2 - hours

        if(hours == hours2):
            remMinutes = minutes2 - minutes
        else :
            remMinutes = minutes2 + (60 - minutes)

        return [hours, minutes]

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

        #we need to draw from segments inbetween the indices and add these totals to the global total
        for index in range(startIndex + 1, endIndex):
            boardingPassengers += self.getPassengers(15, list(passengersRef)[index], stationId, direction)

        return boardingPassengers

#asd = passengerDist()
#asd.createFromEmpiricalData("processeddata/12a.csv", "processeddata/12b.csv")

#print(asd.passengersA["7:15"])
#print(asd.passengersA[list(asd.passengersA)[5]])
#passe = asd.boarding(36000, 8, 1)
#print(asd.lastArrivalsA, asd.lastArrivalsB)
#print(passe)
