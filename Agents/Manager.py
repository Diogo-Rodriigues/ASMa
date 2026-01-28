import spade
from spade.agent import Agent
from spade.template import Template

from Behaviours.ReceiveManager import ReceiveManagerBH
from Behaviours.EstimateProfit import EstimateProfitBH

import datetime

class Manager(Agent):

    def __init__(self, jid, password, eventLocations):
        super().__init__(jid, password)
        self.eventLocations = eventLocations

        self.restDict = {}
        self.attDict = {}
        self.visitorList = []

        self.profit = {"restaurants" : [0,0,0],
                       "attractions" : {1 : [0,0,0],
                                        2 : [0,0,0],
                                        3 : [0,0,0],
                                        4 : [0,0,0],
                                        5 : [0,0,0]},
                       "events" : []}
        
        self.agentName = "manager@"

    async def setup(self):

        print(">> Manager started")

        rMBH = ReceiveManagerBH()
        self.add_behaviour(rMBH)
        
        RequestProfitTemplate = Template()
        RequestProfitTemplate.set_metadata("thread", "RP-Manager")

        period = 60
        startingTime = datetime.datetime.now() + datetime.timedelta(seconds=period)
        profitBH = EstimateProfitBH(period=60, start_at=startingTime)  # de 10 em 10 segundos
        self.add_behaviour(profitBH, RequestProfitTemplate)