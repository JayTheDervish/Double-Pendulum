# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 18:46:22 2018

@author: JTColeman
"""


import pygame
import numpy as np

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
        
    def display(self):
        pygame.draw.line(screen, self.color, self.startpos, self.endpos, self.width)
        
    def update(self, x1, y1, x2, y2):
        self.startpos = (x1, y1)
        self.endpos = (x2, y2)

def main():
    # initialize pygame
    pygame.init()
    
    pygame.display.set_caption("Double Pendulum")
    
    #ticks
    clock = pygame.time.Clock()
    
    #get input
    print('Input mass 1:')
    m1 = input()
    m1 = float(m1)
    print('Input line 1:')
    l1 = input()
    l1 = float(l1)
    print('Input mass 2:')
    m2 = input()
    m2 = float(m2)
    print('Input line 2:')
    l2 = input()
    l2 = float(l2)
    print('Input theta 1 angle:')
    theta1 = input()
    theta1 = float(theta1) * (np.pi/180)
    print('Input theta 2 angle:')
    theta2 = input()
    theta2 = float(theta2) * (np.pi/180)
    print('Input g:')
    g = input()
    g = float(g)
    

    def positiontheta1(theta1, theta2, dtheta1, dtheta2):
        return (-np.sin(theta1 - theta2)*(m2*l1*dtheta1**2*np.cos(theta1 -theta2) + m2*l2*dtheta2**2) - g*((m1 + m2)*np.sin(theta1)- m2*np.sin(theta2)* np.cos(theta1 - theta2))) / l1*(m1 + m2*np.sin(theta1 - theta2)**2) *0.001

    def positiontheta2(theta2, theta1, dtheta1, dtheta2):
        return (np.sin(theta1 - theta2)*((m1 + m2)*l1*dtheta1**2*np.cos(theta1 - theta2)) + g*((m1 + m2)*np.sin(theta1)*np.cos(theta1 -theta2) - (m1 + m2)*np.sin(theta2))) / l2*(m1 + m2*np.sin(theta1 - theta2)**2) *0.001

    
    
    # main loop condition
    running = True 
    
    #font
    msg = pygame.font.Font('freesansbold.ttf',10)
    
    x1 = int(l1*np.sin(theta1))
    y1 = int(l1*np.cos(theta1))
    
    x2 = x1 + int(l2*np.sin(theta2))
    y2 = y1 + int(l2*np.cos(theta2))
    
    mass = Mass(int(x1), int(y1), 10, red)
    mass2 = Mass(int(x2), int(y2), 10, blue)
    
    tube1 = Tube((240 , 0), (mass.x, mass.y), black)
    tube2 = Tube((mass.x, mass.y), (mass2.x, mass2.y), green)
    
    ltext1 = msg.render("Length 1 = "+ str(int(l1)), 1, black)
    ltext2 = msg.render("Length 2 = "+ str(int(l2)), 1, black)
    
    fps = 60
    
    ticksLastFrame = 0
    
    dtheta1 = 0
    dtheta2 = 0
    
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
        
        time = pygame.time.get_ticks()
        
        deltaTime = (time - ticksLastFrame) / 1000.0
        
        deltaText = msg.render("delta time is "+ str(deltaTime), 1, black)
        
        #call integration here
        theta1 += dtheta1
        theta2 += dtheta2
        rk11 = positiontheta1(theta1, theta2, dtheta1, dtheta2)
        rk21 = positiontheta1(theta1 + rk11/2, theta2 + rk11/2, dtheta1 + rk11/2, dtheta2 + rk11/2)
        rk31 = positiontheta1(theta1 + rk21/2, theta2 + rk21/2, dtheta1 + rk21/2, dtheta2 + rk21/2)
        rk41 = positiontheta1(theta1 + rk31, theta2 + rk31, dtheta1 + rk31, dtheta2 + rk31)
        
        rk12 = positiontheta1(theta1, theta2, dtheta1, dtheta2)
        rk22 = positiontheta1(theta1 + rk12/2, theta2 + rk12/2, dtheta1 + rk12/2, dtheta2 + rk12/2)
        rk32 = positiontheta1(theta1 + rk22/2, theta2 + rk22/2, dtheta1 + rk22/2, dtheta2 + rk22/2)
        rk42 = positiontheta1(theta1 + rk32, theta2 + rk32, dtheta1 + rk32, dtheta2 + rk32)
        
        dtheta1 += (rk11 + 2*rk21 + 2*rk31 + rk41)/6
        dtheta2 += (rk12 + 2*rk22 + 2*rk32 + rk42)/6
        
        #updating values
        x1 = l1*np.sin(theta1)
        y1 = l1*np.cos(theta1) 
        x2 = x1 + l2*np.sin(theta2)
        y2 = y1 + l2*np.cos(theta2)
                
        #update positions here
        mass.update(int(x1), int(y1))
        mass2.update(int(x2), int(y2))
        tube1.update(240, 0, mass2.x, mass2.y)
        tube2.update(mass2.x, mass2.y, mass.x, mass.y)
        
        #Render Code that will not change
        screen.blit(ltext1, (0, 10))
        screen.blit(ltext2, (0, 20))
        screen.blit(deltaText, (0, 30))
        mass.display()
        mass2.display()
        tube1.display()
        tube2.display()
        
        pygame.display.flip()
        
        ticksLastFrame = time
                
    pygame.quit()
                
if __name__=="__main__":
    
    main()