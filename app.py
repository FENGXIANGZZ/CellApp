from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QDialog, QTableView, QListWidgetItem,
                             QLabel, QSlider, QVBoxLayout, QMainWindow, QLineEdit, QListWidget,
                             QMessageBox, QComboBox, QTableWidgetItem, QAbstractItemView, QCheckBox, QWidget,
                             qApp, QAction, QDesktopWidget, QMenu, QTabWidget, QTextEdit, QFileDialog)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextCursor, QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QRect, QMetaObject, QCoreApplication
import sys
import os
import traceback
from preprocess import Preprocess
from segmentation import Segmentation
from analysis import Analysis
from train import Train


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.statusbar = self.statusBar()  # 初始化状态栏

        menubar = self.menuBar()  # 初始化菜单栏

        fileMenu = menubar.addMenu("File")  # 添加File选项到菜单栏

        filebutton1 = QAction("New Project", self)  # 添加new_project按钮到File选项
        filebutton1.setStatusTip("Create a new project")
        fileMenu.addAction(filebutton1)

        filebutton2 = QAction("Save Project", self)  # 添加save_project按钮到File选项
        filebutton2.setStatusTip("Save the project")
        fileMenu.addAction(filebutton2)

        filebutton3 = QAction("Load Project", self)  # 添加load_project按钮到File选项
        filebutton3.setStatusTip("Load a origin project")
        fileMenu.addAction(filebutton3)

        runMenu = menubar.addMenu("Run")  # 添加Run选项到菜单栏

        runbutton1 = QAction("Run Preprocess", self)  # 添加run preprocess按钮到Run选项
        runbutton1.setStatusTip("Preprocess the files")
        runMenu.addAction(runbutton1)

        runbutton2 = QAction("Run Segmentation", self)  # 添加run segmentation按钮到Run选项
        runbutton2.setStatusTip("Segment the cell")
        runMenu.addAction(runbutton2)

        runbutton3 = QAction("Run Analysis", self)  # 添加run analysis按钮到Run选项
        runbutton3.setStatusTip("Analyse the result")
        runMenu.addAction(runbutton3)

        runbutton4 = QAction("Run All", self)  # 添加run all按钮到Run选项
        runbutton4.setStatusTip("Run all programs")
        runMenu.addAction(runbutton4)

        runbutton5 = QAction("Open Result Folder", self)  # 添加open result按钮到Run选项
        runbutton5.setStatusTip("Open the result folder")
        runMenu.addAction(runbutton5)

        aboutMenu = menubar.addMenu("About")  # 添加About选项到菜单栏

        aboutbutton1 = QAction("Online Document", self)  # 添加open document按钮到About选项
        aboutbutton1.setStatusTip("Open the document")
        aboutMenu.addAction(aboutbutton1)

        aboutbutton2 = QAction("About CShaperApp", self)  # 添加open introduction按钮到About选项
        aboutbutton2.setStatusTip("Brief introduction of CShaperApp")
        aboutMenu.addAction(aboutbutton2)

        aboutbutton3 = QAction("License", self)  # 添加open license按钮到About选项
        aboutbutton3.setStatusTip("Open the license")
        aboutMenu.addAction(aboutbutton3)

        mainwidget = QWidget()  # 初始化主窗口的主组件
        mainlayout = QGridLayout()  # 初始化主组件的栅格布局
        mainwidget.setLayout(mainlayout)  # 将栅格布局应用到主组件上,可以在初始化时传入父类来简化代码

        self.functionbar = QTabWidget()  # 初始化选项菜单栏
        self.functionbar.setLayoutDirection(Qt.LeftToRight)
        self.functionbar.setTabBarAutoHide(False)
        self.preprocess = Preprocess()
        self.segmentation = Segmentation()
        self.analysis = Analysis()
        self.train = Train()
        self.functionbar.addTab(self.preprocess, "Preprocess")  # 将不同功能的widget放入选项菜单栏
        self.functionbar.addTab(self.segmentation, "Segmentation")
        self.functionbar.addTab(self.analysis, "Analysis")
        self.functionbar.addTab(self.train, "Train")
        self.functionbar.setCurrentIndex(0) #这个函数可以通过下标设置初始化打开那个功能, 默认是第一个
        self.functionbar.currentChanged.connect(self.updateBlankInfo) #功能卡的变化会调用updateBlankInfo这个函数

        mainlayout.addWidget(self.functionbar, 1, 0, 1, 1)  # 将选项菜单栏放入主组件的栅格布局中,位置为第1行第0列

        self.setCentralWidget(mainwidget)  # 将主组件放入主窗口
        self.resize(600, 720)  # 设置窗口大小
        self.setWindowTitle("CShaper")  # 设置窗口标题
        self.setWindowIcon(QIcon("CShaperLogo.png"))  # 设置窗口小图标
        self.show()  # 展示主窗口

    def closeEvent(self, event):
        """
        关闭窗口提醒
        :param event:
        :return:
        """
        reply = QMessageBox.question(self, "quit confirm",
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        """
        窗口居中
        :return:
        """
        qr = self.frameGeometry()  # 获取主窗口框架
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心
        qr.moveCenter(cp)  # 将框架中心移动到屏幕中心
        self.move(qr.topLeft())  # 将主窗口左上角与框架左上角对齐


    def contextMenuEvent(self, event):
        """
        右键菜单
        使用 exec_() 方法显示菜单。从鼠标右键事件对象中获得当前坐标。
        mapToGlobal() 方法把当前组件的相对坐标转换为窗口 (window) 的绝对坐标
        :param event:
        :return:
        """
        cmenu = QMenu(self)

        runAct = cmenu.addAction("Run")
        clearAct = cmenu.addAction("Clear")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == clearAct:
            if self.functionbar.currentIndex() == 0:
                for item in self.preprocess.findChildren((QLineEdit, QComboBox)):
                    if not item is self.preprocess.findChild(QComboBox, "preprocessObject"):
                        item.clear()
            if self.functionbar.currentIndex() == 1:
                for item in self.segmentation.findChildren((QLineEdit, QComboBox)):
                    item.clear()
            if self.functionbar.currentIndex() == 2:
                for item in self.analysis.findChildren((QLineEdit, QComboBox)):
                    item.clear()
            if self.functionbar.currentIndex() == 3:
                for item in self.train.findChildren((QLineEdit, QComboBox)):
                    item.clear()


    def updateBlankInfo(self):
        """
        用来同步更新参数
        :return:
        """
        if self.functionbar.currentIndex() == 1: #当按钮点到segmentation
            pass
            if self.preprocess.projectFolderEdit.text():
                self.segmentation.membsegment.projectFolderEdit.setText(self.preprocess.projectFolderEdit.text())
                self.segmentation.membsegment.embryoNameBtn.clear()
                if os.path.isdir(os.path.join(self.preprocess.projectFolderEdit.text(), "RawStack")):
                    listdir = [x for x in os.listdir(os.path.join(self.preprocess.projectFolderEdit.text(), "RawStack")) if not x.startswith(".")]
                    listdir.sort()
                    self.segmentation.membsegment.embryoNameBtn.addItems(listdir)
                else:
                    os.makedirs(os.path.join(self.preprocess.projectFolderEdit.text(), "RawStack"))


        if self.functionbar.currentIndex() == 2: #当按钮点到analysis
            if self.preprocess.rawFolderEdit.text():
                self.analysis.rawFolderEdit.setText(self.preprocess.rawFolderEdit.text())
                self.analysis.embryoNamesBtn.clear()
                listdir = [x for x in os.listdir(self.preprocess.rawFolderEdit.text()) if not x.startswith(".")]
                listdir.sort()
                self.analysis.embryoNamesBtn.addItems(listdir)
            if self.preprocess.xyResoluEdit.text():
                self.analysis.xyResoluEdit.setText(self.preprocess.xyResoluEdit.text())
            if self.preprocess.sliceNumEdit.text():
                self.analysis.sliceNumEdit.setText(self.preprocess.sliceNumEdit.text())
            if self.preprocess.projectFolderEdit.text():
                self.analysis.projectFolderEdit.setText(self.preprocess.projectFolderEdit.text())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
