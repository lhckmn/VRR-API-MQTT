# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import resultClasses as RC


def TQ_processQuery(data):
    root = ET.fromstring(str(data))
    itdRouteList = root.find("./itdTripRequest/itdItinerary/itdRouteList")
    itdCleanRouteList = itdRouteList.findall("itdRoute[@alternative='0']")
    
    processedRoutes = []
    for i in range(0, len(itdCleanRouteList)):
        processedRoutes.append(TQ_getRoute(itdCleanRouteList[i]))
    
    return processedRoutes
    

def TQ_getRoute(itdRoute):
    duration = str(itdRoute.attrib["publicDuration"])

    itdPartialRouteList = itdRoute.find("./itdPartialRouteList")
    
    transportShortnames = []
    for i in range(0, len(itdPartialRouteList)):
        itdMeansOfTransport = itdPartialRouteList[i].find("itdMeansOfTransport")
        transportShortnames.append(str(itdMeansOfTransport.attrib["shortname"]))

    itdPartialRoute_first = itdPartialRouteList[0]
    itdPartialRoute_last = itdPartialRouteList[len(itdPartialRouteList) - 1]

    itdPoint_departure = itdPartialRoute_first.find("itdPoint[@usage='departure']")
    itdPoint_arrival = itdPartialRoute_last.find("itdPoint[@usage='arrival']")

    departureName = str(itdPoint_departure.attrib["name"])
    arrivalName = str(itdPoint_arrival.attrib["name"])

    itdTime_departure = itdPoint_departure.find("itdDateTime/itdTime")
    itdTime_arrival = itdPoint_arrival.find("itdDateTime/itdTime")

    departure_hour = int(itdTime_departure.attrib["hour"])
    departure_minute = int(itdTime_departure.attrib["minute"])

    arrival_hour = int(itdTime_arrival.attrib["hour"])
    arrival_minute = int(itdTime_arrival.attrib["minute"])

    departureTime = ""
    if departure_hour < 10:
        departureTime = "0" + str(departure_hour)
    else:
        departureTime = str(departure_hour)

    if departure_minute < 10:
        departureTime = str(departureTime) + ":0" + str(departure_minute)
    else:
        departureTime = departureTime + ":" + str(departure_minute)

    arrivalTime = ""
    if arrival_hour < 10:
        arrivalTime = "0" + str(arrival_hour)
    else:
        arrivalTime = str(arrival_hour)

    if arrival_minute < 10:
        arrivalTime = str(arrivalTime) + ":0" + str(arrival_minute)
    else:
        arrivalTime = arrivalTime + ":" + str(arrival_minute)
    
    trip = RC.RouteData()
    trip.duration = duration
    trip.departureTime = departureTime
    trip.arrivalTime = arrivalTime
    trip.departureName = departureName
    trip.arrivalName = arrivalName
    trip.transportShortnames = transportShortnames
    return trip