from bangtal import *
from enum import Enum

# Game Options
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

# scene
scene = Scene('odello', 'Images/background.png')

class Turn(Enum):
    BLACK = '흑색'
    WHITE = '백색'
now_turn = Turn.BLACK

class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 3
    WHITE = 4

class Stone(Object):
    def __init__(self, x, y, file):
        super().__init__(file)
        self.state = State.BLANK
        self.x = x
        self.y = y

    def change_state(self, new_state):
        self.state = new_state

    def onMouseAction(self, x, y, action):
        global now_turn, POSSIBLE_COUNT

        if not (self.state == State.POSSIBLE):
            return

        if now_turn == Turn.BLACK:
            self.setImage('Images/black.png')
            self.change_state(State.BLACK)
        else:
            self.setImage('Images/white.png')
            self.change_state(State.WHITE)

        change_Stones(self.x, self.y)
        count_Stones()

        change_turn()
        show_Possible()
        
        print(WHITE_POSSIBLE_DICT)

        if POSSIBLE_COUNT == 0:
            if now_turn == Turn.BLACK:
                showMessage('{0}돌을 둘 수 있는 곳이 없어 {1}돌로 자동으로 턴이 넘어갑니다.'.format(Turn.BLACK.value, Turn.WHITE.value))
            else:
                showMessage('{0}돌을 둘 수 있는 곳이 없어 {1}돌로 자동으로 턴이 넘어갑니다.'.format(Turn.WHITE.value, Turn.BLACK.value))
            change_turn()
            show_Possible()

            if POSSIBLE_COUNT == 0:
                showMessage('게임 종료')

Stones = []
POSSIBLE_COUNT = 0
WHITE_POSSIBLE_DICT = {}

def change_turn():
    global now_turn
    if now_turn == Turn.BLACK:
        now_turn = Turn.WHITE
    else:
        now_turn = Turn.BLACK

def create_Stones():
    global Stones
    for i in range(8):
        arr = []
        for j in range(8):
            stone = Stone(i, j, 'Images/blank.png')
            #for test
            #stone = Stone('Images/black.png')
            stone.locate(scene, 40 + 80 * j, 40 + 80 * i)
            stone.show()
            arr.append(stone)
        Stones.append(arr)
    Stones[3][3].setImage('Images/black.png')
    Stones[3][3].change_state(State.BLACK)
    Stones[4][4].setImage('Images/black.png')
    Stones[4][4].change_state(State.BLACK)

    Stones[4][3].setImage('Images/white.png')
    Stones[4][3].change_state(State.WHITE)
    Stones[3][4].setImage('Images/white.png')
    Stones[3][4].change_state(State.WHITE)

def show_Possible():
    global now_turn, Stones, POSSIBLE_COUNT, WHITE_POSSIBLE_DICT

    moveX = [1, 1, 1, 0, -1, -1, -1, 0]
    moveY = [1, 0, -1, -1, -1, 0, 1, 1]

    POSSIBLE_COUNT = 0
    WHITE_POSSIBLE_DICT.clear()

    for x in range(8):
        for y in range(8):
            if Stones[x][y].state == State.POSSIBLE:
                Stones[x][y].change_state(State.BLANK)
                Stones[x][y].setImage('Images/blank.png')

    if now_turn == Turn.BLACK:

        for x in range(8):
            for y in range(8):

                if Stones[x][y].state == State.BLACK:
                    for step in range(len(moveX)):
                        newX = x + moveX[step]
                        newY = y + moveY[step]

                        if newX >= 0 and newX < 8 and newY >= 0 and newY < 8 and Stones[newX][newY].state == State.WHITE:
                            isOutBounded = False

                            while Stones[newX][newY].state == State.WHITE:
                                newX += moveX[step]
                                newY += moveY[step]


                                if newX < 0 or newX >= 8 or newY < 0 or newY >= 8:
                                    isOutBounded = True
                                    break
                                
                            # 찾았을때
                            if (not isOutBounded) and Stones[newX][newY].state == State.BLANK:
                                Stones[newX][newY].change_state(State.POSSIBLE)
                                Stones[newX][newY].setImage('Images/black possible.png')
                                POSSIBLE_COUNT += 1

    else: # WHITE turn
        for x in range(8):
            for y in range(8):

                if Stones[x][y].state == State.WHITE:
                    for step in range(len(moveX)):
                        newX = x + moveX[step]
                        newY = y + moveY[step]

                        if newX >= 0 and newX < 8 and newY >= 0 and newY < 8 and Stones[newX][newY].state == State.BLACK:
                            isOutBounded = False
                            count = 0
                            while Stones[newX][newY].state == State.BLACK:
                                newX += moveX[step]
                                newY += moveY[step]
                                count += 1

                                if newX < 0 or newX >= 8 or newY < 0 or newY >= 8:
                                    isOutBounded = True
                                    break
                                
                            # 찾았을때
                            if (not isOutBounded) and (Stones[newX][newY].state == State.BLANK or Stones[newX][newY].state == State.POSSIBLE):
                                if Stones[newX][newY].state == State.BLANK:
                                    POSSIBLE_COUNT += 1
                                    Stones[newX][newY].change_state(State.POSSIBLE)
                                    Stones[newX][newY].setImage('Images/white possible.png')
                                
                                if (newX, newY) in WHITE_POSSIBLE_DICT:
                                    WHITE_POSSIBLE_DICT[(newX, newY)] = WHITE_POSSIBLE_DICT.get((newX, newY)) + count
                                else:
                                    WHITE_POSSIBLE_DICT[(newX, newY)] = count

