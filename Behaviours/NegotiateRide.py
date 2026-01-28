import spade 
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Behaviours.ReceiveRest import ReceiveRestBH

from Classes.Subscription import Subscription
from Classes.VisitorData import VisitorData

import asyncio
import jsonpickle

# Behaviour OneShot destinado ao Manager, para negociar com um determinado Visitor a melhor atração possível tendo em conta as preferências do mesmo
# Desta forma o Behaviour "ReceiveManager" não fica bloqueado enquanto discute a atração com o visitor
class NegotiateRideBH(CyclicBehaviour):

    def __init__(self, visitData, negotiation):
        super().__init__()
        self.visitData = visitData
        self.negotiation = negotiation

        self.attractions =  {}
        self.restrictions = {}

    async def on_start(self):
        self.visitorJID = self.visitData.getJID()
        self.attractions = self.agent.attDict
        self.restrictions = self.setupVisitorRestrictions(self.visitData)
        self.possibleAtts = self.getPossibleAttractions(self.attractions, self.restrictions)
        self.sortAttractions(self.possibleAtts, self.visitData)

    async def run(self):

        if self.possibleAtts == []:
            
            msg = Message(to=self.visitorJID)
            msg.set_metadata("performative", "REFUSE")
            await self.send(msg)
            self.kill()

        else:

            # print(f"{self.agent.name} >> Suggested Ride:\n")
            # self.possibleAtts[0].print_info()

            attProposal = self.possibleAtts.pop(0)
            msg = Message(to=attProposal.getJID())
            msg.set_metadata("performative", "REQUEST")
            msg.set_metadata("thread", self.negotiation.getThreadID())
            msg.body = jsonpickle.encode(self.negotiation)
            await self.send(msg)

            msgEWT = await self.receive(timeout = 10)

            if msgEWT:
                perf = msgEWT.get_metadata("performative")
                if perf == "INFORM":

                    self.negotiation = jsonpickle.decode(msgEWT.body)

                    msg = Message(to=self.visitorJID)
                    msg.set_metadata("performative", "PROPOSE")
                    msg.set_metadata("thread", self.negotiation.getThreadID())
                    msg.body = jsonpickle.encode(self.negotiation)

                    await self.send(msg)

                    msg2 = await self.receive(timeout = 30)

                    if msg2:
                        perf = msg2.get_metadata("performative")
                        if perf == "ACCEPT-PROPOSAL":
                            # msgRide = Message(to=str(self.negotiation.getAttractionJID()))
                            # msgRide.set_metadata("performative", "REQUEST_RIDE")
                            # msgRide.body = jsonpickle.encode(self.negotiation)
                            # await self.send(msgRide)

                            #TODO: Talvez seja necessário adicionar aqui uma lógica para avisar o bh: "ReceiveManager" que um behaviour negotiation está disponível
                            
                            self.kill()

                        else:
                            #TODO: Verify "REFUSE" LOGIC
                            # print("REFUSE")
                            return
                else:
                    print("ELSE")
                    print(perf)
                    print(msgEWT.sender)
                    return
                

        #TODO: Continuar implementação da negociação
        await asyncio.sleep(1)        

    def setupVisitorRestrictions(self, visitData):
        restrictions = {}
        
        restrictions["isAdult"] = visitData.getIsAdult()
        restrictions["height"] = visitData.getHeight()
        restrictions["specialNeeds"] = visitData.getSpecialNeeds()
        restrictions["budget"] = visitData.getBudget()

        return restrictions
    
    def getPossibleAttractions(self, attractions, restrictions):

        possibleAtts = []

        for att in attractions.values():
            if att[0]:
                attInfo = att[1]

                if self.rideConditions(attInfo, restrictions):
                    possibleAtts.append(att[1])

        return possibleAtts

    def rideConditions(self, attInfo, restrictions):
        # Tem a idade certa para andar na diversão
        ageCondition = attInfo.getAgeRestriction() == 0 or not restrictions["isAdult"] and (attInfo.getAgeRestriction() < 0) or restrictions["isAdult"] and (attInfo.getAgeRestriction() > 0)  
        # Tem a altura mínima para andar na diversão
        heightCondition = restrictions["height"] >= attInfo.getMinHeight()
        # A diversão é acessível
        specialNCondition = not restrictions["specialNeeds"] or attInfo.getAccessability()
        # O visitante consegue pagar uma volta na diversão
        budgetCondition = restrictions["budget"] >= attInfo.getPrice()
        
        return ageCondition and heightCondition and specialNCondition and budgetCondition
    
    def sortAttractions(self, attList, visitData):
        # Ordenamos pela distância ao visitante (Os resultados estão agrupados em grupos de 10 em 10 para que a distância não seja discutida ao nível das casas decimais) (torna a distância num fator mais redundante)
        attList.sort(key = lambda item: round(item.getPosition().getDistance(visitData.getPosition()) / 10) * 10)
        # Ordenamos primeiro por preço (do maior ao menor para favorecer o parque)
        attList.sort(key = lambda item: item.getPrice(), reverse = True)
        # Ordenamos pela adrenalina Correspondente (da menor diferença entre a adrenalina preferencial do visitante e a adrenalina da atração )
        attList.sort(key = lambda item: abs(item.getAdrenalineLevel() - visitData.getAdrenalineLevel()))


