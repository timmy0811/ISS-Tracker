# ISS-Tracker

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#information">Information Explanation</a>
    </li>
    <li><a href="#installation-setup">Installation / Setup</a></li>
    <li><a href="#win-executable">ISS-Tracker Executable</a></li>
    <li><a href="#further-plans">Further Plans</a></li>
    <li><a href="#open-source">open Source</a></li>
    <li><a href="#source-code">Source code</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is my first complete Python programm. It is API based and uses NASA's Open-Notify API to print the ISS-data live to the console. Furthermore it renderes a map based on user inputs and the API-data to the current project folder. The render frequency is set also by the users input with at least 1 second delay each period the data gets updated

<!-- INFORMATION  -->
## What does the Information mean?
First of all the programm will ask you some questions how you want the programm to operate. 

### Folowing inputs are valid:
  * `refresh-rate` -> Time between each period of retreiving new data in seconds, simple integer. Recommended is 3-10
  * `Draw map?` -> Enter `y` or `n` if the generated map shall be displayed to screen after each period. The programm will pause when open
  * `your location` -> Enter your location as simple string. Nearest bigger City is recommended
  * `map style` -> Different colorings and appearances of the map are available:
    * `2-Color` colors the water light blue and the land lime
    * `Bluemarble` draws an image of the earth on top of the map
    * `Black-White` colors the map in gray and white. may take a while to load.
    * `Shaded Relief` displays the relief in certain areas.

### The console log explained: 
  * The `Past Loc. in Bytes` print shows the current size of the list that saves past ISS-Locations to plot it's orbit to the map. It is rather used to debug.
  * The `Latitude` and `Longitude` print shows the current latitude and longitude of the ISS in degrees.
  * The `Location` print gives you the current adress of the place the ISS is passing over. Output is always in native language.
  * The `Translation` simply prints out the english Translation of the current location.
  * The `People on ISS` log shows the amount of people which are right now on it. Moreover `Names` gives you there names.
  * Finally the `Next pass` and its `Duration` predicts the next pass over your given location. `Next pass` gives you the date and `Duration` the time it is possible to see the ISS above you. (up to 10° off)

Once the programm is running, it can be plotting points over hours and days, showing the ISS's orbit.

<!-- INSTALLATION STUP -->
## Installation / Setup

When running as Python code you will need Python installed including following modules using `pip` or `conda`
  * `requests`
  * `json`
  * `numpy`
  * `matplotlib`
  * `datetime`
  * `basemap`
  * `geopy`
  * `googletrans`
  
The module get imported as following:
### imports
```python
import requests, json, time, os, sys

import numpy as np
import matplotlib.pyplot as plot

from pympler.asizeof import asizeof
from datetime import datetime
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from googletrans import Translator
```



<!-- WIN EXECUTABLE -->
## ISS-Tracker Executable

The Project is also available as an Executable for Windows. This means that no pip- / or conda installations are necessary. All modules are allready included.
It can be downloaded here.

  ### [ISS-Tracker Executable](https://www.mediafire.com/file/16aj49ikilh8ock/ISS-TrackerExecutable.rar/file)

<!-- FURTHER PLANS -->
## Further Plans

### Further plans of improving and axpanding the project:
  * Building a graphical UI for better Overview and consitency
  * Predict the ISS's orbit and plotting it to map 
  * Designing the programm more lightweight 

<!-- OPEN SOURCE -->
## open Source

Feel free to use the code as a whole or only parts of it. I make those projects to learn software development and have fun :-)

