import pygame
import random

pygame.font.init()


class Block:
    """This class helps in the placement of blocks on the grid
        e.g Block(5, 5) in snake body corresponds to a block placed
        at row 5 column 5 of the grid
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Block({self.x}, {self.y})'


class Food:
    def __init__(self, row, col, cellSize):
        """Creates random coordinates for the creation of the food block"""

        self.row = random.randint(0, row-1)
        self.col = random.randint(1, col-1)
        self.cellSize = cellSize

        # creates a new block object for the food
        self.block = Block(self.row, self.col)

    def drawFood(self, screen):
        # multiplying the x and y coords by the cellSWize to get correct positioning
        xPos = self.block.x * self.cellSize
        yPos = self.block.y * self.cellSize

        # food block color
        YELLOW = (255, 255, 0)

        # create and draw the food block
        rect = pygame.Rect(xPos, yPos, self.cellSize, self.cellSize)
        pygame.draw.rect(screen, YELLOW, rect)


class Snake:
    def __init__(self, cellSize):
        # Create a list of Blocks corresponding to the initial body state of the snake
        self.body = [Block(5, 5), Block(5, 6), Block(5, 7), Block(5, 8)]

        # initializing the snake direction
        self.direction = "DOWN"
        self.cellSize = cellSize

    def drawSnake(self, screen):
        # loop through every block in the snake body list and drawing them one by one
        for block in self.body:
            xPos = block.x * self.cellSize
            yPos = block.y * self.cellSize

            rect = pygame.Rect(xPos, yPos, self.cellSize, self.cellSize)
            pygame.draw.rect(screen, (255, 0, 0), rect)

    def moveSnake(self):
        # proceeding like this sinc the last element of the snake body list corresponds to the head
        # Hence the head's index is at position lenght-1

        length = len(self.body)
        head = self.body[length-1]

        # modifying the x and y coords according to the direction
        # recall adding y coord in pygame moves down and vice versa

        if self.direction == "DOWN":
            newHead = Block(head.x, head.y + 1)

        elif self.direction == "UP":
            newHead = Block(head.x, head.y - 1)

        elif self.direction == "LEFT":
            newHead = Block(head.x - 1, head.y)

        else:
            newHead = Block(head.x + 1, head.y)

        self.body.append(newHead)

    def eat(self, food, row, col, cellSize):
        length = len(self.body)
        head = self.body[length-1]

        # checking if the head coordinates corresponds to the food's coordinate
        if head.x == food.block.x and head.y == food.block.y:
            food.__init__(row, col, cellSize)
            return 1

        else:
            self.body.pop(0)
            return 0

    def die(self, row, col, cellSize):
        length = len(self.body)
        bodyBlocksExceptHead = self.body[:length-1]
        head = self.body[length-1]

        # looping through all the list except the head checking if the head intersects with any body block
        # if the head intersects with any then
        if any(block.x == head.x and block.y == head.y for block in bodyBlocksExceptHead):
            self.__init__(cellSize)
            return True

        # checking if the head's coords are out of the window bounds
        if head.x not in range(0, col) or head.y not in range(0, row):
            self.__init__(cellSize)
            return True

        return False


class Main:
    def __init__(self):
        # game constants
        self.col = 25
        self.row = 25
        self.cellSize = 20
        self.score = 0
        self.bestScore = 0

        # game resources (self.event is used to regulate snake's movement speed)
        self.screen = pygame.display.set_mode((self.col * self.cellSize, self.row * self.cellSize))
        self.event = pygame.USEREVENT
        self.font = pygame.font.SysFont('inkfree', 15, True)
        pygame.time.set_timer(self.event, 100)

        # instance of the food and snake classes
        self.food = Food(self.row, self.col, self.cellSize)
        self.snake = Snake(self.cellSize)

        # game regulators
        self.paused = False
        self.resetScore = False

        # load previous saved game state
        self.loadGameState()

    def showScores(self, screen):
        # display score and best score
        bestScoreText = self.font.render(f"Best Score: {self.bestScore}", True, (255, 255, 255))
        scoreText = self.font.render(f"Score: {self.score}", True, (255, 255, 255))

        screen.blit(bestScoreText, (400, 5))
        screen.blit(scoreText, (10, 5))

    def saveGameState(self):
        # save the game data to a file

        with open("data.txt", "w") as dat:
            dat.write("Best Score: " + str(self.bestScore) + "\n")
            dat.write("Current Score: " + str(self.score)+"\n")
            dat.write("Current Body: " + str(self.snake.body)+"\n")
            dat.write("Direction: " + str(self.snake.direction)+"\n")
            dat.write("Food xPos: " + str(self.food.block.x)+"\n")
            dat.write("Food yPos: " + str(self.food.block.y))

    def loadGameState(self):
        # load the game data from the file

        with open("data.txt", "r") as dat:
            data = dat.readlines()

            self.bestScore = int(data[0].split(": ")[1])
            self.score = int(data[1].split(": ")[1])
            self.snake.body = eval(data[2].split(": ")[1])
            self.snake.direction = data[3].split(": ")[1]
            self.food.block.x = int(data[4].split(": ")[1])
            self.food.block.y = int(data[5].split(": ")[1])

    def mainLoop(self):
        screen = self.screen
        running = True

        # mainloop
        while running:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.saveGameState()

                if event.type == self.event and not self.paused:
                    self.snake.moveSnake()
                    self.score += self.snake.eat(self.food, self.row, self.col, self.cellSize)
                    self.resetScore = self.snake.die(self.row, self.col, self.cellSize)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.paused:
                        if self.snake.direction != "RIGHT":
                            self.snake.direction = "LEFT"

                    if event.key == pygame.K_RIGHT and not self.paused:
                        if self.snake.direction != "LEFT":
                            self.snake.direction = "RIGHT"

                    if event.key == pygame.K_UP and not self.paused:
                        if self.snake.direction != "DOWN":
                            self.snake.direction = "UP"

                    if event.key == pygame.K_DOWN and not self.paused:
                        if self.snake.direction != "UP":
                            self.snake.direction = "DOWN"

                    if event.key == pygame.K_ESCAPE:
                        self.paused = True if not self.paused else False

            screen.fill((24, 110, 54))

            self.food.drawFood(screen)
            self.snake.drawSnake(screen)
            self.showScores(screen)

            if self.resetScore:
                if self.score > self.bestScore:
                    self.bestScore = self.score

                self.score = 0

            pygame.display.update()


main = Main()
main.mainLoop()
