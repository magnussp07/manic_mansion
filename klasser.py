

class SpillObjekt:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

class Spokelse(SpillObjekt):
    pass

class Spiller(SpillObjekt):
    pass

class Hindring(SpillObjekt):
    pass

class Sau(SpillObjekt):
    pass