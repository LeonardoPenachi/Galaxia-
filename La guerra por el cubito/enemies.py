import random
import balas
import pygame
import constantes
class Enemigos:
    img_enemigos = pygame.image.load("imagenes/nave_enemiga.png")
    img_balas_enemigos = pygame.image.load("imagenes/nebulosa.png")
    img_balas_enemigos = pygame.transform.scale(img_balas_enemigos,(15,15))
    def __init__(self,nave = img_enemigos,vida = 0,x = 0,y = 0,opcion = "",rect = "",bala = img_balas_enemigos) -> None:
        self.naveEnemiga = nave
        self.vidaEnemiga = vida
        self.x = x
        self.y = y
        self.opcion = opcion
        self.rect = rect
        self.img_bala = bala
    def mover_nave(self):
         if self.opcion== "right":
            self.x += 5
            if self.x > 970:
                self.opcion = "left"
         if self.opcion == "left":
            self.x -= 5
            if self.x < 20:
                self.opcion = "right"
    def disparar(self):
       disparo = balas.Balas(self.img_bala,self.x +50,self.y,"enemigo")
       disparo.rect = pygame.Rect(disparo.x,disparo.y,5,10)
       return disparo
    def cambiar_escalas(self):
        self.naveEnemiga = pygame.transform.scale(self.naveEnemiga,constantes.SCALE_EMEMY[self.vidaEnemiga])
        self.rect = pygame.Rect((self.x,self.y),constantes.SCALE_EMEMY[self.vidaEnemiga])

def generar_enemigos():
    lista_x = [500,450,400,350,300,250,200,150,100,50]
    lista_y = [20,65,110,155,200,245]
    lista_vida = [10,7,5,3,1]
    lista_opciones = ["right","left"]
    enemigo_1 = Enemigos(vida = random.choice(lista_vida),x = random.choice(lista_x),y = random.choice(lista_y), opcion = random.choice(lista_opciones))
    return enemigo_1
