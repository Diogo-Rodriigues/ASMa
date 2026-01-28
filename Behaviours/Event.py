import spade 
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from Behaviours.ReceiveRest import ReceiveRestBH
from Behaviours.ReceiveAtt import ReceiveAttBH
from Behaviours.SimRide import SimRideBH

from Classes.Negotiation import Negotiation

import jsonpickle
import asyncio
import datetime

# Behaviour OneShot destinado ao Manager, que irá simular eventos no parque
class EventBH(OneShotBehaviour):
    def __init__(self, eventPosition, adrenalineLevel):
        super().__init__()
        self.eventPosition = eventPosition
        self.adrenalineLevel = adrenalineLevel
        self.hasStarted = False
        self.visitors = []

    async def on_start(self):
        self.proposal = Negotiation(attractionPosition=self.eventPosition, adrenalineLevel=self.adrenalineLevel)
        await self.notifyAllVisitors(self.agent.visitorList)

    async def run(self):
        #Aguardar que visitors interessados cheguem ao Evento
        await asyncio.sleep(20) # TODO: Testar Valores

        await self.getVisitors()

        await self.refuseVisitors()

        # await self.


    
    async def notifyAllVisitors(self, visitorList):
        for visitorJID in visitorList:
            msg = Message(to=visitorJID)
            msg.set_metadata("performative", "PROPOSE")
            msg.set_metadata("thread", f"E-{self.agent.agentName}")
            msg.body = jsonpickle.encode()

            await self.send(msg)

    async def getVisitors(self):
        beginWaiting = datetime.datetime.now()

        while(datetime.datetime.now() - beginWaiting < 25):
            msg = await self.receive(timeout = 25)

            if msg:
                perf = msg.metadata.get("performative")
                if perf == "SUBSCRIBE":
                    self.visitors.append(msg.sender)

            msg2 = self.make_reply(msg)
            msg2.set_metadata("performative", "AGREE")
            await self.send(msg2)

    async def refuseVisitors(self):
        while(True):
            msg = await self.receive(timeout=3)

            msg2 = self.make_reply()
            msg2.set_metadata("performative", "REFUSE")
            await self.send(msg2)

            if not msg:
                break