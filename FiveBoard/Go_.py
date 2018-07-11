import sys
import random
import math
from Board import board
from PyQt5 import QtCore,QtGui,QtWidgets
from UI.boardMain import Ui_MainWindow
from UI.LE import Ui_LengthEdit
from PyQt5.QtMultimedia import QMediaPlayer ,QMediaContent

TFdic = {True: '白', False: '黑'}


class lengthEdit(QtWidgets.QDialog, Ui_LengthEdit):
    """
    This is a modal dialog created initially,
    to determine the size of the board and how many lines need to draw

    It has two buttons:
    accept, reject

    It has a comboBox to edit length and as a return.
    """
    def __init__(self,parent = None):
        super(lengthEdit, self).__init__(parent)
        self.setupUi(self)
        self.acceptButton.clicked.connect(self.accept)
        self.rejectButton.clicked.connect(self.reject)


class chessLabel(QtWidgets.QLabel):
    """
    This is the label to show the chess, and there are many labels stored in a list,
    so after one turn the label become unchangable
    Its size was determined by the parameter length, and color by para color
    """
    def __init__(self, length, parent = None):
        super(chessLabel,self).__init__(parent)
        self.size = length
        self.resize(self.size*0.9,self.size*0.9)

    def paintLabel(self,color):
        self.setStyleSheet("border-image:url(:/chess/%s.png)"%color)


class boardWidget(QtWidgets.QWidget):
    """
    This is to draw a board with the size of para length,
    func: paintEvent(self,event)
    """
    def __init__(self, length, parent = None):
        super(boardWidget,self).__init__(parent)
        self.parent = parent
        self.length = length
        self.chessBox = []
        self.size = 720//length
        self.resize(730, 730)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.begin(self)
        self.drawLines(event,painter)
        painter.end()

    def drawLines(self, event, painter):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(0, 0, 730, 0)
        painter.drawLine(0, 0, 0, 730)
        painter.drawLine(0, 730, 730, 730)
        painter.drawLine(730, 0, 730, 730)
        '''lines'''
        for i in range(720//self.length+1):
            painter.drawLine(5, 5+i*720//self.length, 725, 5+i*720//self.length)
            painter.drawLine(5+i*720//self.length, 5, 5+i*720//self.length, 725)
        pen = QtGui.QPen(QtCore.Qt.black, 9, QtCore.Qt.SolidLine)

        '''center point'''
        painter.setPen(pen)
        painter.drawPoint(365, 365)

    def mousePressEvent(self, QMouseEvent):
        '''Only when the pressed position is not farther than 0.3*size from one center'''
        self.currentX = QMouseEvent.x()
        self.currentY = QMouseEvent.y()
        self.absX = None
        self.absY = None
        if ((self.currentX-5) % self.size) <= 0.35*self.size:
            self.absX = (self.currentX-5)//self.size*self.size+5
        elif (math.ceil((self.currentX-5)/self.size)-(self.currentX-5)/self.size) <= 0.35:
            self.absX = math.ceil((self.currentX-5)/self.size)*self.size+5
        if ((self.currentY-5) % self.size) <= 0.35*self.size:
            self.absY = (self.currentY-5)//self.size*self.size+5
        elif (math.ceil((self.currentY-5)/self.size)-(self.currentY-5)/self.size) <= 0.35:
            self.absY = math.ceil((self.currentY-5)/self.size)*self.size+5
        if self.absX is not None and self.absY is not None:
            self.parent.setChess((self.absX-5)//self.size, (self.absY-5)//self.size)

    def showLabel(self, color):
        self.currentChess = chessLabel(self.size, self)
        self.currentChess.paintLabel(color)
        self.currentChess.setGeometry(QtCore.QRect(
            self.absX-self.size*0.45, self.absY-self.size*0.45, self.size*0.9, self.size*0.9))
        self.currentChess.show()
        self.chessBox.append(self.currentChess)


class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    """
    So this is the main window class in which an instance of board lies

    It has several child windows:
    LengthEdit(determine the length and keep it, SureToLeave)

    It has four buttons:
    regret, surrender, exit, replay.

    The board widgets is redefined outside and created instance here(not initially but after editing length).
    """
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.LengthEdit = lengthEdit(self)
        if self.LengthEdit.exec_():
            self.length = int(self.LengthEdit.comboBox.currentText().split('*')[0])
            if self.LengthEdit.timeBox.currentText().isdigit():
                self.timeLimit = int(self.LengthEdit.timeBox.currentText())
            else:
                self.timeLimit = float('inf')
        else:
            exit(0)

        self.cnt = 0
        self.board = board(self.length+1)
        self.steps = self.board.steps
        self.colors = ['black', 'white']
        self.initWidgets()
        self.lastStep = (None, None)
        self.timer = QtCore.QTimer(self)
        if self.timeLimit < 60:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.timeOut)
            self.timer.start(1000)

        file = "src\\down.mp3"
        music = QMediaContent(QtCore.QUrl.fromLocalFile(file))
        self.player = QMediaPlayer()
        self.player.setMedia(music)

        self.replayButton.clicked.connect(self.replay)
        self.ExitButton.clicked.connect(self.close)
        self.regretButton.clicked.connect(self.regret)
        self.surrenderButton.clicked.connect(self.surrender)

    def initWidgets(self):
        self.boardWidget = boardWidget(self.length, self)
        self.boardWidget.setGeometry(QtCore.QRect(20, 20, 730+(-1.6*self.length+55), 730+(-1.6*self.length+55)))
        self.updateUi()

    def regret(self):
        try:
            self.board.regret()
            self.boardWidget.chessBox[-1].setStyleSheet("")
            self.boardWidget.chessBox.pop()
        except ValueError:
            pass
        else:
            self.steps -= 1
        finally:
            self.updateUi()

    def setChess(self, x, y):
        try:
            self.board.step(self.colors[self.steps%2], [x, y])
        except EOFError as e:
            print(e)
        except ValueError as e:
            print(e)
        else:
            self.player.play()
            self.boardWidget.showLabel(self.colors[self.steps %2])
            self.steps += 1
            self.cnt = 0
        self.checkWinner()
        self.updateUi()

    def surrender(self):
        self.timer.stop()
        self.boardWidget.setEnabled(False)
        self.winnerLabel.setText ("%s方胜"%TFdic[False if self.steps % 2 else True])

    def checkWinner(self):
        self.board.setWinner()
        if self.board.winner is not None:
            self.boardWidget.setEnabled(False)
            self.timer.stop()
            self.winnerLabel.setText("%s方胜"%TFdic[self.board.winner])

    def randomStep(self):
        while True:
            rX = random.randint(0, self.length)
            rY = random.randint(0, self.length)
            self.boardWidget.absX = 5 + rX * self.boardWidget.size
            self.boardWidget.absY = 5 + rY * self.boardWidget.size
            try:
                self.setChess(rX, rY)
            except EOFError:
                continue
            else:
                break

    def timeOut(self):
        """
        If the cnt of the timer is more than limit,then choose a random step
        """
        self.cnt += 1
        self.updateUi()
        if self.cnt >= self.timeLimit:
            self.cnt = 0
            self.randomStep()

    def updateUi(self):
        self.countdownLabel.setText(str(self.timeLimit-self.cnt))
        self.turnLabel.setText("%s方回合" % TFdic[True if self.steps % 2 else False])
        self.stepsLabel.setText("回合数:%d" % self.steps)

    def replay(self):
        Main = MainWindow()
        Main.show()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Main = MainWindow()
    Main.show()
    sys.exit(app.exec_())

