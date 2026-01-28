import spade 
from spade.agent import Agent

from Behaviours.Subscribe import SubscribeBH

from Classes.Coordinates import Coordinates

import random
import time
import asyncio

class Attraction(Agent):

    def __init__(self, jid, password, agentName:str, managerJID, position:Coordinates, ageRestriction:int, accessability:bool, 
                 adrenalineLevel:int, minHeight:float, capacity:int, duration:int, price:float, zone:int, num:int):
        super().__init__(jid,password)
        self.agentName = agentName
        self.managerJID = managerJID
        self.position = position
        self.ageRestriction = ageRestriction
        self.accessability = accessability
        self.adrenalineLevel = adrenalineLevel
        self.minHeight = minHeight
        self.capacity = capacity
        self.duration = duration
        self.price = price

        self.zone = zone
        self.num = num

        self.queue = []
        self.queue_lock = asyncio.Lock()

        self.profit = 0.0

        self.imAvailable = True
        self.imAvailable_lock = asyncio.Lock()

    async def setup (self):

        print(f">> Attraction_N{self.num}-Z{self.zone} started")

        sBH = SubscribeBH()
        self.add_behaviour(sBH)