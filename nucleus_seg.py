import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

class Nucleus_Segmentation(QWidget):

    def __init__(self):
        super().__init__()

        self.mainlayout = QVBoxLayout()  # 组件的整体布局是垂直布局,第一层是一个栅格放参数,第二层是个水平布局放进度条, 最下层是一个反馈信息栏

        self.initUI()  # 设置参数相关的各种组件位置

        self.middlelayout = QHBoxLayout()
        self.runsegmentBtn = QPushButton("Run Segmentation")
        self.runsegmentBtn.clicked.connect(self.runSegmentation)
        self.stopsegmentBtn = QPushButton("Stop Segmentation")
        self.stopsegmentBtn.clicked.connect(self.stopSegmentation)
        self.segmentBar = QProgressBar()
        self.middlelayout.addWidget(self.runsegmentBtn)
        self.middlelayout.addWidget(self.stopsegmentBtn)
        self.middlelayout.addWidget(self.segmentBar)
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
        projectFolder = QLabel('Project Folder')
        embryoNames = QLabel('Embryo Names')
        maxTime = QLabel('Max Time')
        batchSize = QLabel('Batch Size')
        lineageFile = QLabel('Lineage File')
        modelFile = QLabel('Model File')
        # 栅格布局第二列是参数输入框
        self.projectFolderEdit = QLineEdit()
        self.maxTimeEdit = QLineEdit()
        self.batchSizeEdit = QLineEdit()
        self.modelFileEdit = QLineEdit()
        # 栅格布局第三列是参数选择按钮
        projectFolderBtn = QPushButton("Select")
        projectFolderBtn.clicked.connect(self.chooseProjectFolder)
        self.embryoNamesBtn = QComboBox()
        self.lineageFileBtn = QComboBox()
        modelFileBtn = QPushButton("Select")
        modelFileBtn.clicked.connect(self.chooseModelFile)

        grid = QGridLayout()
        grid.setSpacing(30)

        grid.addWidget(projectFolder, 1, 0)
        grid.addWidget(self.projectFolderEdit, 1, 1)
        grid.addWidget(projectFolderBtn, 1, 2)

        grid.addWidget(embryoNames, 2, 0)
        grid.addWidget(self.embryoNamesBtn, 2, 1)

        grid.addWidget(modelFile, 3, 0)
        grid.addWidget(self.modelFileEdit, 3, 1)
        grid.addWidget(modelFileBtn, 3, 2)






        self.mainlayout.addLayout(grid)

    def chooseProjectFolder(self):
        pass

    def chooseModelFile(self):
        pass

    def runSegmentation(self):
        pass

    def stopSegmentation(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Nucleus_Segmentation()
    sys.exit(app.exec_())