def change_Stones(x, y):
    global Stones

    moveX = [1, 1, 1, 0, -1, -1, -1, 0]
    moveY = [1, 0, -1, -1, -1, 0, 1, 1]

    if now_turn == Turn.BLACK:
        for step in range(len(moveX)):
            newX = x + moveX[step]
            newY = y + moveY[step]

            if newX >= 0 and newX < 8 and newY >= 0 and newY < 8 and Stones[newX][newY].state == State.WHITE:
                isOutBounded = False

                while Stones[newX][newY].state == State.WHITE:
                    newX += moveX[step]
                    newY += moveY[step]

                    if newX < 0 or newX >= 8 or newY < 0 or newY >= 8:
                        isOutBounded = True
                        break
                # 찾았을때
                if (not isOutBounded) and Stones[newX][newY].state == State.BLACK:
                    while newX != x or newY != y:
                        Stones[newX][newY].change_state(State.BLACK)
                        Stones[newX][newY].setImage('Images/black.png')
                        newX += moveX[step] * (-1)
                        newY += moveY[step] * (-1)
    
    else: # WHITE TURN
        for step in range(len(moveX)):
            newX = x + moveX[step]
            newY = y + moveY[step]

            if newX >= 0 and newX < 8 and newY >= 0 and newY < 8 and Stones[newX][newY].state == State.BLACK:
                isOutBounded = False

                while Stones[newX][newY].state == State.BLACK:
                    newX += moveX[step]
                    newY += moveY[step]

                    if newX < 0 or newX >= 8 or newY < 0 or newY >= 8:
                        isOutBounded = True
                        break
                # 찾았을때
                if (not isOutBounded) and Stones[newX][newY].state == State.WHITE:
                    while newX != x or newY != y:
                        Stones[newX][newY].change_state(State.WHITE)
                        Stones[newX][newY].setImage('Images/white.png')
                        newX += moveX[step] * (-1)
                        newY += moveY[step] * (-1)

def count_Stones():
    global Stones, black_num1, black_num2, white_num1, white_num2

    black_count = 0
    white_count = 0

    for x in range(8):
        for y in range(8):
            if Stones[x][y].state == State.BLACK:
                black_count += 1
            elif Stones[x][y].state == State.WHITE:
                white_count += 1
            else:
                continue
   
    black_num1.setImage('Images/L{}.png'.format(black_count//10))
    black_num2.setImage('Images/L{}.png'.format(black_count%10))
    white_num1.setImage('Images/L{}.png'.format(white_count//10))
    white_num2.setImage('Images/L{}.png'.format(white_count%10))



black_num1 = Object('Images/L0.png')
black_num1.locate(scene, 750, 220)
black_num1.show()
black_num2 = Object('Images/L2.png')
black_num2.locate(scene, 830, 220)
black_num2.show()

white_num1 = Object('Images/L0.png')
white_num1.locate(scene, 1070, 220)
white_num1.show()
white_num2 = Object('Images/L2.png')
white_num2.locate(scene, 1150, 220)
white_num2.show()


create_Stones()
show_Possible()
count_Stones()


startGame(scene)
