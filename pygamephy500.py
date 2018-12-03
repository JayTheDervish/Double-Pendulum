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
        

def rungekuttasecondorder(f1, f2, deltaTime, n, alpha):
    h = deltaTime
    t = 0
    x = alpha[0]
    y = alpha[1]
    i = 1
    xs = []
    ys = []
    ts = []
    xs.append(x)
    ys.append(y)
    ts.append(t)
    k1 = [0, 0]
    k2 = [0, 0]
    k3 = [0, 0]
    k4 = [0, 0]
    while (i < n):
        k1[0] =  f1(t, x, y)
        k1[1] =  f2(t, x, y)
        k2[0] =  f1(t + h/2, x + k1[0]/2, y + k1[1]/2)
        k2[1] =  f2(t + h/2, x + k1[0]/2, y + k1[1]/2)
        k3[0] =  f1(t + h/2, x + k2[0]/2, y + k2[1]/2)
        k3[1] =  f2(t + h/2, x + k2[0]/2, y + k2[1]/2)
        k4[0] =  f1(t + h, x + k3[0], y + k3[1])
        k4[1] =  f2(t + h, x + k3[0], y + k3[1])
        x = x + h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])/6
        y = y + h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])/6
        t = 0 + i * h
        i = i + 1
        """plot (t, w)"""
        xs.append(x)
        ys.append(y)
        ts.append(t)
    return

def main():
    # initialize pygame
    pygame.init()
    
    pygame.display.set_caption("Double Pendulum")
    
    #ticks
    clock = pygame.time.Clock()
    
    #get input
    print('Input mass 1:')
    m1 = input()
    print('Input line 1:')
    l1 = input()
    l1 = int(l1)
    print('Input mass 2:')
    m2 = input()
    print('Input line 2:')
    l2 = input()
    l2 = int(l2)
    print('Input theta 1 angle:')
    theta1 = input()
    theta1 = float(theta1) * (np.pi/180)
    print('Input theta 2 angle:')
    theta2 = input()
    theta2 = float(theta2) * (np.pi/180)
    print('Input g:')
    g = input()
    
    
    def velocitytheta1(t, theta1, theta2):
        return theta1

    def positiontheta1(t, theta1, theta2):
        return (-g*(m1 + m2 + m1)*np.sin(theta1) - m2*g*np.sin(theta1 - 2*theta2) - 2*np.sin(theta1 -theta2)*m2*(theta1**2*l1*np.cos(theta1 - theta2)+theta2**2 *l2)) / (l1(m1 + m2 +m1 - m2*np.cos(2*theta1 - 2*theta2)))

    def velocitytheta2(t, theta1, theta2):
        return theta2

    def positiontheta2(t, theta1, theta2):
        return (2*np.sin(theta1 - theta2)*((m1 + m2)* theta1**2 * l1 + g*(m1+m2)*np.cos(theta1) + theta2**2 * l2*m2*np.cos(theta1 - theta2))) / l2*((m1 + m2) + m1 - m2*np.cos(2*theta1 - 2*theta2))

    
    
    # main loop condition
    running = True 
    
    #font
    msg = pygame.font.Font('freesansbold.ttf',10)
    
    x1 = l1*np.sin(theta1)
    y1 = l1*np.cos(theta1)
    
    x2 = x1 + l2*np.sin(theta2)
    y2 = y1 + l2*np.cos(theta2)
    
    mass = Mass(int(x1), int(y1), 10, red)
    mass2 = Mass(int(x2), int(y2), 10, blue)
    
    tube1 = Tube((240 , 0), (mass2.x, mass2.y), black)
    tube2 = Tube((mass2.x, mass2.y), (mass.x, mass.y), green)
    
    ltext1 = msg.render("Length 1 = "+ str(int(l1)), 1, black)
    
    fps = 60
    
    ticksLastFrame = 0
    
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
                
        tube1.update(240, 0, mass2.x, mass2.y)
        tube2.update(mass2.x, mass2.y, mass.x, mass.y)
        
        #Render Code that will not change
        screen.blit(ltext1, (0, 10))
        screen.blit(deltaText, (0, 20))
        mass.display()
        mass2.display()
        tube1.display()
        tube2.display()
        
        pygame.display.flip()
        
        ticksLastFrame = time
                
    pygame.quit()
                
if __name__=="__main__":
    
    main()