import spade 
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from Classes.VisitorData import VisitorData

import jsonpickle
import random
import asyncio
import math
import datetime

# Behaviour Cyclic destinado ao Visitor, este estará constantemente a enviar pedidos ao manager para que este lhe sugira atrações que ele possa visitar
class VisitParkBH(CyclicBehaviour):

    async def on_start(self):
        await asyncio.sleep(1)

    async def run(self):

        # self.agent.print_info()

        visitorHungry = self.agent.hunger / 100
        visitorEnjoyment = self.agent.enjoyment
        if visitorEnjoyment > 20:
            visitorEnjoyment = 1
        else:
            visitorEnjoyment /= 100

        if self.agent.budget <=10:
            print(f"{self.agent.agentName} >> Exited Park :) ")
            self.kill()

        msg = await self.receive() # Verficar logo no ínicio se o visitor recebeu uma proposta de evento
        if msg :
            if perf == "PROPOSE":
                proposal = jsonpickle.decode(msg.body)

                if self.eventAcceptance(proposal):
                    return
                

        # TODO: Balance enjoyment
        if (self.agent.chanceRandom(visitorEnjoyment)):
            if(self.agent.chanceRandom(visitorHungry)):
                await self.handleMessage("REQUEST", VisitorData(jid = self.agent.jid,
                                                                    num = self.agent.num,
                                                                    isVegan = self.agent.isVegan,
                                                                    budget = self.agent.budget,
                                                                    position = self.agent.position))
                
            else:
                await self.handleMessage("CPF", VisitorData(jid = self.agent.jid,
                                                            num = self.agent.num,
                                                            isAdult = self.agent.isAdult,
                                                            specialNeeds = self.agent.specialNeeds,
                                                            height = self.agent.height,
                                                            adrenalineLevel = self.agent.adrenalineLevel,
                                                            alrdVisited = self.agent.alrdVisited,
                                                            position = self.agent.position,
                                                            budget = self.agent.budget))
        else:
            #TODO: Talvez dar UNSUBSCRIBE
            print(f"{self.agent.agentName} >> Exited Park :( ")
            self.kill()

        tries = 0
        flagAccepted = False
        while(not flagAccepted and self.agent.enjoyment > 0):

            msg = await self.receive(timeout = 10)

            if msg:
                perf = msg.metadata.get("performative")
                match perf:
                    case "INFORM":
                        restInfo = jsonpickle.decode(msg.body)

                        restJID = restInfo.getJID()

                        await self.agent.goToPosition(restInfo.getPosition())
                        price = restInfo.getPrice()

                        await self.haveMeal(restJID, price)
                        return

                    case "PROPOSE":
                        negotiation = jsonpickle.decode(msg.body)

                        if (self.rideAcceptance(negotiation)):
                            # print(f"{self.agent.name} >> AGREE WITH RIDE")
                            reply = msg.make_reply()
                            reply.set_metadata("performative", "ACCEPT-PROPOSAL")
                            await self.send(reply)
                            self.agent.enjoyment += 7 - tries
                            flagAccepted = True

                        else:
                            # print(f"{self.agent.name} >> REFUSE RIDE")
                            reply = msg.make_reply()
                            reply.set_metadata("performative", "REFUSE")
                            await self.send(reply)
                            self.agent.enjoyment -= math.pow(2, tries)

                    case "REFUSE": # Negotiator é incapaz de sugerir uma atração
                        self.agent.enjoyment /= 2
                        return


        if (not flagAccepted):
            # Se não foi aceite nada é porque o enjoyment deste visitor esgotou
            # TODO: Talvez seja necessário mandar mensagem para o manager antes
            self.kill()
        
        await self.agent.goToPosition(negotiation.getAttractionPosition())
        # print(f"{self.agent.name} >> Arrived Attraction")

        msg = Message(to=negotiation.getAttractionJID())
        msg.set_metadata("performative", "SUBSCRIBE")
        msg.body = jsonpickle.encode(negotiation)
        await self.send(msg)

        await self.getRideResponse(negotiation)


    # Função auxiliar para facilitar o envio de algumas mensagens
    async def handleMessage(self, performative, visitData):
        msg = Message (to=self.agent.managerJID)
        msg.set_metadata("performative", performative)
        msg.body = jsonpickle.encode(visitData)
        await self.send(msg)

    # Função auxiliar que simula uma refeição
    async def haveMeal(self, restJID, price):
        msg = Message(to=restJID)
        msg.set_metadata("performative", "REQUEST")
        
        await self.send(msg)

        msg2 = await self.receive(timeout = 15)

        if msg2:
            perf = msg2.metadata.get("performative")
            if perf == "AGREE":

                await asyncio.sleep(random.randrange(15,31)) # simula o tempo da refeição

                self.agent.budget -= price
                self.agent.hunger = max(self.agent.hunger - 70, 0) # Apenas para a fome nunca ficar abaixo de 0
                self.agent.enjoyment = min(self.agent.enjoyment + 10, 100)

    # Função auxiliar verifica se o visitor aceita ou não a atração proposta
    def rideAcceptance(self, negotiation):

        ewt = negotiation.getEWT()
        patienceList = self.agent.patienceDict[self.agent.patienceLevel]

        adrenalineLevel = negotiation.getAdrenalineLevel()

        currAtt = negotiation.getAttractionJID()
        alrdVisited = self.agent.alrdVisited

        acceptance = 0.5

        acceptance = self.etwApproval(acceptance, patienceList, ewt)
        acceptance = self.adrenalineApproval(acceptance, adrenalineLevel)

        # print(alrdVisited)
        if currAtt in alrdVisited:
            acceptance += (alrdVisited[currAtt] / 10) * 1.5

        # print(f"WITH ACCEPTANCE: {acceptance}")
        return self.agent.chanceRandom(acceptance)

    def eventAcceptance(self, proposal):
        return self.agent.chanceRandom(0.5)

    # Função auxiliar que calcula a variação na aceitação causada pelo tempo de espera estimado
    def etwApproval(self, acceptance, patienceList, ewt):

        (low, high) = patienceList[0]
        if low <= ewt <= high:
            if ewt <= (high / 3):
                acceptance += 0.05

            elif ewt <= (high * 2 / 3):
                acceptance += 0.1

            else:
                acceptance += 0.15
        else:
            low = patienceList[2]
            if low <= ewt:
                acceptance -= (ewt - low) // 100 + 1  

        return acceptance 

    # Função auxiliar que calcula a variação na aceitação causada pela diferença no nivel de adrenalina        
    def adrenalineApproval(self, acceptance, adrenalineLevel):

        variance = 0
        diff = abs(self.agent.adrenalineLevel - adrenalineLevel)
        
        if diff == 0:
            variance = 0.2
        elif diff == 1:
            variance = -0.15
        elif diff == 2:
            variance = -0.3

        return acceptance + variance
        
    async def getRideResponse(self, negotiation):
        response = await self.receive(timeout = 10)

        if response:
            perf = response.metadata.get("performative")
            if perf == "AGREE":
                await self.simQueue(negotiation)
            else:
                return
        
    
    async def simQueue(self, negotiation):
        flagStillWaiting = True
        flagReachedEWT = False
        patienceLevel = self.agent.patienceLevel
        toleranceDict = {1 : [5, 5],               
                         2 : [15, 10],
                         3 : [25, 15]}
        
        tolerance = negotiation.getEWT() + toleranceDict[patienceLevel][0]


        startQueueTime = datetime.datetime.now()
        tries = 1
        while(flagStillWaiting and tries <= 5):

            msg = await self.receive(timeout = tolerance)
            if msg:
                perf = msg.metadata.get("performative")
                match perf: 
                    case "INFORM":  # Ride informou o visitor que chegou a sua vez
                        endQueueTime = datetime.datetime.now()
                        await asyncio.sleep(negotiation.getDuration()) # Simula uma volta na atração

                        
                        hungerVariation = hungerVariation = (endQueueTime - startQueueTime).total_seconds() // 4 #TODO: Verificar se este valor funciona
                        self.agent.hunger = min(self.agent.hunger + hungerVariation, 100) 
                        enjoymentVariation = self.updateEnjoyment(negotiation)
                        self.updateAlrdVisited(enjoymentVariation, negotiation)
                        self.agent.budget -= negotiation.getPrice()
                        return

                    case "PROPOSE": # Manager informa que vai haver um evento caso ele queria abandonar a fila para ir assistir
                        return 
                    
                    case "CANCEL":  # Ride informa que vai ter de cancelar a volta (devido a avaria)
                        self.agent.enjoyment -= math.pow(2,tries + 1)
                        return
            else:
                if not flagReachedEWT:
                    tolerance = toleranceDict[patienceLevel][1]
                    flagReachedEWT = True

                self.agent.enjoyment -= math.pow(2,tries)
                tries += 1

        # FIXME: Talvez não seja necessário
        if(flagStillWaiting):   
            return

    def updateEnjoyment(self, negotiation):
        rideAdrenalineLevel = negotiation.getAdrenalineLevel()
        visitorAdrenalineLevel = self.agent.adrenalineLevel

        aLDiference = abs(visitorAdrenalineLevel - rideAdrenalineLevel)
        enjoymentVariation = 0

        if aLDiference == 0:
            enjoymentVariation = random.randrange(-5, 21)
        elif aLDiference == 1:
            enjoymentVariation = random.randrange(-10, 11)
        else:
            enjoymentVariation = random.randrange(-20, 6)

        if enjoymentVariation > 0:
            self.agent.enjoyment = min(self.agent.enjoyment + enjoymentVariation, 100)
        else:
            self.agent.enjoyment = max(self.agent.enjoyment + enjoymentVariation, 0)

        return enjoymentVariation

    def updateAlrdVisited(self, enjoymentVariation, negotiation):
        # Caso seja a primeira vez a andar nesta diversão
        if negotiation.getAttractionJID() not in self.agent.alrdVisited:
            self.agent.alrdVisited[negotiation.getAttractionJID()] = 0

        if enjoymentVariation > 0:
            if random.random() < 0.1:   # Caso o enjoyment seja positivo, o visitante tem 10% de chance de marcar esta atração como uma que ele gostaria de repetir
                self.agent.alrdVisited[negotiation.getAttractionJID()] = 1
                return
        if self.agent.alrdVisited[negotiation.getAttractionJID()] == 1:
            self.agent.alrdVisited[negotiation.getAttractionJID()] = -1
        else:
            self.agent.alrdVisited[negotiation.getAttractionJID()] -= 1