from Classes.Coordinates import Coordinates

class Subscription:
    def __init__(self, jid:str, agentType:str, num:int=None, position:Coordinates=None, price:float=None,
                 zone:int=None, ageRestriction:int=None, accessability:bool=None,
                 minHeight:float=None, adrenalineLevel:int=None, veganFriendly:bool=None):
        self.jid = jid
        self.agentType = agentType
        self.num = num
        self.zone = zone
        self.position = position
        self.price = price
        
        self.ageRestriction = ageRestriction
        self.accessability = accessability
        self.minHeight = minHeight
        self.adrenalineLevel = adrenalineLevel

        self.veganFriendly = veganFriendly

    def getJID(self):
        return self.jid
    
    def setJID(self, jid):
        self.jid = jid

    def getAgentType(self):
        return self.agentType
    
    def setAgentType(self, agentType:str):
        self.agentType = agentType

    def getNum(self):
        return self.num
    
    def setNum(self, num):
        self.num = num

    def getPosition(self):
        return self.position
    
    def setPosition(self, position:Coordinates):
        self.position = position

    def getPrice(self):
        return self.price
    
    def setPrice(self, price):
        self.price = price

    def getZone(self):
        return self.zone
    
    def setZone(self, zone):
        self.zone = zone

    def getAgeRestriction(self):
        return self.ageRestriction
    
    def setAgeRestriction(self, ageRestriction):
        self.ageRestriction = ageRestriction

    def getAccessability(self):
        return self.accessability
    
    def setAccessability(self, accessability):
        self.accessability = accessability

    def getMinHeight(self):
        return self.minHeight
    
    def setMinHeight(self, minHeight):
        self.minHeight = minHeight

    def getAdrenalineLevel(self):
        return self.adrenalineLevel
    
    def setAdrenalineLevel(self, adrenalineLevel):
        self.adrenalineLevel = adrenalineLevel

    def getVeganFriendly(self):
        return self.veganFriendly
    
    def setVeganFriendly(self, veganFriendly):
        self.veganFriendly = veganFriendly

    def print_info(self):
        print("=== Subscription Info ===")
        print(f"JID: {self.jid}")
        print(f"Agent Type: {self.agentType}")
        print(f"Number: {self.num}")
        print(f"Zone: {self.zone if self.zone is not None else 'N/A'}")
        print(f"Position: {self.position.toString()}")
        print(f"Price: {self.price:.2f}")
        print(f"Age Restriction: " f"{self.ageRestriction if self.ageRestriction is not None else 'None'}")
        print(f"Minimum Height: " f"{self.minHeight if self.minHeight is not None else 'None'}")
        print(f"Accessibility: " f"{'Yes' if self.accessability else 'No' if self.accessability is not None else 'Unknown'}")
        print(f"Adrenaline Level: " f"{self.adrenalineLevel if self.adrenalineLevel is not None else 'None'}")
        print(f"Vegan Friendly: " f"{'Yes' if self.veganFriendly else 'No' if self.veganFriendly is not None else 'Unknown'}")
        print("=========================")
