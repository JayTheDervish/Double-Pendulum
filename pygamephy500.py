# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 18:46:22 2018

@author: JTColeman
"""

import pygame

#defining some colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
orange = 255, 165, 0
pink = 255, 105, 180

# create an SDL surface on a screen with this size
screen = pygame.display.set_mode((480,360))

class Mass:
    
    def __init__(self, x, y, size, color = (255, 255, 255), width = 0):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.width = width
        
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.width)
        
    def update(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

class Tube:
    
    def __init__(self, startpos, endpos, color = (255, 255, 255), width = 2):
        self.startpos = startpos
        self.endpos = endpos
        self.color = color
        self.width = width
        
    def display(self):
        pygame.draw.line(screen, self.color, self.startpos, self.endpos, self.width)
        
    def update(self, x, y):
        #self.startpos = (self.startpos[0] + 1, self.startpos[1] + 1)
        self.endpos = (self.endpos[0] + x, self.endpos[1] + y)


def main():
    # initialize pygame
    pygame.init()
    
    pygame.display.set_caption("Double Pendulum")
    
    #ticks
    clock = pygame.time.Clock()
    
    # main loop condition
    running = True 
    
    circle = Mass(150 + 240, 150, 10, red)
    circle2 = Mass(100 + 240, 100, 10, blue)
    
    tube1 = Tube((240 , 0), (100 + 240, 100), black)
    tube2 = Tube((100 + 240, 100), (150 + 240, 150), black)
    
    fps = 60
    
    #main loop
    while running:
        # limit frame rate
        clock.tick(fps)
        
        # event handling
        for event in pygame.event.get():
            #handle quitting event
            if event.type == pygame.QUIT:
                # exit main loop
                running = False
        
        screen.fill(white)
        
        
        circle.update(0, 1)
        circle2.update(0, 1)
        tube1.update(-2, 1)
        tube2.update(-3, 2)
        
        
        circle.display()
        circle2.display()
        tube1.display()
        tube2.display()
        
        pygame.display.flip()
                
    pygame.quit()
                
if __name__=="__main__":
    
    main()