import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication)

class Preprocess(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        rawFolder = QLabel('Raw Folder')
        xyResolu = QLabel('X-Y Resolution')
        zResolu = QLabel('Z Resolution')
        reduceRation = QLabel('Reduce Ratio')
        sliceNum = QLabel('Slice Num')
        maxTime = QLabel('Max Time')
        projectFolder = QLabel('Project Folder')
        lineageFile = QLabel('Lineage File')
        numberDict = QLabel('Number Dictionary')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(rawFolder, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(xyResolu, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(zResolu, 3, 0)
        grid.addWidget(reviewEdit, 3, 1)

        grid.addWidget(reduceRation, 4, 0)

        grid.addWidget(sliceNum, 5, 0)

        grid.addWidget(maxTime, 6, 0)

        grid.addWidget(projectFolder, 7, 0)

        grid.addWidget(lineageFile, 8, 0)

        grid.addWidget(numberDict, 9, 0)


        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()


if __name__ == '__main__':
    """单独看这个组件"""
    app = QApplication(sys.argv)
    ex = Preprocess()
    sys.exit(app.exec_())