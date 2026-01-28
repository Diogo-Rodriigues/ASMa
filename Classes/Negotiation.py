from Classes.Coordinates import Coordinates

class Negotiation:
    def __init__(self, visitorJID:str=None, attractionJID:str=None, attractionPosition:Coordinates = None, 
                 ewt:int=None, duration:int = None, threadID:str=None, adrenalineLevel:int = None, price:int = None):
        self.visitorJID = visitorJID
        self.attractionJID = attractionJID
        self.attractionPosition = attractionPosition
        self.ewt = ewt
        self.duration = duration
        self.threadID = threadID
        self.adrenalineLevel = adrenalineLevel
        self.price = price

    def getVisitorJID(self):
        return self.visitorJID
    
    def setVisitorJID(self, visitorJID):
        self.visitorJID = visitorJID

    def getAttractionJID(self):
        return self.attractionJID

    def setAttractionJID(self, attractionJID):
        self.attractionJID = attractionJID

    def getAttractionPosition(self):
        return self.attractionPosition   

    def setAttractionPosition(self, attractionPosition):
        self.attractionPosition = attractionPosition

    def getEWT(self):
        return self.ewt
    
    def setEWT(self, ewt):
        self.ewt = ewt

    def getDuration(self):
        return self.duration
    
    def setDuration(self, duration):
        self.duration = duration

    def getThreadID(self):
        return self.threadID
    
    def setThreadID(self, threadID):
        self.threadID = threadID

    def getAdrenalineLevel(self):
        return self.adrenalineLevel
    
    def setAdrenalineLevel(self, adrenalineLevel):
        self.adrenalineLevel = adrenalineLevel

    def getPrice(self):
        return self.price
    
    def setPrice(self, price):
        self.price = price
    
