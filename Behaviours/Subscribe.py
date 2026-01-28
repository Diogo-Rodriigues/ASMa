import spade 
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from Behaviours.ReceiveRest import ReceiveRestBH
from Behaviours.ReceiveAtt import ReceiveAttBH
from Behaviours.SimRide import SimRideBH
from Behaviours.VisitPark import VisitParkBH

from Classes.Subscription import Subscription

import jsonpickle

# Behaviour OneShot destinado à Attraction e ao Restaurant, para que fiquem registados no Manager
class SubscribeBH(OneShotBehaviour):

    async def run(self):

        agentClass = self.agent.__class__.__name__ 

        if agentClass == "Attraction":
            subscription = Subscription(jid = self.agent.jid, 
                                        agentType = self.agent.__class__.__name__, 
                                        num = self.agent.num,
                                        zone = self.agent.zone,
                                        position = self.agent.position,
                                        ageRestriction = self.agent.ageRestriction,
                                        accessability = self.agent.accessability,
                                        minHeight = self.agent.minHeight,
                                        adrenalineLevel = self.agent.adrenalineLevel,
                                        price = self.agent.price
                                        )

        elif (agentClass == "Restaurant"):
            subscription = Subscription(jid = self.agent.jid, 
                                        agentType = self.agent.__class__.__name__, 
                                        num = self.agent.num,
                                        position = self.agent.position,
                                        veganFriendly = self.agent.veganFriendly,
                                        price = self.agent.price
                                        )
        
        else:
            subscription = Subscription(jid = self.agent.jid,
                                        agentType = self.agent.__class__.__name__)

        msg = Message(to = self.agent.managerJID)
        msg.set_metadata("performative", "SUBSCRIBE")
        msg.body = jsonpickle.encode(subscription)

        await self.send(msg)

        msg2 = await self.receive(timeout = 30)

        if msg2:
            perf = msg2.metadata.get("performative")
            match perf:
                case "AGREE":
                    if agentClass == "Attraction":
                        rABH = ReceiveAttBH()
                        self.agent.add_behaviour(rABH)

                        threadID = f"R-Att_{subscription.getNum()}"
                        rideTemplate = Template()
                        rideTemplate.set_metadata("thread", threadID)

                        nRBH = SimRideBH()
                        self.agent.add_behaviour(nRBH, rideTemplate)


                    
                    elif agentClass == "Restaurant":
                        rRBH = ReceiveRestBH()
                        self.agent.add_behaviour(rRBH)

                    else:
                        vPBH = VisitParkBH()
                        self.agent.add_behaviour(vPBH)
                

        else:
            sBH = SubscribeBH()
            self.agent.add_behaviour(sBH)
        


        

    
