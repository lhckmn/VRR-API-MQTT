# -*- coding: utf-8 -*-
import commFunctions as VRR
import dataFunctions as dat
import paho.mqtt.client as mqtt
import time
from datetime import datetime

ExcludedMeans = [0, 14, 15, 16] #[Zug, IR & D, IC & EC, ICE] ausschließen
#Halbe Höhe 20009281
#Essen HBF 20009289
#Schönscheidtstr 20009553
#Flughafen Terminal C 20018489

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    mqttMSG = msg.payload.decode()
    print("Received request! (" + mqttMSG + ")")
    reqType = mqttMSG.partition("#")[0]
    reqQntt = mqttMSG.partition("#")[2]
    if reqType == "1":
        now = datetime.now()
        current_year = now.strftime("%Y")
        current_mounth = now.strftime("%m")
        current_day = now.strftime("%d")
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
        print("Current time is: " + current_hour + ":" + current_minute + "  " + current_day + "/" + current_mounth + "/" + current_year + "\n")
        
        data = VRR.tripQuery("20009281", "20018489", current_year, current_mounth, current_day, current_hour, current_minute, reqQntt, 1, ExcludedMeans)
        result = dat.TQ_processQuery(data)
        
        for n in range(0, len(result)):
            result[n].printRoute()
            pubstr = str(n) + "#" + str(reqType) + "#[" +result[n].duration + "][" + result[n].departureTime + "][" + result[n].arrivalTime + "][" + result[n].departureName + "][" + result[n].arrivalName + "]["
            for i in range(0, len(result[n].transportShortnames)):
                pubstr = pubstr + result[n].transportShortnames[i]
                if i < len(result[n].transportShortnames) - 1:
                    pubstr = pubstr + "#"
            pubstr = pubstr + "]"
            client.publish("VRRserver/TX", pubstr, 2)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message= on_message
client.connect("xxxx", 1883, 60)
client.subscribe("VRRserver/RX", 2)
client.loop_forever()
