from constants import *

class SpillObjekt:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

class Spokelse(SpillObjekt):
    def __init__(self, x:int, y: int) -> None:
        super().__init__(x, y)
        self.vx = 5
        self.vy = 5

    def oppdater(self):
        self.x += self.vx
        self.y += self.vy

        #Sjekk kollisjon med frisoner
        if self.x > GRENSE_H or self.x < GRENSE_V:
            self.vx *= -1        
        if self.y > VINDU_HOYDE or self.y < 0:
            self.y *= -1
        

class Spiller(SpillObjekt):
    pass

class Hindring(SpillObjekt):
    pass

class Sau(SpillObjekt):
    pass