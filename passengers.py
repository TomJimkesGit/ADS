


class passengerDist:

    def __init__(self, csvFile, testData = false):
        file = open(csvFile)
        self.passengers = {}
        if(testData):
            self.createFromTestFile(file)
        else:
            self.createFromEmpiricalData(file)

    def createFromTestFile(self, file):

    def createFromEmpiricalData(self, file):
