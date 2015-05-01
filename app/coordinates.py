# ===========================================================================
# +++coordinates.py+++|
# ____________________|
#
# Chris Palmer
# Badge Tracking App
# ===========================================================================
import sys
import math

#input is a list of data records. Basically the JSON from Padfoot
#converted into a list of dictionaries, minus the extra stuff we 
#don't need
'''
essentially, this:
{
	"myID" : "123456789",
	"timeStamp" : 1428591816262,
	"trimmedResults" : [ {
		"BSSID" : "f8:e4:fb:2e:29:84",
		"SSID" : "393B6",
		"frequency" : 2412,
		"level" : -54
	}, {
		"BSSID" : "18:1b:eb:0b:05:7a",
		"SSID" : "RVM23",
		"frequency" : 2437,
		"level" : -50
	}, {

		"BSSID" : "18:1b:eb:82:02:fa",
		"SSID" : "Justin28",
		"frequency" : 2437,
		"level" : -95
	} ]
}

needs to become this: 

[ dictA,dictB,dictC ] 

where

dictA = [	"BSSID" -> "f8:e4:fb:2e:29:84","SSID" -> "393B6",
		"frequency" -> 2412,"level" -> -54]
and so on...

'''
def coordinates(input):
	routers = initRouters()
	arr = findRouters(input,routers)
	y = calcY(arr)
	x = calcX(y)
	if(y==-1):
		y=0
	retval = [x,y]
	return (retval)
	
def calcX(y):
	if(y==-1):
		return 0
	if(y>138):
		return 73
	elif(y<129):
		return 24
	else:
		return 41
		
def yHelper(arr):
	if(len(arr)==0):
		return -1
	closest = arr.pop(0)
	y = closest.y
	seen =0
	exclusive = 0
	for r in arr:
		pos = r.y
		rad = r.radius
		if(rad>100 and seen>=1):
			break
		elif(rad<=100):
			seen+=1
			if(exclusive==0):
				exclusive=rad
			elif(exclusive*2<rad):
				break
		if(pos<y):
			y=(y+rad+pos)/2
		else:
			y=(y-rad+pos)/2
	pinpoint = 0
	if(closest.radius>10):
		pinpoint = closest.radius
	else:
		pinpoint = closest.radius*2
	if(((closest.y+pinpoint)>y) and (closest.y-pinpoint<y)):
		return int(y)
	elif((closest.y+pinpoint)<y):
		return int(closest.y+pinpoint)
	else:
		return int(closest.y-pinpoint)
		
		
		
def calcY(arr):
	if not arr:
		return -1
	closest = []
	for router in arr:
		if(router.radius<=10):
			closest.append(router)
	if (len(closest)>1):
		return yHelper(closest)
	return yHelper(arr)
	
def findRouters(input,routers):
	arr = []
	for data in input:
		for router in routers:
			if(router.MAC==data["BSSID"]):
				distance = calcDistance(data["frequency"],data["level"])
				if (distance<50):
					distance*=router.multiplier
				router.radius = distance
				arr.append(router)
	arr.sort(key=lambda r: r.radius)
	return arr

def calcDistance(freqInMHz,signalLevelInDb):
	exp = (27.55 - (20 * math.log10(freqInMHz)) + math.fabs(signalLevelInDb)) / 20.0
	return 3.28 * math.pow(10.0, exp);

def initRouters():
	arr = []
	arr.append(Router(69,263,"50:17:ff:c8:9c:0c",1.5))
	arr.append(Router(73,308,"3c:ce:73:39:a2:0c",1))
	arr.append(Router(77,420,"dc:a5:f4:cc:a2:6e",2))
	arr.append(Router(69,472,"3c:ce:73:39:a2:8f",3))
	arr.append(Router(0,0,"cc:d5:39:ba:c4:3c",1))
	arr.append(Router(24,89,"3c:ce:73:39:53:6c",1))
	arr.append(Router(41,134,"58:97:1e:b3:f3:6c",1))
	return arr

class Router:
	def __init__(self, x,y,MAC,multiplier):
		self.x=x
		self.y=y
		self.radius = 0
		self.MAC = MAC
		self.multiplier = multiplier


