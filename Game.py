import numpy as np
import random
import pygame
import math as m

class Game:
    def __init__(self) -> None:
        self.maxFRAME = 0

        self.WIN_SCALE = 0.8
        self.FPS = 60

        # Defining colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Defining the number of pixels for the screen 1920*1080 as a default for HD
        self.WIDTH, self.HEIGHT = 1080*self.WIN_SCALE, 1080*self.WIN_SCALE

        # Setting up the clock to refresh the screen based on FPS
        self.clock = pygame.time.Clock()

        # Defining the ball's initial velocity
        valuex = random.random() * 3
        valuey = m.sqrt(25-pow((2+valuex),2))
        if round(random.random()) == 0:
            self.Ball_velocity = [2+ valuex, valuey]
        else:
            self.Ball_velocity = [2+ valuex, -valuey]

        # Defining the player's velocity (only an integer as velocity only has vertical component)
        self.Player1_Velocity = 7
        self.Player2_Velocity = 7

        # Determines how much the ball speeds up every time it is hit by a player
        self.Game_Speed = 0.5

        # Defining the rectangles for the two players
        self.Player1_Rectange = pygame.Rect(10, self.HEIGHT//2 - 50, 10, 100)
        self.Player2_Rectange = pygame.Rect(self.WIDTH - 20, self.HEIGHT//2 - 50, 10, 100)

        # Defining the ball rectangle
        self.Ball_rectangle = pygame.Rect(
            self.WIDTH//2 - 5 + self.Ball_velocity[0], self.HEIGHT//2 - 5 + self.Ball_velocity[1], 10, 10)

    def input(self, INPUT, auto):
        #AI CONTROLS PLAYER 1
        
        if INPUT == 1 and self.Player1_Rectange.y > 0:
                self.Player1_Rectange.y -= self.Player1_Velocity
        if INPUT == 0 and self.Player1_Rectange.y < self.HEIGHT - 100:
                self.Player1_Rectange.y += self.Player1_Velocity
        

        if auto == 1:
            self.Player2_Rectange.y = self.Ball_rectangle.y -50
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            keys_pressed = pygame.key.get_pressed()	
            if keys_pressed[pygame.K_w] and self.Player2_Rectange.y > 0:
                self.Player2_Rectange.y -= self.Player1_Velocity
                

            if keys_pressed[pygame.K_s] and self.Player2_Rectange.y < self.HEIGHT - 100:
                self.Player2_Rectange.y += self.Player2_Velocity	
                

        # #AI CONTROLS PLAYER 2
        # if INPUT == 1 and self.Player2_Rectange.y > 0:
        #     self.Player2_Rectange.y -= self.Player2_Velocity
        # if INPUT == 0 and self.Player2_Rectange.y < HEIGHT - 100:
        #     self.Player2_Rectange.y += self.Player2_Velocity
        
        # self.Player1_Rectange.y = self.Ball_rectangle.y

    def run_game(self):
		# This will make the ball rebound off the side walls (leave off for regular gameplay)
		# if Ball_rectangle.x <= 0 or Ball_rectangle.x + 10 >= WIDTH:
		# 	Ball_velocity[0] = -Ball_velocity[0]		

		# Conditional processes rebounts off the top and bottom of the screen
        if self.Ball_rectangle.y <= 0 or self.Ball_rectangle.y + 10 >= self.HEIGHT:
            self.Ball_velocity[1] = -self.Ball_velocity[1]

        # Adds the initial velocity vector to the ball's position each frame creating movement
        self.Ball_rectangle.x += self.Ball_velocity[0]
        self.Ball_rectangle.y += self.Ball_velocity[1]

        # Conditional processes rebounts off the player's paddles
        if self.Ball_rectangle.colliderect(self.Player1_Rectange):
            self.Ball_velocity[0] = abs(self.Ball_velocity[0]) * 1.1
            self.Ball_velocity[1] = self.Ball_velocity[1] * 1.1
        
        if self.Ball_rectangle.colliderect(self.Player2_Rectange):
            self.Ball_velocity[0] = -abs(self.Ball_velocity[0]) * 1.1
            self.Ball_velocity[1] = self.Ball_velocity[1] * 1.1


        if self.Ball_rectangle.x < 5: # was -60 set to 10 for training purposes
            return 0

        elif self.Ball_rectangle.x > self.WIDTH + 50:
            return 0
        
        self.maxFRAME += 1
        return 1
    
    def drawGame(self, WIN):
        # Draws all game objects on the screen
        pygame.draw.rect(WIN, self.WHITE, self.Player1_Rectange)
        pygame.draw.rect(WIN, self.WHITE, self.Player2_Rectange)
        pygame.draw.rect(WIN, self.WHITE, self.Ball_rectangle)

    