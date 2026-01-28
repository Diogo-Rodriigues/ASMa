import spade 
from spade.agent import Agent

from Behaviours.Subscribe import SubscribeBH
from Classes.Coordinates import Coordinates

import random

class Restaurant(Agent):

    def __init__(self, jid, password, agentName:str, managerJID:str, position:Coordinates, veganFriendly:bool, price:float, num:int):
        super().__init__(jid,password)
        self.agentName = agentName
        self.managerJID = managerJID
        self.position = position 
        self.veganFriendly = veganFriendly
        self.price = price
        
        self.num = num

        self.profit = 0


    async def setup (self):

        print(f">> Restaurant_N{self.num} started")

        sBH = SubscribeBH()
        self.add_behaviour(sBH)

