#this module will return historical daily information since the entered date

import urllib2
import json

import datetime
from time import strftime

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

plotly.tools.set_credentials_file(username='atomicwest', api_key='EHcu4pz4kxCrlIXDlXPB')

def convertSec(s):
    time = datetime.datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d %H:%M:%S')
    return time


def getLocation():
    
    place = raw_input("Enter a location: \n")
    address = place.replace(' ', '+')
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    keyConcat = "&key="
    key = "AIzaSyC0xRZYhpoV14WiwdKSeWgAJgSCZkMD_g0"

    urlComplete = url + address + keyConcat + key
    
    return [place,urlComplete]


def getLatLong(d):
    jsonData = json.loads(d)
    latlong = jsonData["results"][0]["geometry"]["location"]
    coords = (latlong["lat"], latlong["lng"])
    return coords


def getStartTime():
	yr = raw_input('Enter a start year\n')
	month = raw_input('Enter a start month\n')
	day = raw_input('Enter a start day\n')
	
	startTime = ''
	startTime = '%s-%s-%sT00:00:00' % (yr, month, day)
	dateOnly = "%s-%s-%s" % (yr,month,day)
	return (dateOnly,startTime)


def getEndTime():
	yr = raw_input('Enter a end year\n')
	month = raw_input('Enter a end month\n')
	day = raw_input('Enter a end day\n')
	
	startTime = ''
	startTime = '%s-%s-%sT00:00:00' % (yr, month, day)
	dateOnly = "%s-%s-%s" % (yr,month,day)
	return (dateOnly,startTime)


def getWeather(lat, lng, startTime):
	url = "https://api.darksky.net/forecast/"
	sk = "6827351e56557cfc282c0cadb4e3d4e6"

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
    
    while (int(startyear) < int(endyear)):
        startyear = str(int(startyear) + 1)
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

            
            
            if int(startmonth)+1 < 10:
                startmonth = '0' + str(int(startmonth)+1)
            else:
                startmonth = str(int(startmonth)+1)
                
            if int(startyear)==int(endyear) and int(startmonth) > int(endmonth):
                break
        startmonth = '01'
        
    return [highTempSet, lowTempSet, daySet, filename]


def graphHistorical(historical):
    highTempSet = historical[0]
    lowTempSet = historical[1]
    daySet = historical[2]
    place_range = historical[3]
    
    line0 = go.Scatter(
        x = daySet,
        y = highTempSet,
        name = 'Highs',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )
    
    
    line1 = go.Scatter(
        x = daySet,
        y = lowTempSet,
        name = 'Lows',
        line = dict(
            color = ('rgb(0, 35, 178)'),
            width = 4)
    )
    
    data = [line0, line1]
    
    # Edit the layout
    layout = dict(title = "Historical High and Low  Temperatures for " + place_range,
                  xaxis = dict(title = 'Days'),
                  yaxis = dict(title = 'Temperature (degrees F)'),
                  )
    
    fig = dict(data=data, layout=layout)
    # py.iplot(fig, filename='styled-line')
    filename = "%s.png" % place_range
    py.image.save_as(fig, filename)




def main():
    #open URL
    loc = getLocation()
    webURL = urllib2.urlopen(loc[1])
    placename = loc[0]
    print webURL.getcode()
	
	#read URL on success
    if (webURL.getcode() == 200):
		data = webURL.read()
		l = getLatLong(data)
		sTime = getStartTime()
		eTime = getEndTime()
		startDateOnly = sTime[0]
		startTimeString = sTime[1]
		endDateOnly = eTime[0]
		endTimeString = eTime[1]
		#weather = getWeather(l[0], l[1], sTime)
		
        #graphHistorical will make many calls to getWeather
		historical = getHistorical(placename,l[0],l[1],startDateOnly, startTimeString, endDateOnly, endTimeString)
# 		print historical[0]
# 		print historical[1]
# 		print historical[2]
		graphHistorical(historical)
		print "--------------"

		
if __name__ == "__main__":
    main()
    
    