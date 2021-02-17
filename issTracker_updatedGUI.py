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


    

