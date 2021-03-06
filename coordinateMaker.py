import json
import csv
from shapely.geometry import shape, Polygon, Point

#Opening GeoJSON file
with open('Neighbourhoods.geojson', 'r') as f:
    js = json.load(f)

#List to store coordinates
coordinateList = []

#Opening coordinates.csv file
with open('coordinates.csv', 'r') as f2:
    reader = csv.reader(f2, skipinitialspace=True)
    for row in reader:
        
        coordinateList.append(row)

#Remove whitespace
coordinateList = list(filter(None,coordinateList))

#Reverse all elements and convert to floats
for i in range(len(coordinateList)):
    coordinateList[i] = list(map(float,reversed(coordinateList[i])))

#Convert all coordinates to shapely points
for i in range(len(coordinateList)):
    coordinateList[i] = Point(coordinateList[i][0],coordinateList[i][1])

#List to store area codes with number of coffee shops in each neighbourhood
areaCodewithNumCoord = []

#initialize array values to store area code and num of locations
for feature in js['features']:
    areaCodewithNumCoord.append([feature['properties']['AREA_SHORT_CODE'],0])

#Iterates through GeoJSON file
for feature in js['features']:

    polygon = shape(feature['geometry'])
    
    for i in range(len(coordinateList)):
        #If polygon contains coffee shop cooridinate from api call, add, otherwise discard
        if polygon.contains(coordinateList[i]):
            #Iterate through area code and tally array, if found add to tally
            for j in range(len(areaCodewithNumCoord)):                
                if areaCodewithNumCoord[j][0]==feature['properties']['AREA_SHORT_CODE']:
                    areaCodewithNumCoord[j][1]=areaCodewithNumCoord[j][1]+1

areaCodewithNumCoord.insert(0,['Neighbourhood_ID','Number_CoffeeShop'])

#Cleaned data, will write to areaCodeNum with num of starbucks file
with open('areaCodeNum.csv', 'w', newline="") as f3:
    writer = csv.writer(f3)
    writer.writerows(areaCodewithNumCoord)
