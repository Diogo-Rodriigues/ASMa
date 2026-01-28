import math

class Coordinates:
    def __init__(self, posX:float, posY:float):
        self.posX = posX
        self.posY = posY

    def getPosX(self):
        return self.posX
    
    def setPosX(self, posX):
        self.posX = posX

    def getPosY(self):
        return self.posY
    
    def setPosY(self, posY):
        self.posY = posY

    def getDistance(self, destination):
        return math.sqrt( math.pow((self.posX - destination.getPosX()), 2) + 
                          math.pow((self.posY - destination.getPosY()), 2) )
    
    def toString(self):
        return f"(X: {self.posX}, Y: {self.posY})"