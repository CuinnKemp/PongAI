import numpy as np
import pygame

from Game import Game

from QModel import QModel

# Setting up model being tested
autoPlay = True;
model = QModel()

model.load_model("QModel (50,10)(4layers).txt") # change this value to use a different model


# set up pygame main window
pygame.init()

FPS = 60
clock = pygame.time.Clock()

# Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

info = pygame.display.Info()
SIZE = MWIDTH, MHEIGHT = info.current_w, info.current_h-info.current_h*0.05
MainWIN = pygame.display.set_mode(SIZE)

# Defining the number of pixels for the screen 1920*1080 as a default for HD
WIDTH, HEIGHT = 1080*0.8, 1080*0.8

# Setup Game surface
WIN = pygame.Surface((WIDTH, HEIGHT))

# set up surface for data display

# Setup data surfaces

Data1WIN = pygame.Surface((3000,model.hiddenLayers*90))

Data2WIN = pygame.Surface((1000,1000))
InstructionsWin = pygame.Surface((1050,800))

font = pygame.font.SysFont(None, 40)

previousOutputs = np.empty(30, dtype = str)
PlayerScore = 0
AIScore = 0
# main loop
testing = True
while testing == True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                testing = False
    # inisialize a game
    game = Game()
    # create while loop
    run = True
    while run == True:
        # check if window has been closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                testing = False
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    match autoPlay:
                        case False:
                            autoPlay = True
                        case True:
                            autoPlay = False
        
        # wait for clock tick
        clock.tick(FPS)

        # move paddles (ai and player)
        
        modelOutput = model.run_model(game.Player1_Rectange.y, game.Ball_rectangle.x, game.Ball_rectangle.y, game.Ball_velocity[0], game.Ball_velocity[1])
        game.input(modelOutput, autoPlay)

        # if game has been lost (either player or ai) exit loop
        if game.run_game() == 0:
            if game.Ball_rectangle.x > (1080*0.8)/2:
                AIScore += 1
            else:
                PlayerScore += 1
            run = False

        # clear main window
        MainWIN.fill(BLACK)
        
        # draw game window
        WIN.fill(BLACK)
        game.drawGame(WIN)
        pygame.draw.rect(WIN, (0,255,0), pygame.Rect(0,0,WIDTH,HEIGHT),  2)
        MainWIN.blit(pygame.transform.scale(WIN, (MWIDTH/2,(MHEIGHT*2)/3)),(0,0))

        # draw data1 window
        Data1WIN.fill(BLACK)
        text = font.render("Weights: ", True, (0, 255, 0))
        Data1WIN.blit(text, (20, 20))
        for i in range (0,model.hiddenLayers):
            RawData =  str(model.weights[i][0]) + " * " + str(game.Player1_Rectange.y) + "^" + str(i+1) + " | " + str(model.weights[i][1]) + " * " +str(game.Ball_rectangle.x) + "^" + str(i+1) + " | " + str(model.weights[i][2]) + " * " + str(game.Ball_rectangle.y) + "^" + str(i+1) + " | " +  str(model.weights[i][3]) + " * " + str(game.Ball_velocity[0]) + "^" + str(i+1) + " | " + str(model.weights[i][3]) + " * " + str(game.Ball_rectangle.y) + "^" + str(i+1) + " | " +  str(model.weights[i][4]) + " * " + str(game.Ball_velocity[1]) + "^" + str(i+1) 
            text = font.render(RawData, True, (0, 255, 0))
            Data1WIN.blit(text, (20, 50+ (30 * i)))
        text = font.render("Bias: ", True, (0, 255, 0))
        Data1WIN.blit(text, (20, 50+ (30 * model.hiddenLayers)))
        text = font.render(str(model.bias), True, (0, 255, 0))
        Data1WIN.blit(text, (20, 50+ (30 * (model.hiddenLayers+1))))
        MainWIN.blit(pygame.transform.scale(Data1WIN, (MWIDTH,(MHEIGHT)/3)),(0,(MHEIGHT*2)/3))

        #draw data2 window
        Data2WIN.fill(BLACK)
        score = font.render(("Score: " + str(AIScore) + " : " + str(PlayerScore)), True, (0, 255, 0))
        Data2WIN.blit(score, (20, 20))
        
        text = font.render("Previous Outputs:", True, (0, 255, 0))
        Data2WIN.blit(text, (20, 50))
        for i in range (0,29):
            previousOutputs[i] = previousOutputs[i+1]
            text = font.render(str(previousOutputs[i]), True, (0, 255, 0))
            Data2WIN.blit(text, (20, 80 + (30 * i)))
        previousOutputs[29] = str(modelOutput)
        text = font.render(str(previousOutputs[29]), True, (0, 255, 0))
        Data2WIN.blit(text, (20, 80 + (30 * 9)))
        MainWIN.blit(pygame.transform.scale(Data2WIN, (MWIDTH/2,(MHEIGHT*2)/3)),(MWIDTH/2,0))

        # draw instructions window
        InstructionsWin.fill(BLACK);
        text = font.render(("This is an extremely basic pong AI."), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 20))
        text = font.render(("The paddle on the left is controlled by the AI."), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 50))
        text = font.render(("The paddle on the right is controlled by you,"), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 80))
        text = font.render(("or is having its y-coord set to the balls (auto play)."), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 110))
        text = font.render(("To read more about how it works see my GitHub"), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 140))
        text = font.render(("https://github.com/CuinnKemp"), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 170))

        text = font.render(("Auto Play: " + str(autoPlay)), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 220))
        text = font.render(("Toggle Auto Play by pressing 'T'."), True, (0, 255, 0))
        InstructionsWin.blit(text, (0, 250))
        

        MainWIN.blit(pygame.transform.scale(InstructionsWin, (MWIDTH/2,(MHEIGHT*2)/3)),(MWIDTH/1.5,0))

        # update display
        pygame.display.update()