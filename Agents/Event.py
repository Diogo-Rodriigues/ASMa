import spade 
from spade.agent import Agent

from Behaviours. import 


import random

class Event(Agent):

    def __init__(self, jid, password):
        super().__init__(jid,password)
        # TODO: Add vars



    async def setup (self):

        print(f">> Event_{self.num} started")

        rBH = RegisterBH()
        self.add_behaviour(rBH)