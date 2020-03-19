# -*- coding: utf-8 -*-
import http.client

def getQuery(url, query):
    connection = http.client.HTTPSConnection(str(url))
    connection.request("GET", str(query))
    response = connection.getresponse()
    if response.reason == "OK":
        data = str(response.read())
        connection.close()
        data = data[2:-1] #cutting header symbols
        return data
    else:
        print("ERROR! " + str(response.status) + ", " + str(response.reason))
        return None


def tripQuery(OriginID, DestinationID, DateYear, DateMounth, DateDay, TimeHour, TimeMinute, NumberOfTrips, UseRealtime, ExcludedMeans):
    Qpreamble = "/static02/XML_TRIP_REQUEST2?sessionID=0&requestID=0&language=DE"
    QoriginData = "&type_origin=stopID&name_origin=" + str(OriginID)
    QdestinationData = "&type_destination=stopID&name_destination=" + str(DestinationID)
    QdateData = "&itdDateYear=" + str(DateYear) + "&itdDateMonth=" + str(DateMounth) + "&itdDateDay=" + str(DateDay)
    QtimeData = "&itdTimeHour="+ str(TimeHour) + "&itdTimeMinute=" + str(TimeMinute)
    Qproperties = "&calcNumberOfTrips=" + str(NumberOfTrips) + "&useRealtime=" + str(UseRealtime)
    
    QexcludedMeans = ""
    if len(ExcludedMeans) > 0:
        QexcludedMeans = "&excludedMeans=checkbox&"
        for i in range(0, len(ExcludedMeans)):
            QexcludedMeans = QexcludedMeans + "exclMOT_" + str(ExcludedMeans[i]) + "=1"
            if i < len(ExcludedMeans) - 1:
                QexcludedMeans = QexcludedMeans + "&"
    
    query = str(Qpreamble + QoriginData + QdestinationData + QdateData + QtimeData + Qproperties + QexcludedMeans)
    data = getQuery("openservice-test.vrr.de", query)
    return data