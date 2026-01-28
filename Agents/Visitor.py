import spade 
from spade.agent import Agent

from Behaviours.Subscribe import SubscribeBH

from Classes.Coordinates import Coordinates

import random
import asyncio
import math

class Visitor(Agent):

    def __init__(self, jid, password, agentName:str, managerJID:str, entrances, num:int):
        super().__init__(jid, password)
        self.agentName = agentName
        self.managerJID = managerJID
        self.isAdult = self.chanceRandom(0.6)
        self.height = self.heightRandom(self.isAdult)
        self.patienceLevel = random.randrange(1,4) 
        self.adrenalineLevel = random.randrange(1,4)
        self.isVegan = self.chanceRandom(0.3)
        self.specialNeeds = self.chanceRandom(0.15)
        self.budget = self.budgetRandom(100, self.isAdult)

        [x , y] = random.choice(entrances)
        self.position = Coordinates(x, y)

        self.num = num

        self.hunger = random.randrange(0, 21)
        # self.hunger = 0 # Temporário para testar attractions
        self.enjoyment = random.randrange(75, 101)

        self.alrdVisited = {}
        self.patienceDict = {1 : [(0, 15), (16, 29), 30],
                             2 : [(0, 20), (21, 44), 45],
                             3 : [(0, 30), (31, 49), 50],}

    async def setup (self):

        print(f">> Visitor_{self.num} started")

        # await asyncio.sleep(1)

        sBH = SubscribeBH()
        self.add_behaviour(sBH)

    def heightRandom(self, isAdult):
        if isAdult:
            return round(random.uniform(1.5, 2.1), 2)
        return round(random.uniform(1.0, 1.7), 2)
    
    def chanceRandom(self, prob):
        chance = random.random()
        return chance <= prob 
    
    # para base = 100, qualquer visitante terá entre 100 e 200 $
    def budgetRandom(self, base, isAdult): 
        cash = base * (random.random() + 1)
        if isAdult:
            cash += 50 
        return round(cash, 2)
    
    # Função que simula o tempo que o visitante demoraria a chegar a um local
    async def goToPosition(self, newPosition):
        distance = self.position.getDistance(newPosition)
        self.position = newPosition

        await asyncio.sleep(math.sqrt(distance))

    # fiz esta função para verificar os dados dos users
    def print_info(self):
        print()
        print("===== VISITOR INFO =====")
        print(f"JID: {self.jid}")
        print(f"Manager JID: {self.managerJID}")
        print(f"Visitor Nº: {self.num}")
        print(f"Position: ({self.position.posX}, {self.position.posY})")
        print()
        print(f"Adult: {self.isAdult}")
        print(f"Height: {self.height:.2f} m")
        print(f"Patience Level: {self.patienceLevel}")
        print(f"Adrenaline Level: {self.adrenalineLevel}")
        print(f"Vegan: {self.isVegan}")
        print(f"Special Needs: {self.specialNeeds}")
        print()
        print(f"Enjoyment: {self.enjoyment}")
        print(f"Hunger: {self.hunger}")
        print(f"Budget: {self.budget:.2f} €")
        print("========================")