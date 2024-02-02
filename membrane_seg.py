import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import traceback
import os


class Memb_Segmentation(QWidget):

    def __init__(self):
        super().__init__()

        self.mainlayout = QVBoxLayout()  # 组件的整体布局是垂直布局,第一层是一个栅格放参数,第二层是个水平布局放进度条, 最下层是一个反馈信息栏

        self.initUI()  # 设置参数相关的各种组件位置

        self.middlelayout = QGridLayout()

        self.runsegmentBtn = QPushButton("Run Segmentation")
        self.runsegmentBtn.clicked.connect(self.runSegmentation)
        self.cancelsegmentBtn = QPushButton("Cancel Segmentation")
        self.cancelsegmentBtn.setEnabled(False)
        self.cancelsegmentBtn.clicked.connect(self.cancelSegmentation)
        self.pausesegmentBtn = QPushButton("Pause Preprocess")
        self.pausesegmentBtn.setEnabled(False)
        self.pausesegmentBtn.clicked.connect(self.pauseSegmentation)
        self.resumesegmentBtn = QPushButton("Resume Segment")
        self.resumesegmentBtn.setEnabled(False)
        self.resumesegmentBtn.clicked.connect(self.resumeSegmentation)
        self.segmentBar = QProgressBar()
        self.segmentBar.valueChanged.connect(self.completeSegmentation)

        self.middlelayout.addWidget(self.runsegmentBtn, 0, 1)
        self.middlelayout.addWidget(self.cancelsegmentBtn, 0, 2)
        self.middlelayout.addWidget(self.pausesegmentBtn, 2, 1)
        self.middlelayout.addWidget(self.resumesegmentBtn, 2, 2)
        self.middlelayout.addWidget(self.segmentBar, 1, 3)
        self.mainlayout.addStretch(1)
        self.mainlayout.addLayout(self.middlelayout)

        self.textEdit = QTextEdit()  # 初始化反馈信息栏
        self.textEdit.setFocusPolicy(Qt.NoFocus)  # 将反馈信息栏设置为无法主动编辑
        self.mainlayout.addStretch(1)  # 将反馈信息栏压到垂直布局的底层
        self.mainlayout.addWidget(self.textEdit)  # 将反馈信息栏添加到整体布局中

        self.setLayout(self.mainlayout)
        self.setGeometry(300, 300, 450, 500)
        self.show()

    def initUI(self):
        # 栅格布局第一列是参数名称
        projectFolder = QLabel('Project Folder')
        embryoName = QLabel('Embryo Name')
        modelName = QLabel('Model Name')
        modelFile = QLabel('Model File')
        GPU = QLabel("GPU")
        # 栅格布局第二列是参数输入框
        self.projectFolderEdit = QLineEdit()
        self.modelNameEdit = QLineEdit()
        self.modelFileEdit = QLineEdit()
        self.GPU = QCheckBox('Whether to use GPU')
        self.GPU.stateChanged.connect(self.GPUchange)
        self.GPUcheck = None
        # 栅格布局第三列是参数选择按钮
        projectFolderBtn = QPushButton("Select")
        projectFolderBtn.clicked.connect(self.chooseProjectFolder)
        self.embryoNameBtn = QComboBox()
        modelFileBtn = QPushButton("Select")
        modelFileBtn.clicked.connect(self.chooseModelFile)

        grid = QGridLayout()
        grid.setSpacing(30)

        grid.addWidget(projectFolder, 1, 0)
        grid.addWidget(self.projectFolderEdit, 1, 1)
        grid.addWidget(projectFolderBtn, 1, 2)

        grid.addWidget(embryoName, 2, 0)
        grid.addWidget(self.embryoNameBtn, 2, 1)

        grid.addWidget(modelFile, 3, 0)
        grid.addWidget(self.modelFileEdit, 3, 1)
        grid.addWidget(modelFileBtn, 3, 2)

        grid.addWidget(modelName, 4, 0)
        grid.addWidget(self.modelNameEdit, 4, 1)

        grid.addWidget(GPU, 5, 0)
        grid.addWidget(self.GPU, 5, 1)

        self.mainlayout.addLayout(grid)

    def chooseProjectFolder(self):
        dirName = QFileDialog.getExistingDirectory(self, 'Choose RawStack Folder', './')
        try:
            self.textEdit.clear()
            self.embryoNameBtn.clear()
            self.projectFolderEdit.setText(dirName)
            if dirName:
                listdir = [x for x in os.listdir(dirName) if not x.startswith(".")]
                listdir.sort()
                self.embryoNameBtn.addItems(listdir)
        except Exception as e:
            self.textEdit.setText(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def chooseModelFile(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose Model File',
                                                         self.projectFolderEdit.text(), "(*.pth)")
        try:
            self.textEdit.setText('')
            self.modelFileEdit.setText(fileName)
        except Exception as e:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right File!')

    def runSegmentation(self):
        pass

    def cancelSegmentation(self):
        pass

    def pauseSegmentation(self):
        pass

    def resumeSegmentation(self):
        pass

    def completeSegmentation(self):
        pass

    def GPUchange(self, state):
        if state == Qt.Checked:
            self.GPU.setText("Use GPU")
            self.GPUcheck = True
        else:
            self.GPU.setText("Don't use GPU")
            self.GPUcheck = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Memb_Segmentation()
    sys.exit(app.exec_())
