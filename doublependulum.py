# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 18:46:22 2018

@author: JTColeman
"""


import pygame
import numpy as np
#import fpectl
#import fpetest

#fpectl.turnon_sigfpe()
#fpetest.test()

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
    print('RK4? (Y/N)')
    isRK4 = input()
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
    theta1 = float(theta1) * (np.pi/180.0)
    print('Input theta 2 angle:')
    theta2 = input()
    theta2 = float(theta2) * (np.pi/180.0)
    print('Input g:')
    g = input()
    g = float(g)
    

    def positiontheta1(theta1, theta2, dtheta1, dtheta2):
        M = m1 + m2
        angleChange = theta1 - theta2
        alpha = m1 + m2*np.sin(angleChange)*np.sin(angleChange)
        return (-np.sin(angleChange)*(m2*l1*(dtheta1**2)*np.cos(angleChange) + m2*l2*(dtheta2**2)) - g*(M*np.sin(theta1)- m2*np.sin(theta2)* np.cos(angleChange))) / l1*alpha

    def positiontheta2(theta2, theta1, dtheta1, dtheta2):
        M = m1 + m2
        angleChange = theta1 - theta2
        alpha = m1 + m2*np.sin(angleChange)*np.sin(angleChange)
        return (np.sin(angleChange)*(M*l1*(dtheta1**2) + m2*l2*(dtheta2**2)*np.cos(angleChange)) + g*(M*np.sin(theta1)*np.cos(angleChange) - M*np.sin(theta2))) / l2*alpha

    def velocitytheta1(theta1, theta2, dtheta1, dtheta2):
        return dtheta1
    
    def velocitytheta2(theta1, theta2, dtheta1, dtheta2):
        return dtheta2
    
    
    # main loop condition
    running = True 
    
    #font
    msg = pygame.font.Font('freesansbold.ttf',10)
    
    x1 = int(l1*np.sin(theta1)) + 240
    y1 = int(l1*np.cos(theta1)) + 120
    
    x2 = x1 + int(l2*np.sin(theta2))
    y2 = y1 + int(l2*np.cos(theta2))
    
    mass = Mass(int(x1), int(y1), 10, red)
    mass2 = Mass(int(x2), int(y2), 10, blue)
    
    tube1 = Tube((240 , 120), (mass.x, mass.y), black)
    tube2 = Tube((mass.x, mass.y), (mass2.x, mass2.y), green)
    
    ltext1 = msg.render("Length 1 is "+ str(int(l1)), 1, black)
    ltext2 = msg.render("Length 2 is "+ str(int(l2)), 1, black)
    
    fps = 60
    
    ticksLastFrame = 0
    oldtheta1 = theta1
    oldtheta2 = theta2
    dtheta1 = 0.0
    dtheta2 = 0.0
    olddtheta1 = 0.0
    olddtheta2 = 0.0
    
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
        if(isRK4 == 'Y'):
            """
            #RK4
            rk11 = positiontheta1(theta1, theta2, dtheta1, dtheta2)
            rk1v1 = velocitytheta1(theta1, theta2, dtheta1, dtheta2)
            rk21 = positiontheta1(theta1 + (rk11/2)*deltaTime, theta2 + (rk11/2)*deltaTime, dtheta1 + (rk11/2)*deltaTime, dtheta2 + (rk11/2)*deltaTime)
            rk2v1 = velocitytheta1(theta1 + (rk1v1/2)*deltaTime, theta2 + (rk1v1/2)*deltaTime, dtheta1 + (rk1v1/2)*deltaTime, dtheta2 + (rk1v1/2)*deltaTime)
            rk31 = positiontheta1(theta1 + (rk21/2)*deltaTime, theta2 + (rk21/2)*deltaTime, dtheta1 + (rk21/2)*deltaTime, dtheta2 + (rk21/2)*deltaTime)
            rk3v1 = velocitytheta1(theta1 + (rk2v1/2)*deltaTime, theta2 + (rk2v1/2)*deltaTime, dtheta1 + (rk2v1/2)*deltaTime, dtheta2 + (rk2v1/2)*deltaTime)
            rk41 = positiontheta1(theta1 + rk31*deltaTime, theta2 + rk31*deltaTime, dtheta1 + rk31*deltaTime, dtheta2 + rk31*deltaTime)
            rk4v1 = positiontheta1(theta1 + rk3v1*deltaTime, theta2 + rk3v1*deltaTime, dtheta1 + rk3v1*deltaTime, dtheta2 + rk3v1*deltaTime)
            
            rk12 = positiontheta2(theta1, theta2, dtheta1, dtheta2)
            rk1v2 = velocitytheta2(theta1, theta2, dtheta1, dtheta2)
            rk22 = positiontheta2(theta1 + (rk12/2)*deltaTime, theta2 + (rk12/2)*deltaTime, dtheta1 + (rk12/2)*deltaTime, dtheta2 + (rk12/2)*deltaTime)
            rk2v2 = velocitytheta2(theta1 + (rk1v2/2)*deltaTime, theta2 + (rk1v2/2)*deltaTime, dtheta1 + (rk1v2/2)*deltaTime, dtheta2 + (rk1v2/2)*deltaTime)
            rk32 = positiontheta2(theta1 + (rk22/2)*deltaTime, theta2 + (rk22/2)*deltaTime, dtheta1 + (rk22/2)*deltaTime, dtheta2 + (rk22/2)*deltaTime)
            rk3v2 = velocitytheta2(theta1 + (rk2v2/2)*deltaTime, theta2 + (rk2v2/2)*deltaTime, dtheta1 + (rk2v2/2)*deltaTime, dtheta2 + (rk2v2/2)*deltaTime)
            rk42 = positiontheta2(theta1 + rk32*deltaTime, theta2 + rk32*deltaTime, dtheta1 + rk32*deltaTime, dtheta2 + rk32*deltaTime)
            rk4v2 = velocitytheta2(theta1 + rk3v2*deltaTime, theta2 + rk3v2*deltaTime, dtheta1 + rk3v2*deltaTime, dtheta2 + rk3v2*deltaTime)
            
            theta1 = oldtheta1 + deltaTime*(rk1v1 + 2*rk2v1 + 2*rk3v1 + rk4v1)/6
            theta2 = oldtheta2 + deltaTime*(rk1v2 + 2*rk2v2 + 2*rk3v2 + rk4v2)/6
            
            dtheta1 = olddtheta1 + deltaTime*(rk11 + 2*rk21 + 2*rk31 + rk41)/6
            dtheta2 = olddtheta2 + deltaTime*(rk12 + 2*rk22 + 2*rk32 + rk42)/6
            """
        
        #Euler
        dtheta1 = olddtheta1 + deltaTime*positiontheta1(theta1, theta2, dtheta1, dtheta2)
        dtheta2 = olddtheta2 + deltaTime*positiontheta2(theta1, theta2, dtheta1, dtheta2)
        
        theta1 = oldtheta1 + deltaTime*velocitytheta1(theta1, theta2, dtheta1, dtheta2)
        theta2 = oldtheta2 + deltaTime*velocitytheta2(theta1, theta2, dtheta1, dtheta2)
        
        oldtheta1 = theta1
        oldtheta2 = theta2
        olddtheta1 = dtheta1
        olddtheta2 = dtheta2
        
        #updating values
        x1 = int(l1*np.sin(theta1)) + 240
        y1 = int(l1*np.cos(theta1)) + 120
        x2 = x1 + int(l2*np.sin(theta2))
        y2 = y1 + int(l2*np.cos(theta2))
                
        #update positions here
        mass.update(int(round(x1)), int(round(y1)))
        mass2.update(int(round(x2)), int(round(y2)))
        tube1.update(240, 120, mass.x, mass.y)
        tube2.update(mass.x, mass.y, mass2.x, mass2.y)
        
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