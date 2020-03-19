# -*- coding: utf-8 -*-

class RouteData: 
    duration = ""
    departureTime = ""
    arrivalTime = ""
    departureName = ""
    arrivalName = ""
    transportShortnames = []

    def __init__(self):
        self.duration = ""
        self.departureTime = ""
        self.arrivalTime = ""
        self.departureName = ""
        self.arrivalName = ""
        self.transportShortnames = []
    
    def printRoute(self):
        print(self.departureName + " --> " + self.arrivalName)
        print(self.departureTime + " Uhr - " + self.arrivalTime + " Uhr  (" + self.duration + "h)")
        shortnamesConcat = ""
        for i in range(0, len(self.transportShortnames)):
            shortnamesConcat = shortnamesConcat + self.transportShortnames[i] + " "
        print(shortnamesConcat)
        print("")
