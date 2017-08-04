#this module will return historical daily information since the entered date

import urllib2
import json

import datetime
from time import strftime

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

plotly.tools.set_credentials_file(username='USERNAME', api_key='YOUR_KEY')

def convertSec(s):
    time = datetime.datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d %H:%M:%S')
    return time


def getLocation(place):
    
    address = place.replace(' ', '+')
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    keyConcat = "&key="
    key = "YOUR_KEY"

    urlComplete = url + address + keyConcat + key
    
    return [place,urlComplete]


def getLatLong(d):
    jsonData = json.loads(d)
    latlong = jsonData["results"][0]["geometry"]["location"]
    coords = (latlong["lat"], latlong["lng"])
    return coords


def getWeather(lat, lng, startTime):
	url = "https://api.darksky.net/forecast/"
	sk = "YOUR_KEY"

# 	startTime = startTime.replace(' ','')
	urlcomplete =  url + sk + "/" + str(lat) + "," + str(lng)
	urlcomplete += ',' + startTime
	
	#open URL 
	webURL = urllib2.urlopen(urlcomplete)
# 	print webURL.getcode()
	
	#read URL on success
	
	if (webURL.getcode() == 200):
		data = webURL.read()
		jsonData = json.loads(data)
		return (jsonData,startTime.replace('T',' '))
	else:
		print "Error: %d" % webURL.getcode()
		return None


def getHistorical(loc, lat, lng, starttime, startfull ,endtime, endfull):
    
    #get one data point from each month in a year
    
    print "Historical weather for %s from %s to %s" % (loc, starttime, endtime)
    filename = "%s_%s_%s" % (loc, starttime, endtime)
    startyear = starttime[0:4]
    endyear = endtime[0:4]
    
    startmonth = starttime[5:7]
    startday = starttime[8:11]
    
    endmonth = endtime[5:7]
    endday = endtime[8:11]
    
    highTempSet = []
    lowTempSet = []
    daySet = []
    
    pressureSet = []
    daySetPressure = []
    
    while (int(startyear) < int(endyear)+1):
        
        while(int(startmonth) < 13):
        
            nextTime = '%s-%s-%sT00:00:00' % (startyear, startmonth, startday)
            
            #save data from getweather request
            print nextTime
            nextPoint = getWeather(lat, lng, nextTime)[0]
            
            if 'daily' in nextPoint.keys():
                if ('temperatureMax' in nextPoint['daily']['data'][0].keys()) and 'temperatureMin' in nextPoint['daily']['data'][0].keys():
                    highTempSet.append(nextPoint['daily']['data'][0]['temperatureMax'])
                    lowTempSet.append(nextPoint['daily']['data'][0]['temperatureMin'])
                    daySet.append(nextTime[0:10])
                    
                if ('pressure' in nextPoint['daily']['data'][0]):
                    pressureSet.append(nextPoint['daily']['data'][0]['pressure'])
                    daySetPressure.append(nextTime[0:10])
                
            
            if int(startmonth)+1 < 10:
                startmonth = '0' + str(int(startmonth)+1)
            else:
                startmonth = str(int(startmonth)+1)
                
            if int(startyear)==int(endyear) and int(startmonth) > int(endmonth):
                break
        startmonth = '01'
        startyear = str(int(startyear) + 1)
        
    return [highTempSet, lowTempSet, daySet, filename, pressureSet, daySetPressure]


def graphHistorical(historical):
    highTempSet = historical[0]
    lowTempSet = historical[1]
    daySet = historical[2]
    place_range = historical[3]
    
    pressureSet = historical[4]
    daySetPressure = historical[5]
    
    
    lineHighTemp = go.Scatter(
        x = daySet,
        y = highTempSet,
        name = 'Highs',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )
    
    
    lineLowTemp = go.Scatter(
        x = daySet,
        y = lowTempSet,
        name = 'Lows',
        line = dict(
            color = ('rgb(0, 35, 178)'),
            width = 4)
    )
    
    
    linePressure = go.Scatter(
        x = daySetPressure,
        y = pressureSet,
        name = 'Sea-Level Air Pressure',
        line = dict(
            color = ('rgb(150, 227, 255)'),
            width = 4)
    )
    
    
    dataT = [lineHighTemp, lineLowTemp]
    dataP = [linePressure]
    
    # Edit the layout
    layoutT = dict(title = "Historical High and Low  Temperatures for " + place_range,
                  xaxis = dict(title = 'Time'),
                  yaxis = dict(title = 'Temperature (degrees F)'),
                  )
    
    layoutP = dict(title = "Historical Sea-Level Air Pressure for " + place_range,
                  xaxis = dict(title = 'Time'),
                  yaxis = dict(title = 'millibars'),
                  )
    
    figT = dict(data=dataT, layout=layoutT)
    figP = dict(data=dataP, layout=layoutP)
    # py.iplot(fig, filename='styled-line')
    filenameT = "%sTemp.png" % place_range
    filenameP = "%sPres.png" % place_range
    # py.image.save_as(figT, filenameT)
    # py.image.save_as(figP, filenameP)
    
    # dataTd = go.Data(dataT)
    # dataPd = go.Data(dataP)
    urlT = py.plot(figT, filename = filenameT, auto_open=False)
    urlP = py.plot(figP, filename = filenameP, auto_open=False)
    
    
    return {"tempUrl": urlT, "presUrl" : urlP}


def padder(snum):
    if (int(snum) < 10) and len(snum)<2:
        return '0'+snum
    return snum

def apiTimeMachineHandler(query):
    #open URL
    loc = getLocation(query['location'])
    webURL = urllib2.urlopen(loc[1])
    placename = loc[0]
    print webURL.getcode()
	
	#read URL on success
    if (webURL.getcode() == 200):
		data = webURL.read()
		l = getLatLong(data)
		startM = query['startmonth']
		startD = query['startday']
		endM = query['endmonth']
		endD = query['endday']
        
		startDateOnly = '%s-%s-%s' % (query['startyear'], padder(startM), padder(startD))
		startTimeString = '00:00:00'
		endDateOnly = '%s-%s-%s' % (query['endyear'], padder(endM), padder(endD))
		endTimeString = '00:00:00'
		
        #getHistorical will make a call to getWeather per month in the historical range
        #graphHistorical should actuall give the plotly urls of the graphs
		historical = getHistorical(placename,l[0],l[1],startDateOnly, startTimeString, endDateOnly, endTimeString)
		urls = graphHistorical(historical)
		
    return urls
		

    