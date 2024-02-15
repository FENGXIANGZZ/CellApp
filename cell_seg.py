import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QMutex, QWaitCondition
import traceback
import os
import glob
import nibabel as nib
from Utils.segment_lib import segmentation
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


class Cell_Segmentation(QWidget):

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
        self.pausesegmentBtn = QPushButton("Pause Segmentation")
        self.pausesegmentBtn.setEnabled(False)
        self.pausesegmentBtn.clicked.connect(self.pauseSegmentation)
        self.resumesegmentBtn = QPushButton("Resume Segmentation")
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

        projectFolder = QLabel('Project Folder')
        embryoName = QLabel('Embryo Name')
        modelName = QLabel('Model Name')
        binaryMemb = QLabel('Segmented Membrane')
        binaryNuc = QLabel('Segmented Nucleus')
        kernelSize = QLabel('Kernel Size')
        kernelStructure = QLabel('Kernel Structure')
        Nuc = QLabel("Nucleus Position")

        self.projectFolderEdit = QLineEdit()
        self.embryoNameEdit = QComboBox()
        self.modelNameEdit = QComboBox()
        binaryMembEdit = QComboBox()
        binaryNucEdit = QComboBox()
        self.kernelStructureEdit = QComboBox()
        self.kernelStructureEdit.addItems(["cube", "ball"])
        self.kernelSizeEdit = QComboBox()
        self.kernelSizeEdit.addItems(["3", "5", "7"])
        self.Nuc = QCheckBox('Whether to use segmented Nucleus position to segment whole cell')
        self.Nuc.stateChanged.connect(self.Nucchange)
        self.Nucinput = False

        projectFolderBtn = QPushButton("Select")
        projectFolderBtn.clicked.connect(self.chooseProjectFolder)

        grid = QGridLayout()
        grid.setSpacing(30)

        grid.addWidget(projectFolder, 1, 0)
        grid.addWidget(self.projectFolderEdit, 1, 1)
        grid.addWidget(projectFolderBtn, 1, 2)

        grid.addWidget(embryoName, 2, 0)
        grid.addWidget(self.embryoNameEdit, 2, 1)

        grid.addWidget(modelName, 3, 0)
        grid.addWidget(self.modelNameEdit, 3, 1)

        grid.addWidget(binaryMemb, 4, 0)
        grid.addWidget(binaryMembEdit, 4, 1)

        grid.addWidget(binaryNuc, 5, 0)
        grid.addWidget(binaryNucEdit, 5, 1)

        grid.addWidget(kernelStructure, 6, 0)
        grid.addWidget(self.kernelStructureEdit, 6, 1)

        grid.addWidget(kernelSize, 7, 0)
        grid.addWidget(self.kernelSizeEdit, 7, 1)

        grid.addWidget(Nuc, 8, 0)
        grid.addWidget(self.Nuc, 8, 1)

        self.mainlayout.addLayout(grid)

    def chooseProjectFolder(self):
        dirName = QFileDialog.getExistingDirectory(self, 'Choose RawStack Folder', './')
        try:
            self.textEdit.clear()
            self.embryoNameEdit.clear()
            self.projectFolderEdit.setText(dirName)
            if dirName:
                listdir = [x for x in os.listdir(os.path.join(dirName, "SegStack")) if not x.startswith(".")]
                listdir.sort()
                self.embryoNameEdit.addItems(listdir)
        except Exception as e:
            self.textEdit.setText(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def Autofillblank(self, embryo_name):
        try:
            raw_memb_files = glob.glob(os.path.join(self.rawFolderEdit.text(), embryo_name, "tifR", "*.tif"))
            raw_memb_img = raw_memb_files[-1]
            max_time = re.findall(r"\d{2,3}", raw_memb_img)[-2]
            num_slice = re.findall(r"\d{2,3}", raw_memb_img)[-1]

            self.maxTimeEdit.setText(max_time)
            self.sliceNumEdit.setText(num_slice)
            self.xLengthEdit.setText("256")
            self.yLengthEdit.setText("356")
            self.zLengthEdit.setText("160")
            self.reduceRationEdit.setText("1.0")
        except:
            self.textEdit.setText(traceback.format_exc())
            QMessageBox.warning(self, 'Error!', 'Please check your paras!')


    def runSegmentation(self):
        pass

    def pauseSegmentation(self):
        pass

    def cancelSegmentation(self):
        pass

    def resumeSegmentation(self):
        pass

    def completeSegmentation(self, value):
        pass

    def Nucchange(self, state):
        if state == Qt.Checked:
            self.Nuc.setText("Use segmented Nucleus infomation")
            self.Nucinput = True
        else:
            self.Nuc.setText("Use h_maxima to calculate nucleus position")
            self.Nucinput = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cell_Segmentation()
    sys.exit(app.exec_())
