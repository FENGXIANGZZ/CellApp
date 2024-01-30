import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread


class Analysis(QWidget):

    def __init__(self):
        super().__init__()

        self.mainlayout = QVBoxLayout()  # 组件的整体布局是垂直布局,第一层是一个栅格放参数,第二层是个水平布局放进度条, 最下层是一个反馈信息栏

        self.initUI()  # 设置参数相关的各种组件位置

        self.middlelayout = QHBoxLayout()
        self.runanalysisBtn = QPushButton("Run Segmentation")
        self.runanalysisBtn.clicked.connect(self.runAnalysis)
        self.stopanalysisBtn = QPushButton("Stop Segmentation")
        self.stopanalysisBtn.clicked.connect(self.stopAnalysis)
        self.analysisBar = QProgressBar()
        self.middlelayout.addWidget(self.runanalysisBtn)
        self.middlelayout.addWidget(self.stopanalysisBtn)
        self.middlelayout.addWidget(self.analysisBar)
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
        rawFolder = QLabel('Raw Folder')
        embryoNames = QLabel('Embryo Names')
        numberDict = QLabel('Number Dictionary')
        lineageFile = QLabel('Lineage File')
        xyResolu = QLabel('X-Y Resolution')
        sliceNum = QLabel('Slice Num')
        # 栅格布局第二列是参数输入框
        self.projectFolderEdit = QLineEdit()
        self.rawFolderEdit = QLineEdit()
        self.numberDictEdit = QLineEdit()
        self.lineageFileEdit = QLineEdit()
        self.sliceNumEdit = QLineEdit()
        self.xyResoluEdit = QLineEdit()
        # 栅格布局第三列是参数选择按钮
        projectFolderBtn = QPushButton("Select")
        projectFolderBtn.clicked.connect(self.chooseProjectFolder)
        rawFolderBtn = QPushButton("Select")
        rawFolderBtn.clicked.connect(self.chooseRawFolder)
        self.embryoNamesBtn = QComboBox()
        lineageFileBtn = QPushButton("Select")
        lineageFileBtn.clicked.connect(self.chooseLineageFile)
        numberDictBtn = QPushButton("Select")
        numberDictBtn.clicked.connect(self.chooseNumberDict)

        grid = QGridLayout()
        grid.setSpacing(30)

        grid.addWidget(projectFolder, 1, 0)
        grid.addWidget(self.projectFolderEdit, 1, 1)
        grid.addWidget(projectFolderBtn, 1, 2)

        grid.addWidget(rawFolder, 2, 0)
        grid.addWidget(self.rawFolderEdit, 2, 1)
        grid.addWidget(rawFolderBtn, 2, 2)

        grid.addWidget(embryoNames, 3, 0)
        grid.addWidget(self.embryoNamesBtn, 3, 1)

        grid.addWidget(lineageFile, 4, 0)
        grid.addWidget(self.lineageFileEdit, 4, 1)
        grid.addWidget(lineageFileBtn, 4, 2)

        grid.addWidget(numberDict, 5, 0)
        grid.addWidget(self.numberDictEdit, 5, 1)
        grid.addWidget(numberDictBtn, 5, 2)

        grid.addWidget(sliceNum, 6, 0)
        grid.addWidget(self.sliceNumEdit, 6, 1)

        grid.addWidget(xyResolu, 7, 0)
        grid.addWidget(self.xyResoluEdit, 7, 1)

        self.mainlayout.addLayout(grid)

    def chooseProjectFolder(self):
        pass

    def chooseRawFolder(self):
        pass

    def runAnalysis(self):
        pass

    def stopAnalysis(self):
        pass

    def chooseLineageFile(self):
        pass

    def chooseNumberDict(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Analysis()
    sys.exit(app.exec_())
