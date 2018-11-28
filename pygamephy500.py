# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 18:46:22 2018

@author: JTColeman
"""

"""
To Do:
    Parent bars to masses
    Copy integration code to file
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
        self.x = x
        self.y = y

class Tube:
    
    def __init__(self, startpos, endpos, color = (255, 255, 255), width = 2):
        self.startpos = startpos
        self.endpos = endpos
        self.color = color
        self.width = width
        self.lengthSquared = (endpos[0] - startpos[0])**2 + (endpos[1] - startpos[1])**2
        
    def display(self):
        pygame.draw.line(screen, self.color, self.startpos, self.endpos, self.width)
        
    def update(self, x1, y1, x2, y2):
        if (x2 - x1)**2 + (y2 - y1)**2 == self.lengthSquared:
            self.startpos = (x1, y1)
            self.endpos = (x2, y2)


def main():
    # initialize pygame
    pygame.init()
    
    pygame.display.set_caption("Double Pendulum")
    
    #ticks
    clock = pygame.time.Clock()
    
    # main loop condition
    running = True 
    
    circle = Mass(390, 150, 10, red)
    circle2 = Mass(340, 100, 10, blue)
    
    tube1 = Tube((240 , 0), (circle2.x, circle2.y), black)
    tube2 = Tube((circle2.x, circle2.y), (circle.x, circle.y), green)
    
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
        
        if pygame.mouse.get_focused():
            mouseState = pygame.mouse.get_pressed()
            
            if mouseState[0]:
                cursorPos = pygame.mouse.get_pos()
                #if (cursorPos[0] - tube2.startpos[0])**2 + (cursorPos[1] - tube2.startpos[1])**2 == tube2.lengthSquared:
                circle.update(cursorPos[0], cursorPos[1])
        
        tube1.update(240 , 0, circle2.x, circle2.y)
        tube2.update(circle2.x, circle2.y, circle.x, circle.y)
        
        #Render Code that will not change
        circle.display()
        circle2.display()
        tube1.display()
        tube2.display()
        
        pygame.display.flip()
                
    pygame.quit()
                
if __name__=="__main__":
    
    main()