IG: [timmy0811_](https://www.instagram.com/timmy0811_/)

<!-- SOURCE CODE -->
## Source Code

```python
#ISS-Tracker by timmy0811   -   API based   1.1

#Imports
import requests, json, time, os, sys, pygame

import numpy as np
import matplotlib.pyplot as plot

from pympler.asizeof import asizeof
from datetime import datetime
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from googletrans import Translator

#Function declaration
def useGUI():
    GUI = input("Use a graphical GUI? (y/n): ")
    if(GUI == "y"):
        return True
    else: return False

def mapTypes(): #Choose map coloring 
    mapVariant = input('Chose a map type:   1) 2-Color      2) Bluemarble       3) Black-White      4) Shaded-Relief        ')
    return int(mapVariant)

def setup(): #Select refresh rate | Interval between several periods
    refresh_rate = input("Select refresh-rate in seconds: ")
    return int(refresh_rate)

def drawMapDes(): #Choose of drawing map to screen after each period
    doDraw = input("Draw map when generated? (y/n): ")
    if(doDraw == "y"):
        return True
    else: return False

def jsonprint(obj): #Print .json as string - currently not used
    text = json.dumps(obj, sort_keys = True, indent = 4)
    print(text)

def getadress(latitude, longitude, geolocater): #Converting Iss-location to adress
    location = geolocator.reverse(latitude + "," + longitude)
    return location

def distanceAB(home_latitute, home_longitude, latitute, longitude): #Get distance from to given locations
    home = (home_latitute, home_longitude)
    iss = (latitute, longitude)

    distance = geodesic(home, iss).miles
    return distance

def homelocationInput(geolocator): #Input for adress and converting it to long and lat
    home_location = geolocator.geocode(input("Enter your location: "))
    return(home_location)

def translate(srcT): #Using translate to detect adress language and translating it to english
    trans = Translator()
    t = trans.translate(srcT, src= 'auto', dest='en')
    return t.text

def writePep(responsePep, pepjson): #Extracting people info from json
    pepName = []
    for k in range(6):
        pepName.append(None) 
        pepName[k] = (pepjson['people'] [k])['name']
    return pepName

def drawData(iss_latitude, iss_longitude, home_location_lat, home_location_lon, past_locationy, past_locationx, m, fig): #Draw locations to pre rendered map and save figure as file
    iss_marker = m.scatter(float(iss_longitude), float(iss_latitude), latlon = True, s = 45, c = 'red', marker = '*', zorder = 4)
    iss_surr = m.scatter(float(iss_longitude), float(iss_latitude), latlon = True, c = 'teal', s = 10500, alpha = 0.2, edgecolor = 'darkslategray', linewidth = 1,  zorder = 2)
    m.scatter(float(home_location.longitude), float(home_location.latitude), latlon = True, edgecolor = 'maroon', linewidth = 1, c = 'fuchsia', marker = '^', zorder= 3)

    #for x in range(len(past_locationy)):
    #m.scatter(float(past_locationx[x]), float(past_locationy[x]), latlon = True, c = 'orange', s = 10, zorder = 3, alpha = 0.5)    not used drawing routine
    m.scatter(float(iss_longitude), float(iss_latitude), latlon = True, c = 'orange', s = 10, zorder = 3, alpha = 0.5)

    output_file = 'latest_map.png'
    plot.savefig(output_file, bbox_inches = 'tight', dpi = 150)

    if(doDraw == True):
        plot.show()
    
    iss_marker.remove()     #removing existing marker on map
    iss_surr.remove()

def printLogo(): #Printing Logo in upper console
    print(" _____ _____ _____      ___________  ___  _____ _   _____________")
    print("|_   _/  ___/  ___|    |_   _| ___ \/ _ \/  __ | | / |  ___| ___ \ ")
    print("  | | \ `--.\ `--. ______| | | |_/ / /_\ | /  \| |/ /| |__ | |_/ /")
    print("  | |  `--. \`--. |______| | |    /|  _  | |   |    \|  __||    / ")
    print(" _| |_/\__/ /\__/ /      | | | |\ \| | | | \__/| |\  | |___| |\ \ ")
    print(" \___/\____/\____/       \_/ \_| \_\_| |_/\____\_| \_\____/\_| \_|")
    print("___________________________________________________________________")

#Setup and user-input


bg = pygame.image.load("F:\Desktop\Folders\Programming\Python\ISS-Tracker\BgImage.jpg")

printLogo()
doDraw = drawMapDes()
interface = useGUI()
if (interface == False): refresh_rate = setup()

if (interface):
    pygame.init()
    screen = pygame.display.set_mode((900, 400))
    clock = pygame.time.Clock()
    pygame.display.set_caption('ISS-Tracker     by timmy0811')

    font = pygame.font.SysFont(None, 30)

running = True

geolocator = Nominatim(user_agent="Application")
home_location = homelocationInput(geolocator)

n = 0
past_locationy = []     #Past locations of ISS get saved in y and x lists
past_locationx = []

responsePep = requests.get("http://api.open-notify.org/astros.json")    #Getting info about people in Space
pepjson = responsePep.json()
numberPep = pepjson['number']

parameters = {                          #Parameters for API request
    "lat": home_location.latitude,
    "lon": home_location.longitude,
    "n": 4
}

#Pre-Drawing the map based on user-input
draw_map = 1
main_count = 0

fig = plot.figure(figsize = (12,9))

m = Basemap(projection='mill', llcrnrlat= -90, urcrnrlat= 90, llcrnrlon= -180, urcrnrlon= 180, resolution= 'c')

m.drawcountries()
m.drawcoastlines()

user_des = mapTypes()

if(user_des == 1):
    m.drawmapboundary(fill_color = 'aqua')
    m.fillcontinents(color='lightgreen', lake_color= 'aqua', alpha= 1)
elif(user_des == 2):
    m.bluemarble(scale = 0.2)
elif(user_des == 3):
    m.drawlsmask()
elif(user_des == 4):
    m.shadedrelief(scale = 0.07)
else: sys.exit()

m.drawparallels(np.arange(-90,90,10), labels= [True, False, False, False])
m.drawmeridians(np.arange(-180,180, 30), labels= [False, False, False, True])

plot.title('Current ISS-Location', fontsize = 20)

#Main cycle
while(True):   
    while (running):
        if(interface):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False

        if(main_count == 10 or main_count == 0):
            main_count = 1

            os.system("cls")
            printLogo()

            response = requests.get("http://api.open-notify.org/iss-now.json")

            responsePass = requests.get("http://api.open-notify.org/iss-pass.json", params = parameters)
            passjson = responsePass.json()

            text = response.json()
            position = text["iss_position"]

            iss_latitude = position['latitude']
            iss_longitude = position['longitude']

            past_locationy.append(None)
            past_locationx.append(None)

            past_locationy[n] = iss_latitude
            past_locationx[n] = iss_longitude
            n += 1
     
            #print("Latitude History:     " + str(past_locationy))
            #print("Longitude History:    " + str(past_locationx))

            #Print console log
            if(interface == False):
                print("Past Loc. in Bytes:   " + str(asizeof(past_locationy) + asizeof(past_locationx)))

                print("Latitude:             " + iss_latitude + "°")
                print("Longitude:            " + iss_longitude + "°")
                adress = getadress(iss_latitude, iss_longitude, geolocator)
                print("Location:             " + str(adress))
                print("Translation:          " + translate(adress))
                print("Distance to you:      " + str(int(distanceAB(home_location.latitude, home_location.longitude, iss_latitude, iss_longitude) * 1.609344)) + " Kilometers")
                print("---------------------------------------")
                print("People on ISS:        " + str(numberPep))
                print("Names:                " + str(writePep(responsePep, pepjson)))
                print("---------------------------------------")
                print("Next pass:            " + str(datetime.fromtimestamp((passjson['response'])[0]['risetime'])))
                print("Duration:             " + str((passjson['response'])[0]['duration']) + " seconds")
                print(" ")
                print("Second pass:          " + str(datetime.fromtimestamp((passjson['response'])[1]['risetime'])))
                print("Duration:             " + str((passjson['response'])[1]['duration']) + " seconds")
                print(" ")
                print("Third pass:           " + str(datetime.fromtimestamp((passjson['response'])[2]['risetime'])))
                print("Duration:             " + str((passjson['response'])[2]['duration']) + " seconds")
            else:
                screen.fill((92, 244, 255))
                screen.blit(bg, (0,0))

                #GUI-Text
                latImg = font.render("Latitude:         " + str(iss_latitude) + "°", True, (255, 255, 255))
                lonImg = font.render("Longitude:          " + str(iss_longitude) + "°", True, (255, 255, 255)) 
                adress = getadress(iss_latitude, iss_longitude, geolocator)
                locImg = font.render("Location:         " + str(adress), True, (255, 255, 255))
                transImg = font.render("Translation:        " + translate(adress), True, (255, 255, 255))
                distImg = font.render("Distance to you:    " + str(int(distanceAB(home_location.latitude, home_location.longitude, iss_latitude, iss_longitude) * 1.609344)) + " Kilometers", True, (255, 255, 255))

                pepImg = font.render("People on ISS:    " + str(numberPep), True, (255, 255, 255))
                nameImg = font.render("Names:            " + str(writePep(responsePep, pepjson)), True, (255, 255, 255))

                pass1Img = font.render("Next pass:        " + str(datetime.fromtimestamp((passjson['response'])[0]['risetime'])), True, (255, 255, 255))
                dur1Img = font.render("Duration:         " + str((passjson['response'])[0]['duration']) + " seconds", True, (255, 255, 255))

                pass2Img = font.render("Second pass:      " + str(datetime.fromtimestamp((passjson['response'])[1]['risetime'])), True, (255, 255, 255))
                dur2Img = font.render("Duration:         " + str((passjson['response'])[1]['duration']) + " seconds", True, (255, 255, 255))

                pass3Img = font.render("Third pass:       " + str(datetime.fromtimestamp((passjson['response'])[2]['risetime'])), True, (255, 255, 255))
                dur3Img = font.render("Duration:         " + str((passjson['response'])[2]['duration']) + " seconds", True, (255, 255, 255))

                textImg = [latImg, lonImg, locImg, transImg, distImg, pepImg, nameImg, pass1Img, dur1Img, pass2Img, dur2Img, pass3Img, dur3Img]

            #Drawing location to rendered map
            drawData(iss_latitude, iss_longitude, home_location.latitude, home_location.longitude, past_locationy, past_locationx, m, fig)
            
            if(interface == False):
                #Time-delay - at least 1 sec if user-input is 0
                time.sleep(refresh_rate)
                time.sleep(1)
            
        #draw text to screen
        if(interface):
            for image in range(len(textImg)):
                screen.blit(textImg[image], (25, 25 + image * 25))
                pygame.display.flip()
                clock.tick(5)
        
        main_count += 1
        
    if(interface): pygame.quit()

```

