
def processPassengers():
    file = open("rawdata\\12a.csv")
    grouped = []
    header1 = ""
    header2 = ""
    for line in file:
        sp = line.split(';')
        if (sp[0] == ""): #first line
            header1 = line
        elif (sp[0] == "Trip"):
            header2 = line
        else:
            time = sp[2]

