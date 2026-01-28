import spade 
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Behaviours.SimMaintenance import SimMaintenanceBH

from Classes.Coordinates import Coordinates
from Classes.Subscription import Subscription
from Classes.VisitorData import VisitorData

import jsonpickle
import asyncio
import math
import random

# Behaviour Periodic destinado à Attraction, que irá simular o funcionamento de uma atração
class SimRideBH(CyclicBehaviour):

    async def on_start(self):  
        self.duration = self.agent.duration
        self.threadID = f"R-Att_{self.agent.num}"
        # if self.agent.num == 1:
        #     self.flagPrint = True

    async def run(self):

        async with self.agent.imAvailable_lock:
            Available = self.agent.imAvailable

        if Available:

            async with self.agent.queue_lock:
                visitors = [self.agent.queue.pop(0) for q in range(len(self.agent.queue))]

            for visitorJID in visitors:
                msg = Message(to=visitorJID)
                msg.set_metadata("performative", "CANCEL")
                await self.send(msg)

            async with self.agent.queue_lock:
                self.agent.queue = []

            msg = None
            while (not msg): 
                msg = await self.receive(60)

            async with self.agent.imAvailable_lock:
                self.agent.imAvailable = True

        async with self.agent.queue_lock:
            lenQueue = len(self.agent.queue)

        if lenQueue == 0:

            msg = None
            while (not msg):
                msg = await self.receive(60)
            
            if msg:
                perf = msg.metadata.get("performative")
                match perf:
                    case "INFORM":  # Recebe informação de si próprio que um visitante chegou à fila
                        await asyncio.sleep(5) # Simulação de espera por mais clientes
                        await self.simulation()

        elif lenQueue < self.agent.capacity:
            await asyncio.sleep(5)
            await self.simulation()

        else:
            await self.simulation()
        
        malfunctionChance = random.random() <= 0.95  # 5% de chance de ocorrer uma avaria

        async with self.agent.imAvailable_lock:
            self.agent.imAvailable = malfunctionChance
            Available = self.agent.imAvailable
            
        if not Available:
            # print(f"{self.agent.agentName} >> MalFunction Detected, Calling Maintenance")
            sMBH = SimMaintenanceBH()
            self.agent.add_behaviour(sMBH)
            return
        
        # print(f"{self.agent.name} >> Profit: {self.agent.profit}")

            

    # Função auxiliar que informa os visitors que chegou a sua vez consequentemente os remove da queue
    async def sendInformMessage(self):
        async with self.agent.queue_lock:
            visitorNum = min(self.agent.capacity, len(self.agent.queue))
            visitors = [self.agent.queue.pop(0) for _ in range(visitorNum)]
        
        for visitorJID in visitors:
            msg = Message(to=visitorJID)
            msg.set_metadata("performative", "INFORM")
            await self.send(msg)
        return visitorNum
    
    async def simulation(self):
        visitorNum = await self.sendInformMessage()
        self.agent.profit += self.agent.price * visitorNum

        # print(f"{self.agent.agentName} >> Ride with {visitorNum}")
        await asyncio.sleep(self.duration)
        await asyncio.sleep(random.randrange(1,4)) # 1 a 3 minutos extra para simular o tempo em que os visitantes saem/entram na atração
        # print(f"{self.agent.agentName} >> +$ {self.agent.price * visitorNum}")

        
  
         