import spade

from Agents.Manager import Manager
from Agents.Attraction import Attraction
from Agents.Visitor import Visitor
from Agents.Restaurant import Restaurant

from Classes.Coordinates import Coordinates

import time
import json

DOMAIN = "<YOUR_DOMAIN>"
PWORD = "<YOUR_PASSWORD>"

async def main():

    try:
        with open("ParkLayout.json", "r", encoding="utf-8") as file:
            parkLayout = json.load(file)

    except FileNotFoundError:
        print(">> Error: File not found")
    except json.JSONDecodeError:
        print(">> Error: Invalid format")

    manager = Manager("manager@" + DOMAIN, PWORD, parkLayout["eventLocations"])
    await manager.start(auto_register = True)

    attractions = await attractionSetup(parkLayout["attraction"])
    time.sleep(0.2)
    print()
    
    restaurants = await restaurantSetup(parkLayout["restaurant"])
    time.sleep(0.2)
    print()

    visitors = await visitorSetup(10, parkLayout)
    time.sleep(0.2)
    print()


    await spade.wait_until_finished(manager)
    await manager.stop()
    
    #TEMP
    return

    

    # for l in range(10):
    #     addVisitors(visitors, visitors.size())
    

    #TODO: Acrescentar stops dos outros Agents

async def attractionSetup(attLayout):
    attractions = [15]
    j = 1
    for z in range(1,6):
        for _ in range(3):

            i = str(j)
            attraction = Attraction(f"attraction_N{i}-Z{z}@" + DOMAIN, PWORD, f"@attraction_N{i}-Z{z}","manager@" + DOMAIN,
                                             Coordinates(attLayout[i]["xPosition"], attLayout[i]["yPosition"]),
                                             attLayout[i]["ageRestriction"], attLayout[i]["accessability"],
                                             attLayout[i]["adrenalineLevel"], attLayout[i]["minHeight"],
                                             attLayout[i]["capacity"], attLayout[i]["duration"],
                                             attLayout[i]["price"], z, j)
            
            await attraction.start()
            attractions.append(attraction)
            time.sleep(0.1)
            j+=1
    
    return attractions

async def restaurantSetup(restLayout):
    restaurants = [3]
    for j in range(1, 4):
        i = str(j)
        restaurant = Restaurant(f"restaurant_N{i}@" + DOMAIN, PWORD, f"@restaurant_N{i}", "manager@" + DOMAIN,
                                      Coordinates(restLayout[i]["xPosition"], restLayout[i]["yPosition"]),
                                      restLayout[i]["veganFriendly"], restLayout[i]["price"], j)
        await restaurant.start()
        restaurants.append(restaurant)
        time.sleep(0.1)
    
    return restaurants

async def visitorSetup(numVisitors, parkLayout):
    visitors = [numVisitors]
    i = 1
    while i <= numVisitors:
        for _ in range(25):
            if i > numVisitors:
                break
            visitor = Visitor(f"Visitor_N{i}@" + DOMAIN, PWORD, f"@visitor_N{i}", "manager@" + DOMAIN, parkLayout["entrances"], i)
            await visitor.start()
            visitors.append(visitor)
            time.sleep(0.1)
            i+=1
        time.sleep(3)
    return visitors

if __name__ == "__main__":
    spade.run(main())

