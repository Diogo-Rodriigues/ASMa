import spade 
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Coordinates import Coordinates
from Classes.Subscription import Subscription
from Classes.VisitorData import VisitorData

import jsonpickle
import math

# Behaviour Cyclic destinado à Attraction, este estará constantemente a receber pedidos dos outros Agents
class ReceiveAttBH(CyclicBehaviour):

    # async def on_start(self):
        # print(f"{self.agent.agentName} >> Ready to receive requests!")
        # self.flagFirstVisitor = True

    async def run(self):

        msg = await self.receive(timeout = 30)

        if msg:
            perf = msg.metadata.get("performative")            
            
            match perf:
                case "REQUEST":
                    if msg.metadata.get("thread") == f"RP-Manager":
                        reply = msg.make_reply()
                        reply.set_metadata("performative", "INFORM")

                        # Envia profit (pode ser dict simples)
                        reply.body = jsonpickle.encode({"profit": getattr(self.agent, "profit", 0.0)})
                        await self.send(reply)
                        return

                    else:
                        negotiation = jsonpickle.decode(msg.body)
                        ewt = await self.getEWT(self.agent.capacity, self.agent.duration)

                        negotiation.setEWT(ewt)
                        negotiation.setDuration(self.agent.duration)
                        negotiation.setAttractionJID(self.agent.jid)
                        negotiation.setAttractionPosition(self.agent.position)
                        negotiation.setAdrenalineLevel(self.agent.adrenalineLevel)
                        negotiation.setPrice(self.agent.price)

                        msgEWT = msg.make_reply()
                        msgEWT.set_metadata("performative", "INFORM")
                        msgEWT.body = jsonpickle.encode(negotiation)

                        await self.send(msgEWT)

                case "SUBSCRIBE":
                    negotiation = jsonpickle.decode(msg.body)
                    reply = msg.make_reply()

                    async with self.agent.imAvailable_lock:
                        Available = self.agent.imAvailable

                    if Available:
                        reply.set_metadata("performative", "AGREE")
                        await self.send(reply)

                        async with self.agent.queue_lock:
                            self.agent.queue.append(negotiation.getVisitorJID())
                            lenQueue = len(self.agent.queue)

                        if lenQueue == 1:
                            msg = Message(to=self.agent.jid)
                            msg.set_metadata("performative", "INFORM")
                            msg.set_metadata("thread", f"R-Att_{self.agent.num}")
                            await self.send(msg)
                            

                    else:
                        reply.set_metadata("performative", "REFUSE")
                        await self.send(reply)

                        

    async def getEWT(self, capacity, duration):
        async with self.agent.queue_lock:
            lenQueue = len(self.agent.queue)
        if lenQueue == 0:     # Caso chegue o primeiro visitor damos uma tolerância de 5 segundos a ver se chegam mais visitors
            return 5
        return (lenQueue // capacity) * duration