import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QMessageBox,
                             QComboBox, QVBoxLayout, QProgressBar, QHBoxLayout, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import traceback
import os
from Utils.parser import read_yaml_to_dict, parse_tuple
from Utils import dataset
from torch.utils.data import DataLoader
import networks
import torch
import random
import numpy as np
import ast
from skimage.transform import resize
import nibabel as nib


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
        GPU = QLabel("GPU")
        Nuc = QLabel("Nucleus")
        # 栅格布局第二列是参数输入框
        self.projectFolderEdit = QLineEdit()
        self.modelNameEdit = QComboBox()
        self.modelNameEdit.addItems(["TUNETr", "UNETR", "SwinUNETR", "VNet", "UNet", "DMFNet"])
        self.GPU = QCheckBox('Whether to use GPU')
        self.GPU.stateChanged.connect(self.GPUchange)
        self.GPUcheck = False
        self.Nuc = QCheckBox('Whether to use raw Nucleus to segment')
        self.Nuc.stateChanged.connect(self.Nucchange)
        self.Nucinput = False
        # 栅格布局第三列是参数选择按钮
        projectFolderBtn = QPushButton("Select")
        projectFolderBtn.clicked.connect(self.chooseProjectFolder)
        self.embryoNameBtn = QComboBox()

        grid = QGridLayout()
        grid.setSpacing(30)

        grid.addWidget(projectFolder, 1, 0)
        grid.addWidget(self.projectFolderEdit, 1, 1)
        grid.addWidget(projectFolderBtn, 1, 2)

        grid.addWidget(embryoName, 2, 0)
        grid.addWidget(self.embryoNameBtn, 2, 1)

        grid.addWidget(modelName, 3, 0)
        grid.addWidget(self.modelNameEdit, 3, 1)

        grid.addWidget(GPU, 4, 0)
        grid.addWidget(self.GPU, 4, 1)

        grid.addWidget(Nuc, 5, 0)
        grid.addWidget(self.Nuc, 5, 1)

        self.mainlayout.addLayout(grid)

    def chooseProjectFolder(self):
        dirName = QFileDialog.getExistingDirectory(self, 'Choose RawStack Folder', './')
        try:
            self.textEdit.clear()
            self.embryoNameBtn.clear()
            self.projectFolderEdit.setText(dirName)
            if dirName:
                listdir = [x for x in os.listdir(os.path.join(dirName, "RawStack")) if not x.startswith(".")]
                listdir.sort()
                self.embryoNameBtn.addItems(listdir)
        except Exception as e:
            self.textEdit.setText(traceback.format_exc())
            QMessageBox.warning(self, 'Warning!', 'Please Choose Right Folder!')

    def runSegmentation(self):
        para = {}
        try:
            para = read_yaml_to_dict(os.path.join("./static/configs", self.modelNameEdit.currentText() + ".yaml"))

            np.random.seed(para.get("seed"))
            random.seed(para.get("seed"))
            torch.manual_seed(para.get("seed"))
            torch.cuda.manual_seed(para.get("seed"))

            Network = getattr(networks, para.get("net"))
            net_params = para.get("net_params")
            img_size = net_params.get("img_size")
            img_size = parse_tuple(img_size)
            net_params["img_size"] = img_size
            model = Network(**net_params)

            Dataset = getattr(dataset, para.get("dataset_name"))
            memb_dataset = Dataset(
                root=self.projectFolderEdit.text(),
                embryoname=self.embryoNameBtn.currentText(),
                is_input_nuc=self.Nucinput,
                transforms=para.get("transforms")
            )
            memb_loader = DataLoader(
                dataset=memb_dataset,
                batch_size=1,
                shuffle=False,
            )

            if self.GPUcheck:
                assert torch.cuda.is_available()
                device = torch.device("cuda:0")
                model = model.to(device)
            else:
                device = torch.device("cpu")
                model = model.to(device)
        except:
            para.clear()
            self.textEdit.setText(traceback.format_exc())
            QMessageBox.warning(self, 'Error!', 'Initialization Failure!')

        if para:
            try:
                self.textEdit.clear()
                self.textEdit.append("Running Segmentation!")
                self.textEdit.append(f"The model name is {self.modelNameEdit.currentText()}")
                self.textEdit.append(f"The network parameters are {para.get('net_params')}")
                self.textEdit.append(f"The dataset name is {para.get('dataset_name')}")
                self.textEdit.append(f"Use GPU : {self.GPUcheck}")
                self.textEdit.append(f"Use nucleus information :{self.Nucinput}")

                with torch.no_grad():
                    model.eval()
                    for i, data in enumerate(memb_loader):
                        raw_memb = data[0]
                        raw_memb_shape = data[1]
                        embryo_name_tp = data[2][0]
                        raw_memb_shape = (raw_memb_shape[0].item(), raw_memb_shape[1].item(), raw_memb_shape[2].item())
                        pred_memb = model(raw_memb.to(device))
                        pred_memb = pred_memb[0] if len(pred_memb) > 1 else pred_memb

                        pred_memb = pred_memb[0, 0, :, :, :]
                        pred_memb = pred_memb.cpu().numpy().transpose([1, 2, 0])
                        pred_memb = resize(pred_memb,
                                           raw_memb_shape,
                                           mode='constant',
                                           cval=0,
                                           order=1,
                                           anti_aliasing=True)

                        save_path = os.path.join(self.projectFolderEdit.text(), "SegStack", self.embryoNameBtn.currentText(),
                                                 "SegMemb", self.modelNameEdit.currentText())
                        if not os.path.isdir(save_path):
                            os.makedirs(save_path)
                        save_name = os.path.join(save_path, embryo_name_tp + "_segMemb.nii.gz")
                        nib_stack = nib.Nifti1Image((pred_memb * 256).astype(np.int16), np.eye(4))
                        nib.save(nib_stack, save_name)
                        break

            except:
                self.textEdit.append(traceback.format_exc())
                QMessageBox.warning(self, 'Error!', 'Can not start Segmentation!')

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

    def Nucchange(self, state):
        if state == Qt.Checked:
            self.Nuc.setText("Use raw Nucleus infomation")
            self.Nucinput = True
        else:
            self.Nuc.setText("Don't use Nucleus infomation")
            self.Nucinput = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Memb_Segmentation()
    sys.exit(app.exec_())
