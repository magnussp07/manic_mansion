import pygame as pg

from constants import *
from klasser import *
from spiller import Spiller


pg.init()
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
clock = pg.time.Clock()

running = True


spokelser = [Spokelse(200, 300), Spokelse(400, 100)]
spiller = Spiller(50, int(VINDU_HOYDE/2))

while running:
    
    vindu.fill(BLACK)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                spiller.opp = True
            if event.key == pg.K_s:
                spiller.ned = True
            if event.key == pg.K_a:
                spiller.venstre = True
            if event.key == pg.K_d:
                spiller.hoyre = True
                
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                spiller.opp = False
            if event.key == pg.K_s:
                spiller.ned = False
            if event.key == pg.K_a:
                spiller.venstre = False
            if event.key == pg.K_d:
                spiller.hoyre = False
                
    
    spiller.oppdater()


    for s in spokelser:
        s.oppdater()
        #s.tegn()
    
    spiller.tegn(vindu)
        
   
    pg.display.flip()
    clock.tick(FPS)

pg.quit()