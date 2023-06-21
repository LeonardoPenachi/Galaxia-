class Balas:
    def __init__(self,bala,x,y,pertenece,rect = "") -> None:
        self.bala = bala
        self.x = x
        self.y = y
        self.pertenece = pertenece
        self.rect = rect
    def mover_bala(self):
        eliminar = False
        if self.pertenece == "player":
            self.rect.y -=15
            if self.y < -10:
                eliminar = True
        elif self.pertenece == "enemigo":
            self.rect.y += 10
            if self.y > 1010:
                eliminar = True
        else:
            print("Hubo un error")
        return eliminar

