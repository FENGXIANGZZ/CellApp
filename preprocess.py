import sys
import os
import traceback
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout)
from PyQt5.QtCore import Qt


class Preprocess(QWidget):

    def __init__(self):
        super().__init__()

        self.mainlayout = QVBoxLayout()  # 组件的整体布局是垂直布局,上层是一个栅格放参数,下层是一个反馈信息栏

        self.initUI()  # 设置参数相关的各种组件位置

        self.textEdit = QTextEdit()  # 初始化反馈信息栏
        self.textEdit.setFocusPolicy(Qt.NoFocus)  # 将反馈信息栏设置为无法主动编辑
        self.mainlayout.addStretch(1)  # 将反馈信息栏压到垂直布局的底层
        self.mainlayout.addWidget(self.textEdit)  # 将反馈信息栏添加到整体布局中

        self.setLayout(self.mainlayout)  # 将Preprocess这个分组件应用上设置好的整体布局
        self.setGeometry(300, 300, 450, 500)
        self.show()

    def initUI(self):
        # 栅格布局第一列是参数名称
        rawFolder = QLabel('Raw Folder')
        embryoNames = QLabel('Embryo Name')
        xyResolu = QLabel('X-Y Resolution')
        zResolu = QLabel('Z Resolution')
        reduceRation = QLabel('Reduce Ratio')
        sliceNum = QLabel('Slice Num')
        maxTime = QLabel('Max Time')
        projectFolder = QLabel('Project Folder')
        lineageFile = QLabel('Lineage File')
        numberDict = QLabel('Number Dictionary')
        # 栅格布局第二列是参数输入框
        self.rawFolderEdit = QLineEdit()
        xyResoluEdit = QLineEdit()
        zResoluEdit = QLineEdit()
        reduceRationEdit = QLineEdit()
        sliceNumEdit = QLineEdit()
        maxTimeEdit = QLineEdit()
        self.projectFolderEdit = QLineEdit()
        self.lineageFileEdit = QLineEdit()
        self.numberDictEdit = QLineEdit()
        # 栅格布局第三列是参数选择按钮
        rawFolderBtn = QPushButton("Select")
        rawFolderBtn.clicked.connect(self.chooseRawFolder)  # 将这个按钮点击事件与函数chooseRawFolder绑定
        self.embryoNamesBtn = QComboBox()
        projectFolderBtn = QPushButton("Select")
        projectFolderBtn.clicked.connect(self.chooseProjectFolder)
        lineageFileBtn = QPushButton("Select")
        lineageFileBtn.clicked.connect(self.chooseLineageFile)
        numberDictBtn = QPushButton("Select")
        numberDictBtn.clicked.connect(self.chooseNumberDict)

        grid = QGridLayout()
        grid.setSpacing(15)

        grid.addWidget(rawFolder, 1, 0)
        grid.addWidget(self.rawFolderEdit, 1, 1)
        grid.addWidget(rawFolderBtn, 1, 2)

        grid.addWidget(embryoNames, 2, 0)
        grid.addWidget(self.embryoNamesBtn, 2, 1)

        grid.addWidget(projectFolder, 3, 0)
        grid.addWidget(self.projectFolderEdit, 3, 1)
        grid.addWidget(projectFolderBtn, 3, 2)

        grid.addWidget(lineageFile, 4, 0)
        grid.addWidget(self.lineageFileEdit, 4, 1)
        grid.addWidget(lineageFileBtn, 4, 2)

        grid.addWidget(numberDict, 5, 0)
        grid.addWidget(self.numberDictEdit, 5, 1)
        grid.addWidget(numberDictBtn, 5, 2)

        grid.addWidget(xyResolu, 6, 0)
        grid.addWidget(xyResoluEdit, 6, 1)

        grid.addWidget(zResolu, 7, 0)
        grid.addWidget(zResoluEdit, 7, 1)

        grid.addWidget(reduceRation, 8, 0)
        grid.addWidget(reduceRationEdit, 8, 1)

        grid.addWidget(sliceNum, 9, 0)
        grid.addWidget(sliceNumEdit, 9, 1)

        grid.addWidget(maxTime, 10, 0)
        grid.addWidget(maxTimeEdit, 10, 1)


        self.mainlayout.addLayout(grid)  # 将栅格布局添加到整体垂直布局的上层

    def chooseRawFolder(self):
        """
        弹出一个路径选择,将选择的路径名称放到rawFolder,里面的内容放入embryonames
        :return:
        """
        dirName = QFileDialog.getExistingDirectory(self, 'Choose Raw Folder', './')
        try:
            self.textEdit.setText('')
            self.embryoNamesBtn.clear()
            self.rawFolderEdit.setText(dirName)
            listdir = [x for x in os.listdir(dirName) if not x.startswith(".")]
            listdir.sort()
            self.embryoNamesBtn.addItems(listdir)

        except Exception as e:
            self.textEdit.setText(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def chooseProjectFolder(self):
        dirName = QFileDialog.getExistingDirectory(self, 'Choose Stack Folder', './')
        try:
            self.textEdit.setText('')
            self.projectFolderEdit.setText(dirName)
        except Exception as e:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def chooseLineageFile(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose Lineage File',
                                                         self.rawFolderEdit.text(), "CSV Files(*.csv)")
        try:
            self.textEdit.setText('')
            self.lineageFileEdit.setText(fileName)
        except Exception as e:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def chooseNumberDict(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose Lineage File',
                                                         './', "CSV Files(*.csv)")
        try:
            self.textEdit.setText('')
            self.numberDictEdit.setText(fileName)
        except Exception as e:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def runPreprocess(self):
        pass
        # config = {}
        # try:
        #     self.textEdit.setText('')
        #     config['num_slice'] = int(self.LE_sliceNum.text())
        #     en = []
        #     en.append(self.CB_embryoNames.currentText())
        #     config["embryo_names"] = en
        #     config["max_time"] = int(self.LE_maxTime.text())
        #     config["xy_resolution"] = float(self.LE_xyResolution.text())
        #     config["z_resolution"] = float(self.LE_zResolution.text())
        #     config["reduce_ratio"] = float(self.LE_reduceRatio.text())
        #     config["raw_folder"] = self.LE_rawFolder.text()
        #     config["project_folder"] = self.LE_projectFolder.text()
        #     config["lineage_file"] = self.LE_lineage.text()
        #     if config["lineage_file"] == '':
        #         config["lineage_file"] = None
        #     config["number_dictionary"] = self.LE_numberDict.text()
        # except Exception:
        #     self.textEdit.append(traceback.format_exc())
        #     QMessageBox.warning(self, 'Error!', 'Please check your paras!')
        # self.textEdit.append('Running Preprocess!')
        # self.Btn_runPreprocess.setEnabled(False)
        # self.LE_maxTime_Seg.setText(self.LE_maxTime.text())
        # self.LE_sliceNum_Ana.setText(self.LE_sliceNum.text())
        # self.PreprocessCall = False
        # self.pthread = PreprocessThread(config)
        # self.threadbreak.connect(self.pthread.threadflag)
        # self.pthread.signal.connect(self.ThreadCallback)
        # self.pthread.process.connect(self.ProcessCallback)
        # self.pthread.start()

    def stopPreprocess(self):
        pass
        # try:
        #     self.Btn_runPreprocess.setEnabled(True)
        #     self.textEdit.setText('')
        #     self.threadbreak.emit(False)
        #     QMessageBox.information(self, 'Tips', 'Preprocess has been terminated.')
        # except Exception:
        #     self.textEdit.append(traceback.format_exc())
        #     QMessageBox.warning(self, 'Warning!', 'Preprocess has not been started.')


if __name__ == '__main__':
    """单独看这个组件"""
    app = QApplication(sys.argv)
    ex = Preprocess()
    sys.exit(app.exec_())
