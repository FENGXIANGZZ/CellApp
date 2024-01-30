import sys
import os
import traceback
import glob
from multiprocessing import Pool
from tkinter import Image

import numpy as np
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread


class Preprocess(QWidget):

    def __init__(self):
        super().__init__()

        self.mainlayout = QVBoxLayout()  # 组件的整体布局是垂直布局,第一层是一个栅格放参数,第二层是个水平布局放进度条, 最下层是一个反馈信息栏

        self.initUI()  # 设置参数相关的各种组件位置

        self.middlelayout = QHBoxLayout()
        self.runpreprocessBtn = QPushButton("Run Preprocess")
        self.runpreprocessBtn.clicked.connect(self.runPreprocess)
        self.stoppreprocessBtn = QPushButton("Stop Preprocess")
        self.stoppreprocessBtn.clicked.connect(self.stopPreprocess)
        self.preprocessBar = QProgressBar()
        self.middlelayout.addWidget(self.runpreprocessBtn)
        self.middlelayout.addWidget(self.stoppreprocessBtn)
        self.middlelayout.addWidget(self.preprocessBar)
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
        self.xyResoluEdit = QLineEdit()
        self.zResoluEdit = QLineEdit()
        self.reduceRationEdit = QLineEdit()
        self.sliceNumEdit = QLineEdit()
        self.maxTimeEdit = QLineEdit()
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
        grid.addWidget(self.xyResoluEdit, 6, 1)

        grid.addWidget(zResolu, 7, 0)
        grid.addWidget(self.zResoluEdit, 7, 1)

        grid.addWidget(reduceRation, 8, 0)
        grid.addWidget(self.reduceRationEdit, 8, 1)

        grid.addWidget(sliceNum, 9, 0)
        grid.addWidget(self.sliceNumEdit, 9, 1)

        grid.addWidget(maxTime, 10, 0)
        grid.addWidget(self.maxTimeEdit, 10, 1)

        self.mainlayout.addLayout(grid)  # 将栅格布局添加到整体垂直布局的第一层

    def chooseRawFolder(self):
        """
        弹出一个路径选择,将选择的路径名称放到rawFolder,里面的内容放入embryonames
        :return:
        """
        dirName = QFileDialog.getExistingDirectory(self, 'Choose Raw Folder', './')
        try:
            self.textEdit.clear()
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
            self.textEdit.clear()
            self.projectFolderEdit.setText(dirName)
        except Exception as e:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def chooseLineageFile(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose Lineage File',
                                                         self.rawFolderEdit.text(), "CSV Files(*.csv)")
        try:
            self.textEdit.clear()
            self.lineageFileEdit.setText(fileName)
        except Exception as e:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def chooseNumberDict(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, 'Choose Lineage File',
                                                         './', "CSV Files(*.csv)")
        try:
            self.textEdit.clear()
            self.numberDictEdit.setText(fileName)
        except Exception as e:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def runPreprocess(self):

        config = {}
        try:
            self.textEdit.clear()
            config['num_slice'] = int(self.sliceNumEdit.text())
            config["embryo_names"] = self.embryoNamesBtn.currentText()
            config["max_time"] = int(self.maxTimeEdit.text())
            config["xy_resolution"] = float(self.xyResoluEdit.text())
            config["z_resolution"] = float(self.zResoluEdit.text())
            config["reduce_ratio"] = float(self.reduceRationEdit.text())
            config["raw_folder"] = self.rawFolderEdit.text()
            config["project_folder"] = self.projectFolderEdit.text()
            config["number_dictionary"] = self.numberDictEdit.text()
            if self.lineageFileEdit.text() == '':
                config["lineage_file"] = None
            else:
                config["lineage_file"] = self.lineageFileEdit.text()

        except Exception:
            config.clear()
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Error!', 'Please check your paras!')

        if config:
            self.textEdit.append('Running Preprocess!')
            for key, value in config.items():
                self.textEdit.append(f"The {key} is: {value}")

            self.runpreprocessBtn.setEnabled(False)

            self.pthread = PreprocessThread(config)
            # self.pthread.signal.connect(self.ThreadCallback)
            # self.pthread.process.connect(self.ProcessCallback)
            self.pthread.start()

    def stopPreprocess(self):
        try:
            self.runpreprocessBtn.setEnabled(True)
            self.textEdit.clear()
            self.pthread.quit()
            QMessageBox.information(self, 'Tips', 'Preprocess has been terminated.')
        except Exception:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Preprocess has not been started.')

