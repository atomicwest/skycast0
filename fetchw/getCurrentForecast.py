import urllib2
import json

import datetime
from time import strftime


def convertSec(s):
    time = datetime.datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d %H:%M:%S')
    return time


def getLocation(place):
    
    address = place.replace(' ', '+')
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    # address = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    # address = "Lisbon"
    keyConcat = "&key="
    key = "YOUR_KEY"

    urlComplete = url + address + keyConcat + key
    
    return [place,urlComplete]


def getLatLong(d):
    jsonData = json.loads(d)
    latlong = jsonData["results"][0]["geometry"]["location"]
    coords = (latlong["lat"], latlong["lng"])
    return coords


def getWeather(lat, lng):
	url = "https://api.darksky.net/forecast/"
	sk = "YOUR_KEY"
	urlcomplete =  url + sk + "/" + str(lat) + "," + str(lng)
	
	#open URL 
	webURL = urllib2.urlopen(urlcomplete)
	print webURL.getcode()
	
	#read URL on success
	
	if (webURL.getcode() == 200):
		data = webURL.read()
		jsonData = json.loads(data)
		return jsonData
	else:
		print "Error: %d" % webURL.getcode()
		return None


def formatCurrent(loc,diction):
    print "Current weather for %s" % loc
    print '-'*20
    
    unit = dict()
    
    if diction['flags']['units']=='us':
        unit['temp'] = 'F'
    else:
        unit['temp'] = 'C'
    
    data = {}
    # alertlinks = []
    alerts = []
    if "alerts" in diction.keys():
        print "Weather Alerts: "
        for a in diction['alerts']:
            alert = {}
            
            for k,v in a.items():
                if k in ['time', 'expires']:
                    print "%s : %s" % (k.title(), convertSec(v))
                    alert[k] = convertSec(v)
                elif k=='uri':
                    # alertlinks.append(v)
                    print "%s : %s" % (k.title(), v)
                    alert[k] = v
                elif k=='regions':
                    print "Affected Regions:"
                    for el in v:
                        print el
                    alert[k] = v
                elif k=='description':
                    alert[k] = v
                else:
                    print "%s : %s" % (k.title(), v)
        alerts.append(alert)    
    print '-'*20
    
    data["alerts"] = alerts
    
    for k,v in diction["currently"].items():
        if k=='time':
            print "Local Time : %s" % ( convertSec(v))
            fulltime = convertSec(v)
            data['date'] = fulltime[0:10]
            data['time'] = fulltime[11:]
        if k=='icon':
            data[k] = v
        if k=='temperature':
            data[k] = str(v) + ' ' + unit['temp']
        if k=='humidity':
            data[k] = str(v*100)+"%"
        if k=='precipProbability':
            data[k] = str(v*100)+"%"
        if k=='summary':
            data[k] = v
        else:
            print "%s : %s" % (k.title(), v)
    
    return data
    
    

def formatForecast(loc,diction):
    print "Forecast for %s" % loc
    
    unit = dict()
    
    if diction['flags']['units']=='us':
        unit['temp'] = 'F'
    else:
        unit['temp'] = 'C'
    
    forecast = []
    
    for n in diction["daily"]["data"]:
        day = {}
        if "time" in n.keys():
            day["date"] = convertSec(n['time']).split(' ')[0]
            print "Date: %s" % convertSec(n['time']).split(' ')[0]
        if "icon" in n.keys():
            day["icon"] = n['icon']
            print n['icon']
        if "summary" in n.keys():
            day["summary"] = n['summary']
            print "Summary: %s" % n['summary']
        if "temperatureMax" in n.keys():
            day["high"] = "%s %s" % (n['temperatureMax'], unit['temp'])
            print "High: %s %s" % (n['temperatureMax'], unit['temp'])
        if "temperatureMin" in n.keys():
            day["low"] = "%s %s" % (n['temperatureMin'], unit['temp'])
            print "Low: %s %s" % (n['temperatureMin'], unit['temp'])
        if "precipProbability" in n.keys():
            day["precip"] = str(n['precipProbability']*100)+"%"
            print "Chance of Precipitation: %s" % str(n['precipProbability']*100)+"%"
        if "humidity" in n.keys():
            day["humidity"] = str(n['humidity']*100)+"%"
            print "Humidity: %s" % str(n['humidity']*100)+"%"
        
        forecast.append(day)
        
    # print diction['flags']
    return forecast
    

def apiCurrentHandler(query):
    #open URL
    loc = getLocation(query)
    webURL = urllib2.urlopen(loc[1])
    print webURL.getcode()
	
	#read URL on success
    if (webURL.getcode() == 200):
        data = webURL.read()
        l = getLatLong(data)
        print l
        weather = getWeather(l[0], l[1])
        current = formatCurrent(loc[0], weather)
        print "--------------"
        forecast = formatForecast(loc[0], weather)
    
    return {"inputQ":query, "current":current, "forecast":forecast}
		
    
    