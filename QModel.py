import numpy as np
import random
import pygame

import math as m

from Game import Game

class QModel:
    def __init__(self) -> None:
        self.hiddenLayers = 4
        self.weights = np.zeros((self.hiddenLayers,5))
        for i in range (0,5):
            for j in range (0,self.hiddenLayers):
                self.weights[j][i] = (random.random() * 4 - 2)
        self.bias = random.random() * 1000 - 5000

    def sigmoid(self, raw_output): 
        if raw_output > 2:
            return 1
        if raw_output < -2:
            return 0
        
        output = round(1/(1 + pow(2.7,-raw_output)))
        return output

    def run_model(self, playerY, ballX, ballY, bSpeedX, bSpeedY):
        _inputs = [playerY, ballX, ballY, bSpeedX, bSpeedY]
        raw_output = 0
        for i in range (0,5):
            for j in range (0,self.hiddenLayers):
                raw_output += self.weights[j][i] * pow(_inputs[i], j+1)
        raw_output += self.bias
        # print (raw_output)
        return round(self.sigmoid(raw_output))

    def train_model(self, x): #x is max frames reached previous generation
        if x <= -1:
            print("error occured")
        changeLimit = 1/(1+pow(2.7,((x-1000)/2000)))
        # print(changeLimit)
        for i in range(0,5):
            for j in range(0,self.hiddenLayers):
                self.weights[j][i] += changeLimit * (random.random() * 4 - 2)
        
        self.bias += changeLimit * (random.random() * 100 - 50)

    def save_model(self):
        textFile = open("QModel.txt", 'w')
        for i in range(0,5):
            for j in range (0,self.hiddenLayers):
                textFile.write(str(self.weights[j][i]) + "\n")
        textFile.write(str(self.bias))
        textFile.close

    
    def load_model(self, Model):
        textFile = open(Model, "r")
        for i in range (0,5):
            for j in range (0,self.hiddenLayers):
                self.weights[j][i] = float(textFile.readline())
        self.bias = float(textFile.readline())
        textFile.close
        return
    


def show_train(numModels, epochs):
    pygame.init()

    WIN_SCALE = 0.8  # Percentage of the screen given a 16*9 aspect ratio
    FPS = 60

    # Defining colours
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Defining the number of pixels for the screen 1920*1080 as a default for HD
    WIDTH, HEIGHT = 1080*WIN_SCALE, 1080*WIN_SCALE

    # Setup of the screen
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Setting up the clock to refresh the screen based on FPS
    clock = pygame.time.Clock()
    # make array of model objects
    modelARRAY = np.empty(numModels, dtype=QModel)

    for i in range (0, numModels):
        modelARRAY[i] = QModel()
    
    for i in range (0, epochs):
        print("epoch: " + str(i))
        
        # make an array of game objects that have the same starting ball velocities
        valuex = random.random() * 3
        Ball_velocity = [0,0]
        valuey = m.sqrt(-1 * pow(valuex,2) - (4*valuex) + 21)
        if round(random.random()) == 0:
            Ball_velocity = [2+ valuex, valuey]
        else:
            Ball_velocity = [2+ valuey, -valuey]

        gameARRAY = np.empty(numModels, dtype=Game)
        for j in range (0, numModels):
            gameARRAY[j] = Game()
            gameARRAY[j].Ball_velocity[0] = Ball_velocity[0]
            gameARRAY[j].Ball_velocity[1] = Ball_velocity[1]
        
        noCheck = []
        runCHECK = 1
        while runCHECK > 0:
            runCHECK = 0
            
            clock.tick(60)
            
            for j in range (0, numModels):
                if j not in noCheck:
                    gameARRAY[j].input(modelARRAY[j].run_model(gameARRAY[j].Player1_Rectange.y, gameARRAY[j].Ball_rectangle.x, gameARRAY[j].Ball_rectangle.y, gameARRAY[j].Ball_velocity[0], gameARRAY[j].Ball_velocity[1]), 1)
                    if gameARRAY[j].run_game() == 0:
                        noCheck.append(j)
                    
                    else:
                        runCHECK += 1
            
                    WIN.fill([0,0,0])
                    for j in range (0, numModels):
                        if j not in noCheck:
                            gameARRAY[j].drawGame(WIN)
                    pygame.display.update()
        
        bestFRAME = gameARRAY[0].maxFRAME * 2**((-1 *(abs((abs(gameARRAY[j].Player1_Rectange.y - 50)) - abs(gameARRAY[j].Ball_rectangle.y-10))))/50)

        bestNUM = 0
        for j in range (1, numModels):
            gameARRAY[j].maxFRAME = gameARRAY[j].maxFRAME * 2**((-1 *(abs((abs(gameARRAY[j].Player1_Rectange.y - 50)) - abs(gameARRAY[j].Ball_rectangle.y-10))))/200)
            if bestFRAME < gameARRAY[j].maxFRAME:
                bestFRAME = gameARRAY[j].maxFRAME
                bestNUM = j
            
        print(bestFRAME)
        modelARRAY[bestNUM].save_model()
        modelARRAY[0].load_model("QModel.txt")
        for j in range(1, numModels):
            modelARRAY[j].load_model("QModel.txt")
            modelARRAY[j].train_model(bestFRAME)

