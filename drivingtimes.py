import numpy
class DrivingTimes:

    #The parameters are for driving times TOWARDS a certain station
    #so in direction A, the first parameters are associated with station 1; WKZ
    def __init__(self):
        # The parameters for the gamma function
        self.parametersA = {
            1: [134.3131, 0.818982],
            2: [113.1017, 0.689645],
            3: [115.9655, 0.707107],
            4: [99.19677, 0.604858],
            5: [128.0625, 0.780869],
            6: [98.36666, 0.933783],
            7: [153.1405, 0.933783],
            8: [148.7952, 0.907288]
        }

        self.parametersB = {
            0: [136.1323, 0.830075],
            1: [113.1017, 0.689645],
            2: [118.7603, 0.724148],
            3: [99.19677, 0.604858],
            4: [128.7012, 0.784763],
            5: [98.36666, 0.599797],
            6: [199.6297, 1.217254],
            7: [148.243, 0.903921]
        }

    def getDrivingTime(self,station,direction):
        shape = 0
        scale = 0

        if direction == 0:
            shape = self.parametersA[station][0]
            scale = self.parametersA[station][1]
        else:
            shape = self.parametersB[station][0]
            scale = self.parametersB[station][1]

        return numpy.random.gamma(shape, scale)