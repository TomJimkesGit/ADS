
import math

def processPassengers():
    file = open("rawdata/12bbuckets.csv")
    grouped = []
    header1 = []
    header2 = []
    dateBuckets = {}
    for line in file:
        sp = line.split(',')
        if (sp[0] == ""): #first line
            header1 = sp
        elif (sp[0] == "Trip"):
            header2 = sp
        else:
            date = sp[1].split('/')[0]
            time = sp[-1].rstrip()
            passengers = list(map(lambda x: int(x), sp[3:21]))
            if(date not in dateBuckets):
                dateBuckets[date] = {}
            if(time not in dateBuckets[date]):
                dateBuckets[date][time] = [0] * 18
            for num in range(0,18):
                dateBuckets[date][time][num] += passengers[num]

    #now that passengers have been summed to segments for each date, we group by time
    timeBuckets = {}

    for key,value in dateBuckets.items():
        for tkey,tvalue in value.items():
            if(tkey in timeBuckets):
                timeBuckets[tkey].append(tvalue)
            else:
                timeBuckets[tkey] = [tvalue]

    #now that all times have been grouped together, we can average
    averages = {}
    for key,value in timeBuckets.items():
        totalCount = len(value)
        averages[key] = []
        for num in range(0,18):
            accum = 0
            for li in value:
                accum += li[num]
            if accum > 0:
                averages[key].append(int(math.ceil(accum / totalCount)))
            else:
                averages[key].append(0) #if there were no passengers in this segment any of the days


    outputFile = open("processeddata/12bproc.csv", 'w')

    #write headers
    outputFile.write(','.join(header1[2:21]) + '\n')
    outputFile.write(','.join(header2[2:21]) + '\n')
    for key,value in averages.items():
        passengers = ','.join(str(x) for x in value)
        outputFile.write(key + "," + passengers + '\n')


processPassengers()