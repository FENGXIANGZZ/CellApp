import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

class Train(QWidget):

    def __init__(self):
        super().__init__()

        self.mainlayout = QVBoxLayout()  # 组件的整体布局是垂直布局,第一层是一个栅格放参数,第二层是个水平布局放进度条, 最下层是一个反馈信息栏

        self.initUI()  # 设置参数相关的各种组件位置

        self.middlelayout = QHBoxLayout()
        self.runtrainBtn = QPushButton("Start Training")
        self.runtrainBtn.clicked.connect(self.runTrain)
        self.stoptrainBtn = QPushButton("Stop Training")
        self.stoptrainBtn.clicked.connect(self.stopTrain)
        self.trainBar = QProgressBar()
        self.middlelayout.addWidget(self.runtrainBtn)
        self.middlelayout.addWidget(self.stoptrainBtn)
        self.middlelayout.addWidget(self.trainBar)
        self.mainlayout.addStretch(1)
        self.mainlayout.addLayout(self.middlelayout)

        self.textEdit = QTextEdit()  # 初始化反馈信息栏
        self.textEdit.setFocusPolicy(Qt.NoFocus)  # 将反馈信息栏设置为无法主动编辑
        self.mainlayout.addStretch(1)  # 将反馈信息栏压到垂直布局的底层
        self.mainlayout.addWidget(self.textEdit)  # 将反馈信息栏添加到整体布局中

        self.setLayout(self.mainlayout)  # 将Preprocess这个分组件应用上设置好的整体布局
        self.setGeometry(300, 300, 450, 500)
        self.show()


    def initUI(self):
        # 栅格布局第一列是参数名称
        dataFolder = QLabel('Data Folder')
        saveFolder = QLabel('Save Folder')
        dataNames = QLabel('Data Names')
        batchSize = QLabel('Batch Size')
        modelName = QLabel('Model Name')
        # 栅格布局第二列是参数输入框
        self.dataFolderEdit = QLineEdit()
        self.saveFolderEdit = QLineEdit()
        self.batchSizeEdit = QLineEdit()
        self.modelNameEdit = QLineEdit()
        # 栅格布局第三列是参数选择按钮
        dataFolderBtn = QPushButton("Select")
        dataFolderBtn.clicked.connect(self.chooseDataFolder)
        self.dataNamesBtn = QComboBox()
        saveFolderBtn = QPushButton("Select")
        saveFolderBtn.clicked.connect(self.chooseSaveFolder)

        grid = QGridLayout()
        grid.setSpacing(30)

        grid.addWidget(dataFolder, 1, 0)
        grid.addWidget(self.dataFolderEdit, 1, 1)
        grid.addWidget(dataFolderBtn, 1, 2)

        grid.addWidget(dataNames, 2, 0)
        grid.addWidget(self.dataNamesBtn, 2, 1)

        grid.addWidget(saveFolder, 3, 0)
        grid.addWidget(self.saveFolderEdit, 3, 1)
        grid.addWidget(saveFolderBtn, 3, 2)

        grid.addWidget(batchSize, 4, 0)
        grid.addWidget(self.batchSizeEdit, 4, 1)

        grid.addWidget(modelName, 5, 0)
        grid.addWidget(self.modelNameEdit, 5, 1)

        self.mainlayout.addLayout(grid)

    def chooseDataFolder(self):
        pass

    def chooseSaveFolder(self):
        pass

    def runTrain(self):
        pass

    def stopTrain(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Train()
    sys.exit(app.exec_())