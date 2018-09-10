import serial
import time
import xml.etree.cElementTree as ET
import urllib2

gps = serial.Serial('com4',baudrate=9600,timeout=1)
root = ET.Element("fire")
doc = ET.SubElement(root,"location")

URL = "http://gis1.hartford.gov:6180/geoevent/rest/receiver/fire-laptop-xml-in"

while True:
    if gps.isOpen() == False:
        gps.open()
    line = gps.readline()
    data = line.split(",")
    if data[0] == "$GPGGA":
        if data[6] >= "1":
            ET.SubElement(doc, "ID").text = "Laptop 1"
            ET.SubElement(doc, "Time").text = data[1]
            ET.SubElement(doc, "Latitude").text = data[2]
            ET.SubElement(doc, "Longitude").text = data[4]
            ET.SubElement(doc, "Quality").text = data[6]
            ET.SubElement(doc, "Satellites").text = data[7]
            ET.SubElement(doc, "HDOP").text = data[8]
            tree = ET.tostring(root)

            req = urllib2.Request(url=URL, data=tree, headers={'Content-Type':'application/xml'})
            urllib2.urlopen(req)
            #print tree
            tree = ""
            del tree
            gps.close()
            time.sleep(5)