# no display
def train(numModels, epochs):
    # make array of model objects
    modelARRAY = np.empty(numModels, dtype=QModel)

    for i in range (0, numModels):
        modelARRAY[i] = QModel()
    
    for i in range (0, epochs):
        print("epoch: " + str(i))
        
        # make an array of game objects that have the same starting ball velocities
        valuex = random.random() * 3
        Ball_velocity = [0,0]
        valuey = m.sqrt(-1 * pow(valuex,2) - (4*valuex) + 21)
        if round(random.random()) == 0:
            Ball_velocity = [2+ valuex, valuey]
        else:
            Ball_velocity = [2+ valuey, -valuey]

        gameARRAY = np.empty(numModels, dtype=Game)
        for j in range (0, numModels):
            gameARRAY[j] = Game()
            gameARRAY[j].Ball_velocity[0] = Ball_velocity[0]
            gameARRAY[j].Ball_velocity[1] = Ball_velocity[1]
        
        noCheck = []
        runCHECK = 1
        while runCHECK > 0:
            runCHECK = 0
            for j in range (0, numModels):
                if j not in noCheck:
                    gameARRAY[j].input(modelARRAY[j].run_model(gameARRAY[j].Player1_Rectange.y, gameARRAY[j].Ball_rectangle.x, gameARRAY[j].Ball_rectangle.y, gameARRAY[j].Ball_velocity[0], gameARRAY[j].Ball_velocity[1]), 1)
                    if gameARRAY[j].run_game() == 0:
                        noCheck.append(j)
                    
                    else:
                        runCHECK += 1
        
        bestFRAME = gameARRAY[0].maxFRAME * 2**((-1 *(abs((abs(gameARRAY[j].Player1_Rectange.y - 50)) - abs(gameARRAY[j].Ball_rectangle.y-10))))/50)

        bestNUM = 0
        for j in range (1, numModels):
            gameARRAY[j].maxFRAME = gameARRAY[j].maxFRAME * 2**((-1 *(abs((abs(gameARRAY[j].Player1_Rectange.y - 50)) - abs(gameARRAY[j].Ball_rectangle.y-10))))/200)
            if bestFRAME < gameARRAY[j].maxFRAME:
                bestFRAME = gameARRAY[j].maxFRAME
                bestNUM = j
            
        print(bestFRAME)
        modelARRAY[bestNUM].save_model()
        modelARRAY[0].load_model("QModel.txt")
        for j in range(1, numModels):
            modelARRAY[j].load_model("QModel.txt")
            modelARRAY[j].train_model(bestFRAME)
