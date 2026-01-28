from Classes.Coordinates import Coordinates

class VisitorData:
    def __init__(self, jid:str, num:int = None ,isAdult:bool = None, height:float = None, 
                adrenalineLevel:int = None, isVegan:bool = None, specialNeeds:bool = None, 
                budget:float = None, alrdVisited:list = None, position:Coordinates = None): 
        self.jid = jid

        # Caracteristicas relativas a Attractions
        self.isAdult = isAdult
        self.height = height
        self.adrenalineLevel = adrenalineLevel
        self.specialNeeds = specialNeeds
        self.alrdVisited = alrdVisited

        # Caracteriticas relativas a Restaurants
        self.isVegan = isVegan

        # Características gerais 
        self.position = position
        self.budget = budget
        self.num = num

    def getJID(self):
        return self.jid
    
    def setJID(self, jid):
        self.jid = jid 

    def getNum(self):
        return self.num
    
    def setNum(self, num):
        self.num = num

    def getIsAdult(self):
        return self.isAdult
    
    def setIsAdult(self, isAdult):
        self.isAdult = isAdult

    def getHeight(self):
        return self.height
    
    def setHeight(self, height):
        self.height = height

    def getAdrenalineLevel(self):
        return self.adrenalineLevel
    
    def setAdrenalineLevel(self, adrenalineLevel):
        self.adrenalineLevel = adrenalineLevel

    def getSpecialNeeds(self):
        return self.specialNeeds
    
    def setSpecialNeeds(self, specialNeeds):
        self.specialNeeds = specialNeeds

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getIsVegan(self):
        return self.isVegan

    def setIsVegan(self, isVegan):
        self.isVegan = isVegan

    def getBudget(self):
        return self.budget
    
    def setBudget(self, budget):
        self.budget = budget