"""QT 中 QObject 作QT中类的最终父类，具有自定义信号与槽的能力，只要继承自这个类的类，也一样拥有自定义信号和槽的能力。
QT 中定义信号与槽是十分有用的，QT 下多线程类QThread 是继承自 QObject，同样具有有自定义信号和槽的能力"""
class PreprocessThread(QThread):
    signal = pyqtSignal(bool, str, str)
    process = pyqtSignal(str, int, int)

    def __init__(self, config={}):
        super().__init__()
        self.config = config
        self.mpPool = None


    def run(self):
        try:
            sin = self.combine_slices(self.config)
            if sin == 1:
                self.mpPool.close()
                self.signal.emit(True, 'Preprocess', 'Preprocess Completed!')
        except Exception:
            if self.mpPool:
                self.mpPool.close()
            self.signal.emit(False, 'Preprocess', traceback.format_exc())


    def combine_slices(self, process, config):
        """
        Combine slices into stack images
        :param config: parameters
        :return:
        """
        max_time = config["max_time"]
        raw_folder = config["raw_folder"]
        stack_folder = os.path.join(config["project_folder"], "RawStack")
        lineage_file = config.get("lineage_file", None)
        number_dictionary = config["number_dictionary"]

        # get output size
        raw_memb_files = glob.glob(os.path.join(raw_folder, config["embryo_names"][0], "tifR", "*.tif"))
        raw_size = list(np.asarray(Image.open(raw_memb_files[0])).shape) + [int(config["num_slice"] * config["z_resolution"] / config["xy_resolution"])]
        out_size = [int(i * config["reduce_ratio"]) for i in raw_size]
        out_res = [res * x / y for res, x, y in zip([config["xy_resolution"], config["xy_resolution"], config["xy_resolution"]], raw_size, out_size)]

        # multiprocessing
        # self.mpPool = Pool(cpu_count() - 1)
        # for embryo_name in embryo_names:
        #     # save nucleus
        #     origin_files = glob.glob(os.path.join(raw_folder, embryo_name, "tif", "*.tif"))
        #     origin_files = sorted(origin_files)
        #     target_folder = os.path.join(stack_folder, embryo_name, "RawNuc")
        #     if not os.path.isdir(target_folder):
        #         os.makedirs(target_folder)
        #
        #     configs = []
        #     for tp in range(1, max_time + 1):
        #         configs.append((origin_files, target_folder, embryo_name, tp, out_size, num_slice, out_res))
        #
        #     self.flag = True
        #     for idx, _ in enumerate(self.mpPool.imap_unordered(stack_nuc_slices, configs)):
        #         process.emit('1/3 Stack nucleus', idx, max_time)
        #         if not self.flag:
        #             self.mpPool.close()
        #             return 0
        #
        #     # save membrane
        #     origin_files = glob.glob(os.path.join(raw_folder, embryo_name, "tifR", "*.tif"))
        #     origin_files = sorted(origin_files)
        #     target_folder = os.path.join(stack_folder, embryo_name, "RawMemb")
        #     if not os.path.isdir(target_folder):
        #         os.makedirs(target_folder)
        #
        #     configs = []
        #     for tp in range(1, max_time + 1):
        #         configs.append((origin_files, target_folder, embryo_name, tp, out_size, num_slice, out_res))
        #     self.flag = True
        #     for idx, _ in enumerate(tqdm(self.mpPool.imap_unordered(stack_memb_slices, configs), total=len(configs),
        #                                  desc="2/3 Stack membrane of {}".format(embryo_name))):
        #         process.emit('2/3 Stacking membrane', idx, max_time)
        #         if not self.flag:
        #             self.mpPool.close()
        #             return 0
        #
        #     # save nucleus
        #     if lineage_file is not None:
        #         target_folder = os.path.join(stack_folder, embryo_name, "SegNuc")
        #         if not os.path.isdir(target_folder):
        #             os.makedirs(target_folder)
        #         pd_lineage = pd.read_csv(lineage_file, dtype={"cell": str,
        #                                                       "time": np.int16,
        #                                                       "z": np.float32,
        #                                                       "x": np.float32,
        #                                                       "y": np.float32})
        #
        #         pd_number = pd.read_csv(number_dictionary, names=["name", "label"])
        #         number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
        #
        #         configs = []
        #         for tp in range(1, max_time + 1):
        #             configs.append((embryo_name, number_dict, pd_lineage, tp, raw_size, out_size, out_res,
        #                             xy_res / z_res, target_folder))
        #         self.flag = True
        #         for idx, _ in enumerate(tqdm(self.mpPool.imap_unordered(save_nuc_seg, configs), total=len(configs),
        #                                      desc="3/3 Construct nucleus location of {}".format(embryo_name))):
        #             process.emit('3/3 Constructing nucleus location', idx, max_time)
        #             if not self.flag:
        #                 self.mpPool.close()
        #                 return 0
        #         shutil.copy(lineage_file, os.path.join(stack_folder, embryo_name))
        # return 1



if __name__ == '__main__':
    """单独看这个组件"""
    app = QApplication(sys.argv)
    ex = Preprocess()
    sys.exit(app.exec_())
