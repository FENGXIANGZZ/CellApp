import sys
import os
import traceback
import glob
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count
from tkinter import Image

import numpy as np
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from Utils.preprocess_lib import stack_nuc_slices

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
        embryoName = QLabel('Embryo Name')
        xyResolu = QLabel('X-Y Resolution')
        zResolu = QLabel('Z Resolution')
        reduceRation = QLabel('Reduce Ratio')
        sliceNum = QLabel('Slice Num')
        maxTime = QLabel('Max Time')
        projectFolder = QLabel('Project Folder')
        preprocessObject = QLabel('Preprocess Object')
        # 栅格布局第二列是参数输入框
        self.rawFolderEdit = QLineEdit()
        self.xyResoluEdit = QLineEdit()
        self.zResoluEdit = QLineEdit()
        self.reduceRationEdit = QLineEdit()
        self.sliceNumEdit = QLineEdit()
        self.maxTimeEdit = QLineEdit()
        self.projectFolderEdit = QLineEdit()
        # 栅格布局第三列是参数选择按钮
        rawFolderBtn = QPushButton("Select")
        rawFolderBtn.clicked.connect(self.chooseRawFolder)  # 将这个按钮点击事件与函数chooseRawFolder绑定
        self.embryoNameBtn = QComboBox()
        projectFolderBtn = QPushButton("Select")
        projectFolderBtn.clicked.connect(self.chooseProjectFolder)
        self.preprocessObjectBtn = QComboBox()
        self.preprocessObjectBtn.setObjectName("preprocessObject")  # 这里给这个复选框设置名字是为了在主窗口不清除这里的数据
        self.preprocessObjectBtn.addItem("Nucleus")
        self.preprocessObjectBtn.addItem("Membrane")
        self.preprocessObjectBtn.addItem("Both")

        grid = QGridLayout()
        grid.setSpacing(15)

        grid.addWidget(rawFolder, 1, 0)
        grid.addWidget(self.rawFolderEdit, 1, 1)
        grid.addWidget(rawFolderBtn, 1, 2)

        grid.addWidget(embryoName, 2, 0)
        grid.addWidget(self.embryoNameBtn, 2, 1)

        grid.addWidget(projectFolder, 3, 0)
        grid.addWidget(self.projectFolderEdit, 3, 1)
        grid.addWidget(projectFolderBtn, 3, 2)

        grid.addWidget(preprocessObject, 4, 0)
        grid.addWidget(self.preprocessObjectBtn, 4, 1)

        grid.addWidget(xyResolu, 5, 0)
        grid.addWidget(self.xyResoluEdit, 5, 1)

        grid.addWidget(zResolu, 6, 0)
        grid.addWidget(self.zResoluEdit, 6, 1)

        grid.addWidget(reduceRation, 7, 0)
        grid.addWidget(self.reduceRationEdit, 7, 1)

        grid.addWidget(sliceNum, 8, 0)
        grid.addWidget(self.sliceNumEdit, 8, 1)

        grid.addWidget(maxTime, 9, 0)
        grid.addWidget(self.maxTimeEdit, 9, 1)

        self.mainlayout.addLayout(grid)  # 将栅格布局添加到整体垂直布局的第一层

    def chooseRawFolder(self):
        """
        弹出一个路径选择,将选择的路径名称放到rawFolder,里面的内容放入embryonames
        :return:
        """
        dirName = QFileDialog.getExistingDirectory(self, 'Choose Raw Folder', './')
        try:
            self.textEdit.clear()
            self.embryoNameBtn.clear()
            self.rawFolderEdit.setText(dirName)
            if dirName:
                listdir = [x for x in os.listdir(dirName) if not x.startswith(".")]
                listdir.sort()
                self.embryoNameBtn.addItems(listdir)

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

    def runPreprocess(self):

        config = {}
        try:
            self.textEdit.clear()
            config['num_slice'] = int(self.sliceNumEdit.text())
            config["embryo_name"] = self.embryoNameBtn.currentText()
            config["max_time"] = int(self.maxTimeEdit.text())
            config["xy_resolution"] = float(self.xyResoluEdit.text())
            config["z_resolution"] = float(self.zResoluEdit.text())
            config["reduce_ratio"] = float(self.reduceRationEdit.text())
            config["raw_folder"] = self.rawFolderEdit.text()
            config["project_folder"] = self.projectFolderEdit.text()
            config["preprocess_object"] = self.preprocessObjectBtn.currentText()

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

            self.pthread.start()

            self.pthread.finished.connect(self.completePreprocess)

    def stopPreprocess(self):
        try:
            self.runpreprocessBtn.setEnabled(True)
            self.textEdit.clear()
            self.pthread.quit()
            QMessageBox.information(self, 'Tips', 'Preprocess has been terminated.')
        except Exception:
            self.textEdit.append(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Preprocess has not been started.')

    def completePreprocess(self):
        self.textEdit.setText("Preprocess Complete!")
        self.runpreprocessBtn.setEnabled(True)
        self.preprocessBar.setValue(100)


"""QT 中 QObject 作QT中类的最终父类，具有自定义信号与槽的能力，只要继承自这个类的类，也一样拥有自定义信号和槽的能力。
QT 中定义信号与槽是十分有用的，QT 下多线程类QThread 是继承自 QObject，同样具有有自定义信号和槽的能力"""


class PreprocessThread(QThread):

    def __init__(self, config={}):
        super().__init__()
        # load parameters
        self.num_slice = config["num_slice"]
        self.embryo_name = config["embryo_name"]
        self.max_time = config["max_time"]
        self.xy_res = config["xy_resolution"]
        self.z_res = config["z_resolution"]
        self.reduce_ratio = config["reduce_ratio"]
        self.raw_folder = config["raw_folder"]
        self.stack_folder = os.path.join(config["project_folder"], "RawStack")
        self.preprocess_object = config['preprocess_object']

        # get output size
        raw_memb_files = glob.glob(os.path.join(self.raw_folder, self.embryo_name, "tifR", "*.tif"))
        self.raw_size = list(np.asarray(Image.open(raw_memb_files[0])).shape) + [
            int(self.num_slice * self.z_res / self.xy_res)]
        self.out_size = [int(i * self.reduce_ratio) for i in self.raw_size]
        self.out_res = [res * x / y for res, x, y in
                        zip([self.xy_res, self.xy_res, self.xy_res], self.raw_size, self.out_size)]

    def run(self):
        try:
            if self.preprocess_object == "Nucleus":
                self.combine_nucleus_slices()
            elif self.preprocess_object == "Membrane":
                pass
            else:
                pass

        except Exception:
            self.quit()

    def combine_nucleus_slices(self):
        """
        Combine slices into stack images
        :param config: parameters
        :return:
        """
        # save nucleus
        origin_files = glob.glob(os.path.join(self.raw_folder, self.embryo_name, "tif", "*.tif"))
        origin_files.sort()
        target_folder = os.path.join(self.stack_folder, self.embryo_name, "RawNuc")
        if not os.path.isdir(target_folder):
            os.makedirs(target_folder)

        configs = []
        for tp in range(1, self.max_time + 1):
            configs.append((origin_files, target_folder, self.embryo_name, tp, self.out_size, self.num_slice, self.out_res))

        with ThreadPoolExecutor(cpu_count() + 1) as t:
            for idx, config in enumerate(configs):
                t.submit(stack_nuc_slices, config)


    # multiprocessing
    # self.mpPool = Pool(cpu_count() + 1)
    # for embryo_name in embryo_names:
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
