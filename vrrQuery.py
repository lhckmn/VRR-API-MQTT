import http.client
import xml.etree.ElementTree as ET

#Halbe Höhe 20009281
#Essen HBF 20009289
#Schönscheidtstr 20009553
#Flughafen Terminal C 20018489

qOriginID = 20009281
qDestinationID = 20009553
qDateYear = 2020
qDateMounth = 3
qDateDay = 17
qTimeHour = 16
qTimeMinute = 0
qNumberOfTrips = 1
qUseRealtime = 1

Qpreamble = "/static02/XML_TRIP_REQUEST2?sessionID=0&requestID=0&language=DE"
QoriginData = "&type_origin=stopID&name_origin=" + str(qOriginID)
QdestinationData = "&type_destination=stopID&name_destination=" + str(qDestinationID)
QdateData = "&itdDateYear=" + str(qDateYear) + "&itdDateMonth=" + str(qDateMounth) + "&itdDateDay=" + str(qDateDay)
QtimeData = "&itdTimeHour="+ str(qTimeHour) + "&itdTimeMinute=" + str(qTimeMinute)
Qproperties = "&calcNumberOfTrips=" + str(qNumberOfTrips) + "&useRealtime=" + str(qUseRealtime)

conn = http.client.HTTPSConnection("openservice-test.vrr.de")
conn.request("GET", Qpreamble + QoriginData + QdestinationData + QdateData + QtimeData + Qproperties)
r1 = conn.getresponse()
print(r1.status, r1.reason)
data = str(r1.read())
conn.close()

data = data[2:-1] #maybe not necessary

root = ET.fromstring(data)

itdPartialRouteList = root.find("./itdTripRequest/itdItinerary/itdRouteList/itdRoute/itdPartialRouteList")

itdPartialRoute_first = itdPartialRouteList[0]
itdPartialRoute_last = itdPartialRouteList[len(itdPartialRouteList) - 1]

itdPoint_start = itdPartialRoute_first.find("itdPoint[@usage='departure']")
itdPoint_stop = itdPartialRoute_last.find("itdPoint[@usage='arrival']")

itdTime_start = itdPoint_start.find("itdDateTime/itdTime")
itdTime_stop = itdPoint_stop.find("itdDateTime/itdTime")

start_hour = int(itdTime_start.attrib["hour"])
start_minute = int(itdTime_start.attrib["minute"])

stop_hour = int(itdTime_stop.attrib["hour"])
stop_minute = int(itdTime_stop.attrib["minute"])

startTime = ""
if start_hour < 10:
    startTime = "0" + str(start_hour)
else:
    startTime = str(start_hour)

if start_minute < 10:
    startTime = str(startTime) + ":0" + str(start_minute)
else:
    startTime = startTime + ":" + str(start_minute)

stopTime = ""
if stop_hour < 10:
    stopTime = "0" + str(stop_hour)
else:
    stopTime = str(stop_hour)

if stop_minute < 10:
    stopTime = str(stopTime) + ":0" + str(stop_minute)
else:
    stopTime = stopTime + ":" + str(stop_minute)
    
print("Abfahrt: " + startTime + " Uhr")
print("Ankunft: " + stopTime + " Uhr")