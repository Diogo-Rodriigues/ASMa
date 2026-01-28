import spade 
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.Coordinates import Coordinates
from Classes.Subscription import Subscription
from Classes.VisitorData import VisitorData

import jsonpickle
import math

# Behaviour Cyclic destinado ao Restaurant, este estará constantemente a receber pedidos dos outros Agents
class ReceiveRestBH(CyclicBehaviour):

    # async def on_start(self):

    async def run(self):

        msg = await self.receive(timeout=30)
        if not msg:
            return

        perf = msg.metadata.get("performative")

        if perf == "REQUEST":   # Pedido de profit
            if msg.sender == self.agent.managerJID:
                reply = msg.make_reply()
                reply.set_metadata("performative", "INFORM")

                # Envia profit (pode ser dict simples)
                reply.body = jsonpickle.encode({"profit": getattr(self.agent, "profit", 0.0)})
                await self.send(reply)
                return

            else: # Pedido de refeição
                msgAgree = Message(to=msg.sender)
                msgAgree.set_metadata("performative", "AGREE")
                await self.send(msgAgree)

                self.agent.profit += self.agent.price

                

                