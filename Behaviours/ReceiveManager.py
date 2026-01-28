import spade 
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from Behaviours.NegotiateRide import NegotiateRideBH

from Classes.Coordinates import Coordinates
from Classes.Subscription import Subscription
from Classes.VisitorData import VisitorData
from Classes.Negotiation import Negotiation

import jsonpickle
import math

# Behaviour Cyclic destinado ao Manager, este estará constantemente a receber pedidos dos outros Agents
class ReceiveManagerBH(CyclicBehaviour):
    async def on_start(self):
        print(f"{self.agent.agentName} >> Ready to receive requests!")

    async def run(self):

        msg = await self.receive(timeout = 60)

        if msg:
            perf = msg.metadata.get("performative")
            match perf:
                # FIXME: Acrescentar opção dos visitores subscreverem
                case "SUBSCRIBE":   # Subscrição no parque
                    subsc = jsonpickle.decode(msg.body)

                    agentType = subsc.getAgentType()
                    agentJID = subsc.getJID()

                    if(agentType == "Attraction"):
                        self.agent.attDict[agentJID] = [True, subsc]

                    elif (agentType == "Restaurant"):
                        self.agent.restDict[agentJID] = (subsc.getVeganFriendly(), subsc)

                    else:
                        self.agent.visitorList.append(agentJID)

                    msg2 = Message(to=subsc.getJID())
                    msg2.set_metadata("performative", "AGREE")

                    await self.send(msg2)

                case "CPF": # Call For Proposals para iniciar processo de negociação de diversões
                    visitData = jsonpickle.decode(msg.body)

                    visitJID = visitData.getJID()
                    visitNum = visitData.getNum()
                    threadID = f"N-visit_N{visitNum}"
                    negotiation = Negotiation(visitorJID = visitJID, threadID = threadID)

                    negotiationTemplate = Template()
                    negotiationTemplate.set_metadata("thread", threadID)

                    nRBH = NegotiateRideBH(visitData, negotiation)
                    self.agent.add_behaviour(nRBH, negotiationTemplate)

                case "REQUEST": # Pedido de Restaurante

                    visitData = jsonpickle.decode(msg.body)

                    visitPosition = visitData.getPosition()
                    visitIsVegan = visitData.getIsVegan()

                    closestRest = self.getClosestRest(visitPosition, visitIsVegan)
                    closestRestInfo = self.agent.restDict[closestRest][1]

                    msg2 = Message(to = visitData.getJID())
                    msg2.set_metadata("performative", "INFORM")
                    msg2.body = jsonpickle.encode(closestRestInfo)

                    await self.send(msg2)

    async def on_end(self):
        print(f"{self.agent.name} >> Park is Closing!")

    def getClosestRest(self, currLocation:Coordinates, isVegan):
        minDistance = 500
        dict = self.agent.restDict
        for restJID in dict:
            if not (not isVegan or dict[restJID][0]):
                continue
            dist = currLocation.getDistance(dict[restJID][1].getPosition())
            if (dist <= minDistance):
                minDistance = dist
                closestRest = restJID
        return closestRest