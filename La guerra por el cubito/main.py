import colores
import constantes
import pygame
import enemies
import random
import balas
import sql
import allies
pygame.init()
"""LOGEO IMG"""
img = pygame.image.load("imagenes/fondo.jpg")
img_game_over = pygame.image.load("imagenes//game_over.jpg")
img_titulo = pygame.image.load("imagenes/titulo.png")
"""ESCALO LAS IMG"""
img_game_over = pygame.transform.scale(img_game_over,(1000,1000))
img = pygame.transform.scale(img,(constantes.ANCHO_FONDO,constantes.ALTO_FONDO))
"""JUGADOR"""
player_ = allies.Player()
"""PANTALLA"""
screen = pygame.display.set_mode([constantes.ANCHO_PANTALLA,constantes.ALTO_PANTALLA])
pos_fondo = [-1000,0]
"""DECLARO LISTAS"""
lista_balas = []
lista_enemigos = []
"""TIMMERS"""
timer = pygame.time.Clock()
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos,1000) 
"""CONTADORES"""
contador_segundos = 0
contador_segundos_generacion = 0
contador_segundos_movimiento = 0
contador_segundos_disparar = 0
contador_kills = 0
contador_pantalla_0 = 0
contador = 1
"""TEXTO"""
fuente = pygame.font.SysFont("Arial", 50)
texto_ingresar = fuente.render("Ingresa", True, colores.BLACK)
texto_rankin = fuente.render("Ranking", True, colores.BLACK)
"""BANDERAS"""
flag_correr = True
flag = True

opcion_game = 0

name_ingreso_rect = pygame.Rect(300,500,400,60)
ingresar_boton_rect = pygame.Rect(550,600,150,70)
ranking_boton_rect = pygame.Rect(300,600,150,70)
menu_rect = pygame.Rect(900,0,100,50)

"""GENERO MI SQL"""
sql.generar_sql()

