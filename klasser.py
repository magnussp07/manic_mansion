
FRIVENSTRE = 200
FRIHOYRE = 700

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
            if self.x > FRIHOYRE:
                self.vx *= -1 # Snu farten (x-retning)
            if self.x < FRIVENSTRE:
                self.vx *= -1 # Snu farten (x-retning)        
            if self.y > VINDUH:
                self.vy *= -1 # Snu farten (y-retning)
                self.y = hoyde - self.radius # Tving den ut fra kanten
            if self.y < self.radius:
                self.vy *= -1 # Snu farten (y-retning)  
        

class Spiller(SpillObjekt):
    pass

class Hindring(SpillObjekt):
    pass

class Sau(SpillObjekt):
    pass