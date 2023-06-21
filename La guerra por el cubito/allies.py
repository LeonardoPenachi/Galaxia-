import balas
import pygame
class Player:

    img_balas_player = pygame.image.load("imagenes/balas_player.png")
    img_player = pygame.image.load("imagenes/nave_player.png")
    img_player = pygame.transform.scale(img_player,(100,100))
    img_balas_player = pygame.transform.scale(img_balas_player,(20,20))
    rec_player = pygame.Rect(450,800,100,100)

    def __init__(self,ship = img_player,life=20,x = 450,y = 800,rect = rec_player,bala = img_balas_player) -> None:
        self.ship = ship
        self.life = life
        self.x = x
        self.y = y
        self.rect = rect
        self.img_bala = bala
    def move_ship(self,opcion):
        if opcion == "right" and self.rect.x < 880:
            self.rect.x +=10
        if opcion == "left" and self.rect.x > 20:
            self.rect.x -=10
    def disparar(self):
        disparo = balas.Balas(self.img_bala,self.rect.x,self.rect.y,"player")
        disparo.rect = pygame.Rect(disparo.x+45,disparo.y,20,20)
        return disparo
    def restar_vida(self):
        self.vida -=1