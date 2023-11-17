# PongAI
## Overview
This project was the product of a competition between a few of my peers to produce AIs for pong and see who could make the best (make them vs each other). Unfortunately I was the only person to produce a final product so I cannot say whether mine preformed the best (although I guess it did win by default?). My methodology and techniques used are extremely rudimentary and were based on extremely limited research, hence, there is significant room for improvement.

The project is made using python and the following libraries:
  - Numpy
  - Pygame
  - Math
  - Random

I feel as thought his project taught me a lot, however, much of it was basics of project management, planning and basic coding principals rather than AI building. It was a lot of fun to make and feel free to give it a test. Simply run the "ModelShowase.py" file, you can also train up a new AI and watch the training process using the "main.py" file (uncomment some of the code to watch the process).


## Methodology
### Model Input to Output
The rules of the competition allowed for access to your paddles y-coordinate, the balls coordinates (x,y) and the balls velocity vectory (x,y). Hence, the model will take in 5 inputs. My goal was to create an AI that would take in these 5 inputs and output a singular boolean value (1 go up, 0 go down). Hence, using my extremely flawed and gap filled understanding of what an AI is and how it works I produced a model.

My model consists of an array of N rows and 5 columns with N being the number of 'hidden layers' (or at least thats what I am refering to them as) this array holds all the weights which is initialised as a bunch of random numbers, there is then an additional variable "Bias". As any function can (to a degree) be represented by a polynomial function and an AI is basically a complex function that can convert these inputs into the desired output:

I decided that I would sum each weight * the input value ^ the row (hidden layer), and then add the bias. The result of this sum would then be thrown into a sigmoid function to produce a value between 0 and 1 and then rounded in order to aquire the boolean output that is desired.

### Model Training
In order to train the model and improve it I construct an array of models and simulate hundrends of games of pong taking note of how long the games lasted. The games have another paddle that is having its y-coordinate set to that of the ball. Once all the games end I find the model that acheived the best result and populate the other models with its weights +- a random amount. This random amount shrinks as the epoch increases in order to refine the model further as time progresses. This makes the evaluation of the model not care whether they win/lose but rather just how long the game lasts. Once training is completed the weights and bias are then saved into a txt file in order to be loaded later.




  