while flag_correr:

    """PONGO EL NOMBRE A LA PESTAÑA"""
    pygame.display.set_caption("La guerra de las pitusas")
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                if opcion_game == 1:
                     datos_player = sql.ingresar_datos_sql(name_ingreso,score)
                flag_correr = False

    """OPCION GAME 0"""
    if opcion_game == 0:   
        if flag:
            musica = pygame.mixer.music.load("musica/musica_retro2.mp3")
            musica = pygame.mixer.music.play(-1)
            score = 0.0
            name_ingreso = ""
            flag = False

        ingreso_fuente = fuente.render(name_ingreso,True,colores.WHITE) 
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ingresar_boton_rect.collidepoint(evento.pos):
                    if len(name_ingreso) >0:
                            opcion_game = 1
                            flag = True
                if ranking_boton_rect.collidepoint(evento.pos):
                    opcion_game = 3
                    flag = True
            if evento.type == pygame.KEYDOWN:    
                if evento.key == pygame.K_BACKSPACE:
                    name_ingreso = name_ingreso[0:-1]
                else:
                    if len(name_ingreso) <14:
                        name_ingreso += evento.unicode
        
        screen.blit(img,pos_fondo)
        pygame.draw.rect(screen,colores.GREEN1,name_ingreso_rect,2)  
        pygame.draw.rect(screen,colores.BLUE,ingresar_boton_rect)  
        pygame.draw.rect(screen,colores.RED4,ranking_boton_rect) 
        screen.blit(texto_ingresar,ingresar_boton_rect)
        screen.blit(texto_rankin,ranking_boton_rect) 
        screen.blit(ingreso_fuente,name_ingreso_rect)
        screen.blit(img_titulo,(160,80,500,500))

    """OPCION GAME 1"""
    if opcion_game == 1:
        screen.blit(img,pos_fondo)   
        if flag:
            musica = pygame.mixer.music.load("musica/musica_retro1.mp3")
            musica = pygame.mixer.music.play(-1)
            flag = False
        """ACCIONES POR EVENTOS""" 
        for evento in lista_eventos:
            if evento.type == pygame.KEYDOWN:    
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: 
                    bala = allies.Player.disparar(player_)
                    lista_balas.append(bala) 

            if evento.type == pygame.USEREVENT: 
                if evento.type == timer_segundos:  
                        contador_segundos +=1
                        contador_segundos_generacion +=1
                        contador_segundos_movimiento +=1
                        contador_segundos_disparar +=1
                        score +=1
                        """GENERAR ENEMIGOS POR TIMER USEREVENT""" 
                        if contador_segundos_generacion == 1:
                            enemigos_ = enemies.generar_enemigos()
                            lista_enemigos.append(enemigos_)
                            contador_segundos_generacion = 0
                        """CAMBIAR MOVIMIENTO DE ENEMIGOS POR USEREVENT"""
                        if contador_segundos_movimiento == 3:
                            contador_segundos_movimiento = 0
                            for enemigo in lista_enemigos:
                                opciones = ["right","left"]
                                enemigo.opcion = random.choice(opciones)
                        if contador_segundos_disparar == 2:
                            for enemigo in lista_enemigos:    
                                bala = enemies.Enemigos.disparar(enemigo)
                                lista_balas.append(bala)
                                contador_segundos_disparar = 0
    
        """ACCIONES POR TECLAS PRESIONADAS"""
        lista_teclas = pygame.key.get_pressed()
        if True in lista_teclas:
            if lista_teclas[pygame.K_RIGHT] or lista_teclas[pygame.K_d]:
                player_.move_ship("right")
                pos_fondo[0] +=2
            if lista_teclas[pygame.K_LEFT] or lista_teclas[pygame.K_a]:
                player_.move_ship("left")
                pos_fondo[0] -=2
        """CAMBIO DE POSICION Y FUNDO LAS IMAGENES"""      
        screen.blit(player_.ship,player_.rect)
        """fundo y modifico la posicion de mis naves enemigas"""        
        for indice,nave_enemiga in enumerate(lista_enemigos):
            enemies.Enemigos.mover_nave(nave_enemiga)
            enemies.Enemigos.cambiar_escalas(nave_enemiga)
            screen.blit(nave_enemiga.naveEnemiga,nave_enemiga.rect)
        """MUEVO LAS BALAS(allies and enemies) y pregunto por colisiones contra el player y contra naves enemigas"""
        for indice,bala in enumerate(lista_balas):
                eliminar = balas.Balas.mover_bala(bala)
                screen.blit(bala.bala,bala.rect)
                if eliminar:
                    lista_balas.pop(indice)
                if bala.pertenece == "enemigo":     
                    if player_.rect.colliderect(bala.rect):
                        player_.life -=1  
                        if player_.life <=0:
                            opcion_game = 2
                            flag = True
                            datos_player = sql.ingresar_datos_sql(name_ingreso,score)
                        lista_balas.pop(indice)
                elif bala.pertenece == "player":
                        indice_nave = bala.rect.collidelist(lista_enemigos) 
                        if indice_nave >= 0:
                            nave_enemiga = lista_enemigos[indice_nave]
                            nave_enemiga.vidaEnemiga -=1
                            score +=0.5
                            if nave_enemiga.vidaEnemiga <= 0:
                                lista_enemigos.pop(indice_nave) 
                                score +=10
                                contador_kills +=1
                            lista_balas.pop(indice)
        """FUNDO TEXTOS"""
        mensaje_kills = "Kills: {0}".format(contador_kills)
        mensaje_vida = "Vida: {0}".format(player_.life)
        mensaje_score = "Score: {0}".format(score)
        mensaje_tiempo = "Segundos: {0}".format(contador_segundos)
        texto_kills = fuente.render(mensaje_kills, True, colores.RED4)
        texto_score = fuente.render(mensaje_score, True, colores.RED4)
        texto_vida = fuente.render(mensaje_vida,True,colores.BLUE)
        texto_tiempo = fuente.render(mensaje_tiempo,True,colores.YELLOW1)
        screen.blit(texto_kills,(10,10))
        screen.blit(texto_tiempo,(400,950))
        screen.blit(texto_score,(10,950)) 
        screen.blit(texto_vida,(800,950))  
    """OPCION 2"""    
    if opcion_game == 2:
        if flag:
            musica = pygame.mixer.music.load("musica/GameOver.mp3")
            musica = pygame.mixer.music.play(1)
            flag = False
        screen.blit(img_game_over,(0,0))
        for eventos in lista_eventos:
            if evento.type == pygame.USEREVENT: 
                    if evento.type == timer_segundos:
                         contador_pantalla_0 +=1
                         if contador_pantalla_0 == 5:
                              opcion_game = 3
                              flag_musica = True
        """OPCION 3"""
    if opcion_game == 3:
             if flag:
                musica = pygame.mixer.music.load("musica/musica_retro2.mp3")
                musica = pygame.mixer.music.play(-1)
                flag = False
             contador = 0
             lista_ranking = sql.generar_lista_sql()
             lista_ranking.sort(key = lambda score: score["score"],reverse=True)
             rect_ranking = pygame.Rect(10,5,100,100)
             screen.blit(img,(0,0))
             for i in lista_ranking:
                contador +=1
                mensaje_ranking = "{0}° Nombre: {1} score: {2}".format(contador,i["name"],i["score"])
                texto_rankig = fuente.render(mensaje_ranking,True,colores.RED1)
                screen.blit(texto_rankig,rect_ranking)
                rect_ranking.y += 50
                if contador == 21:
                     break
             for eventos in lista_eventos:
                 if evento.type == pygame.MOUSEBUTTONDOWN:
                    if menu_rect.collidepoint(evento.pos):     
                        opcion_game = 0
                        flag = True      
             pygame.draw.rect(screen,colores.BLUE,menu_rect)
             texto_menu = fuente.render("Menu",True,colores.BLACK)
             screen.blit(texto_menu,menu_rect)
    #ACTUALIZO LA PANTALLA
    pygame.display.flip()
    """DECLARO LOS TICKS(FPS) DE MI PROGRAMA"""
    timer.tick(30)
print(lista_eventos)
pygame.quit