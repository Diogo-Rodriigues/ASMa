import spade 
from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.Coordinates import Coordinates
from Classes.Subscription import Subscription
from Classes.VisitorData import VisitorData

import asyncio
import random

# Behaviour Periodic destinado à Attraction, que irá simular o funcionamento de uma atração
class SimMaintenanceBH(OneShotBehaviour):
    async def run(self):

        await asyncio.sleep(random.randrange(20,30))     # TODO: Verificar este valor de simulação da manutenção

        msg = Message(to = self.agent.jid)
        msg.set_metadata("performative", "INFORM")
        msg.set_metadata("thread", f"R-Att_{self.agent.num}")
        
        await self.send(msg)