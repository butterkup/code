#!/bin/python3

from random import choice
from copy import deepcopy

import tkinter
class Game_2048:
    def __init__(self) -> None:
        #start the game
        self.__createGameGui()
    GameOverLabel_bg='skyblue'
    ArrowIsVisible=False
    GameOverLabel_fg='black'
    score_fg='black'
    score_bg='white'
    GameBody_bg='saddlebrown'
    boxSize='25mm'
    ScoreValue=0
    BoxNumber=6
    colors={
        '0':['darkkhaki','black'],
        '2':['#eee4da','black'],
        '4':['#ede0c8','black'],
        '8':['#f2b179','black'],
        '16':['#f59563','white'],
        '32':['#f67c5f','white'],
        '64':['#f65e3b','white'],
        '128':['#edcf72','white'],
        '256':['#edcc61','white'],
        '512':['#edc850','lime'],
        '1024':['#edc53f','lime'],
        '2048':['#edc22e','lime']
    }
    EmptyMatrix=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    def __createGameGui(self):
        self.GUI=tkinter.Tk()
        self.GUI.wm_resizable(False, False)
        self.GUI.title('2048')
        self.GUI.config(width='15.7cm', height='17.3cm', bg=Game_2048.GameBody_bg)
        self.GameMatrix=deepcopy(Game_2048.EmptyMatrix)
        #top score tag name
        ScoreLabel=tkinter.Label(self.GUI, bg='lightblue', font=('monospace',30,'bold'), text='Score : ', anchor='w')
        ScoreLabel.place(x='0.1cm', y='0.1cm', width='5.1cm', height='1.5cm')
        #add arrow launcher
        self.AddExtraButtons=tkinter.Button(self.GUI,
                                            bg='navyblue',
                                            activebackground='lightblue',
                                            activeforeground='black',
                                            text='Arrows',
                                            fg='white',
                                            border=0,
                                            borderwidth=0,
                                            font=('monospace',20,'bold'),
                                            command=self.__addArrowButtons)
        self.AddExtraButtons.place(x='10.5cm', y='0.1cm', height='1.5cm', width='5.1cm')
        #top score holding tag
        self.Score=tkinter.Label(self.GUI, bg='lightpink', font=('freemono',30,'bold'), text=Game_2048.ScoreValue)
        self.Score.place(x='5.3cm', y='0.1cm', width='5.1cm', height='1.5cm')
        #store the __state of the game
        self.GameData=deepcopy(Game_2048.EmptyMatrix)
        #create and place the boxes on the main window
        Y=17
        for y in range(Game_2048.BoxNumber):
            X=1
            for x in range(Game_2048.BoxNumber):
                self.GameMatrix[y][x]=tkinter.Label(self.GUI, bg='black', fg='white', text='', font=('monospace',20,'bold'))
                self.GameMatrix[y][x].place(x=str(X)+'mm', y=str(Y)+'mm', height='25mm', width='25mm')
                X+=26
            Y+=26
        self.__BIND()
        #initialize game with two boxes having value of 2
        self.__addBoxValue()
        self.__addBoxValue()
        Game_2048.ScoreValue=0
        #update the changes
        self.__updateGUI()
        self.GUI.mainloop()

    def __addArrowButtons(self):
        Up=tkinter.Button(self.GUI,
                          text='Up',
                          bg='lime',
                          font=('freemono',20,'bold'),
                          border=0,
                          borderwidth=0,
                          command=self.__PushUp)
        Up.place(x='15.7cm', y='1.7cm', height='2.5cm', width='2.5cm')
        Left=tkinter.Button(self.GUI,
                            text='Left',
                            bg='lime',
                            font=('freemono',20,'bold'),
                            border=0,
                            borderwidth=0,
                            command=self.__PushLeft)
        Left.place(x='15.7cm', y='4.3cm', height='2.5cm', width='2.5cm')
        Down=tkinter.Button(self.GUI,
                            text='Down',
                            bg='lime',
                            font=('freemono',20,'bold'),
                            border=0,
                            borderwidth=0,
                            command=self.__PushDown)
        Down.place(x='15.7cm', y='6.9cm', height='2.5cm', width='2.5cm')
        Right=tkinter.Button(self.GUI,
                             text='Right',
                             bg='lime',
                             font=('freemono',20,'bold'),
                             border=0,
                             borderwidth=0,
                             command=self.__PushRight)
        Right.place(x='15.7cm', y='9.5cm', height='2.5cm', width='2.5cm')
        if Game_2048.ArrowIsVisible:
            self.GUI.config(width='15.7cm')
            Game_2048.ArrowIsVisible=False
        else:
            self.GUI.config(width='18.3cm')
            Game_2048.ArrowIsVisible=True

    def __GameOver(self, text):
        #display the game over tag, shows the value of text passed
        self.GameOverFrame=tkinter.LabelFrame(self.GUI, bg=Game_2048.GameBody_bg)
        self.GameOverFrame.place(x=0,rely=0.3, height='3.1cm', relwidth=1)
        GameOverLabel=tkinter.Label(self.GameOverFrame,
                                    text=text,
                                    bg=Game_2048.GameOverLabel_bg,
                                    fg=Game_2048.GameOverLabel_fg,
                                    font=('cursive', 20,'bold'))
        GameOverLabel.place(height='1.3cm', relwidth=1, x='0mm', y='1mm')
        RestartButton=tkinter.Button(self.GameOverFrame,
                                    command=self.__resetValues,
                                    borderwidth=0,
                                    border=0,
                                    fg='black', 
                                    bg='lime', 
                                    activebackground='blue',
                                    activeforeground='white',
                                    text='Restart',
                                    font=('monospace',15,'bold'))
        QuitButton=tkinter.Button(self.GameOverFrame, 
                                  command=self.GUI.destroy,
                                  border=0,borderwidth=0, 
                                  bg='lime', 
                                  fg='black',
                                  text='Quit',
                                  activeforeground='white', 
                                  activebackground='red',
                                  font=('monospace',15,'bold'))
        RestartButton.place(height='1.4cm', relwidth=0.5, x='0mm', y='1.5cm')
        QuitButton.place(height='1.4cm', relwidth=0.5, relx=0.5, y='1.5cm')
        #deativate the arrow key adder
        self.AddExtraButtons.config(state='disabled')
        self.GUI.config(width='15.7cm')
        self.__state()

    def __BIND(self):
        #add event listeners for the Left, Right, Up and Down keys
        self.GUI.bind('<Right>', lambda key: self.__PushRight())
        self.GUI.bind('<Left>', lambda key: self.__PushLeft())
        self.GUI.bind('<Up>', lambda key: self.__PushUp())
        self.GUI.bind('<Down>', lambda key: self.__PushDown())

    def __resetValues(self):
        #restart the game
        self.AddExtraButtons.config(state='active')
        self.GameData=deepcopy(Game_2048.EmptyMatrix)
        self.__addBoxValue()
        self.__addBoxValue()
        Game_2048.ScoreValue=0
        self.GameOverFrame.place(x='20cm')
        self.GUI.forget(self.GameOverFrame)
        self.__BIND()
        self.__updateGUI()

    def __PushLeft(self):
        #slide left and add value to a valueless box
        self.__rotateBack()
        self.__rotateBack()
        self.__slideRight()
        self.__rotateBack()
        self.__rotateBack()
        self.__addBoxValue()
        self.__updateGUI()

    def __PushUp(self,):
        #slide up and add value to a valueless box
        self.__rotateBack()
        self.__rotateBack()
        self.__rotateBack()
        self.__slideRight()
        self.__rotateBack()
        self.__addBoxValue()
        self.__updateGUI()

    def __PushDown(self):
        #slide down and add value to a valueless box
        self.__rotateBack()
        self.__slideRight()
        self.__rotateBack()
        self.__rotateBack()
        self.__rotateBack()
        self.__addBoxValue()
        self.__updateGUI()

    def __PushRight(self):
        #slide right and add value to a valueless box
        self.__slideRight()
        self.__addBoxValue()
        self.__updateGUI()

    def __slideRight(self):
        #slide self.GameData by -90 degrees
        self.__removeZeros()
        for row in self.GameData:
            preValue=-1
            for value in row:
                if value==preValue:
                    row[row.index(value)]=preValue*2
                    Game_2048.ScoreValue+=2
                    if value in row:
                        row.pop(row.index(value))
                    preValue=-1
                preValue=value
        self.insertZeros()

    def __SLIDERIGHT(self, matrix)->bool:
        #return true if it is possible to slide to the right of the passed matrix
        self.__removeZeros(matrix)
        for row in matrix:
            preValue=-1
            for value in row:
                if value==preValue:
                    return True
                preValue=value
        return False

    def __PUSHRIGHT(self):
        #is it possible to slide right? return true if possible else false
        matrix=deepcopy(self.GameData)
        if not(matrix is self.GameData):
            value=self.__SLIDERIGHT(matrix)
            return value
        print('[ ERROR ] matrix is self.GameData in __PUSHRIGHT')

    def __PUSHUP(self):
        #is it possible to slide up? return true if possible else false
        matrix=deepcopy(self.GameData)
        if not (matrix is self.GameData):
            matrix=self.__ROTATEBACK(matrix)
            matrix=self.__ROTATEBACK(matrix)
            matrix=self.__ROTATEBACK(matrix)
            value=self.__SLIDERIGHT(matrix)
            return value
        print('[ ERROR ] matrix is self.GameData in __PUSHUP')

    def __PUSHDOWN(self):
        #is it possible to slide down? return true if possible else false
        matrix=deepcopy(self.GameData)
        if not (matrix is self.GameData):
            matrix=self.__ROTATEBACK(matrix)
            value = self.__SLIDERIGHT(matrix)
            return value
        print('[ ERROR ] matrix is self.GameData in __PUSHDOWN')
    
    def __PUSHLEFT(self):
        #is it possible to slide left? return true if possible else false
        matrix=deepcopy(self.GameData)
        if not(matrix is self.GameData):
            matrix=self.__ROTATEBACK(matrix)
            matrix=self.__ROTATEBACK(matrix)
            value=self.__SLIDERIGHT(matrix)
            return value
        print('[ ERROR ] matrix is self.GameData in __PUSHLEFT')

    def __UNBIND(self):
        #release the arrow keys after the game is over
        self.GUI.unbind('<Right>')
        self.GUI.unbind('<Up>')
        self.GUI.unbind('<Down>')
        self.GUI.unbind('<Left>')

    def __addBoxValue(self):
        #if the game is over, free the keys, if not,
        #randomly pick an empty box and give it a value of two
        #and also append the score by 5
        ZeroBoxes=[]
        for y in range(Game_2048.BoxNumber):
            for x in range(Game_2048.BoxNumber):
                if self.GameData[y][x]>1048:
                    self.__GameOver('You WIN.')
                    self.__UNBIND()
                if self.GameData[y][x]==0:
                    ZeroBoxes.append((y,x))
        if len(ZeroBoxes):
            selectedBox=choice(ZeroBoxes)
            self.GameData[selectedBox[0]][selectedBox[1]]=2
        else:
            if self.IsGameOver():
                print('game over buddy')
                self.__GameOver('You LOSE.')
                self.__UNBIND()

    def __rotateBack(self):
        #rotate self.GameData by -90 degrees
        assert len(self.GameData)==Game_2048.BoxNumber, f"len(self.GameData) != 6 : current {self.GameData} has {len(self.GameData)} items"
        for row in self.GameData:
            assert len(row)==Game_2048.BoxNumber, f"len(self.GameData[{self.GameData.index(row)}]) != 6 : current {self.GameData[self.GameData.index(row)]} has {len(self.GameData[self.GameData.index(row)])} items"
        col1=[row[0] for row in self.GameData]
        col2=[row[1] for row in self.GameData]
        col3=[row[2] for row in self.GameData]
        col4=[row[3] for row in self.GameData]
        col5=[row[4] for row in self.GameData]
        col6=[row[5] for row in self.GameData]
        self.GameData=[col6,col5,col4,col3, col2, col1]

    def __ROTATEBACK(self, matrix):
        #rotate the passed 4x4 matrix by -90 degrees
        col1=[row[0] for row in matrix]
        col2=[row[1] for row in matrix]
        col3=[row[2] for row in matrix]
        col4=[row[3] for row in matrix]
        col5=[row[4] for row in matrix]
        col6=[row[5] for row in matrix]
        return [col6, col5, col4,col3, col2, col1]

    def __updateGUI(self):
        #update the changes of self.GameData to the screen
        for y in range(Game_2048.BoxNumber):
            for x in range(Game_2048.BoxNumber):
                data=self.GameData[y][x]
                if data==0:
                    self.GameMatrix[y][x]['text']=''
                else:
                    self.GameMatrix[y][x]['text']=data
        self.Score['text']=Game_2048.ScoreValue
        self.colorBoxes()

    def __removeZeros(self, matrix=0):
        #remove zeros from the matrix passed else from self.GameData
        if not matrix:
            matrix=self.GameData
        for index in range(Game_2048.BoxNumber):
            while matrix[index].count(0):
                matrix[index].remove(0)
                
    def insertZeros(self, matrix=0):
        #insert zeros to the matrix passed till it reaches a 4x4 matrix
        #else insert in self.GameData
        if not matrix:
            matrix=self.GameData
        self.__removeZeros(matrix)
        for index in range(Game_2048.BoxNumber):
            while len(matrix[index])<Game_2048.BoxNumber:
                matrix[index].insert(0,0)

    def IsGameOver(self)->bool:
        #check if possible to slide in any direction, if true then game is not over (return False),
        #else game is over (return True)
        if any([self.__PUSHUP(), self.__PUSHLEFT(), self.__PUSHDOWN(), self.__PUSHRIGHT()]):
            return False
        return True

    def __state(self):
        #represent the state of the game
        stringVersion=[]
        for line in self.GameData:
            strLine=[]
            for item in line:
                strLine.append(str(item).rjust(3,' '))
            stringVersion.append(strLine)
        for row in stringVersion: print(row)

    def colorBoxes(self):
        for y in range(Game_2048.BoxNumber):
            for x in range(Game_2048.BoxNumber):
                self.GameMatrix[y][x]['bg']=Game_2048.colors[str(self.GameData[y][x])][0]
                self.GameMatrix[y][x]['fg']=Game_2048.colors[str(self.GameData[y][x])][1]

if __name__=='__main__':
    Game_2048()
    
