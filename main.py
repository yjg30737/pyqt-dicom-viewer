import os
import sys

from dicomImageView import DicomImageViewer
from findPathWidget import FindPathWidget
from script import get_dicom_images_in_dir

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QListWidget, QWidget, \
    QSplitter, QSizePolicy
from PyQt5.QtCore import Qt, QCoreApplication, QThread
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__dicom_arr = {}

    def __initUi(self):
        self.setWindowTitle('DICOM File Viewer')
        findPathWidget = FindPathWidget()
        findPathWidget.setAsDirectory(True)
        findPathWidget.added.connect(self.__addToList)
        self.__viewerWidget = DicomImageViewer()
        self.__listWidget = QListWidget()
        self.__listWidget.itemSelectionChanged.connect(self.__setDicomFile)

        splitter = QSplitter()
        splitter.addWidget(self.__listWidget)
        splitter.addWidget(self.__viewerWidget)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([300, 700])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")
        splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(findPathWidget)
        lay.addWidget(splitter)
        lay.setAlignment(Qt.AlignTop)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)
        self.__viewerWidget.setEnabled(False)
        
    def __addToList(self, dirname):
        self.__listWidget.clear()
        self.__dicom_arr = get_dicom_images_in_dir(dirname)
        filenames = [_['filename'] for _ in self.__dicom_arr]
        self.__listWidget.addItems(filenames)
        f = self.__listWidget.count() > 0
        self.__viewerWidget.setEnabled(f)
        if f:
            self.__listWidget.setCurrentRow(0)

    def __setDicomFile(self):
        r_idx = self.__listWidget.currentRow()
        self.__viewerWidget.setDicomArr(self.__dicom_arr[r_idx])
        self.__viewerWidget.setFocus()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())