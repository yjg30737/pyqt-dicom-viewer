import numpy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class DicomImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__gradient_enabled = False
        self.__initVal()

    def __initVal(self):
        self._scene = QGraphicsScene()
        self._p = QPixmap()
        self._item = ''

    def setNdArray(self, dicom_file_data, width, height):
        # Convert to QImage - for 8-bit grayscale image
        q_image = QImage(dicom_file_data, width, height, width, QImage.Format_Grayscale8)

        # Convert QImage to QPixmap
        self._p = QPixmap.fromImage(q_image)

        # The rest of your code remains the same
        self._scene = QGraphicsScene()
        self._item = self._scene.addPixmap(self._p)
        self._item.setTransformationMode(Qt.SmoothTransformation)
        self.setScene(self._scene)
        self.fitInView(self._item, self.__aspectRatioMode)

    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode

    def resizeEvent(self, e):
        if self._item:
            self.fitInView(self.sceneRect(), self.__aspectRatioMode)
        return super().resizeEvent(e)


class DicomImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__current_dicom_file_info = []
        self.__cur_idx = 0

    def __initUi(self):
        self.__view = DicomImageView()

        self.__prevBtn = QPushButton('Prev')
        self.__prevBtn.clicked.connect(self.__prev)
        self.__nextBtn = QPushButton('Next')
        self.__nextBtn.clicked.connect(self.__next)

        lay = QHBoxLayout()
        lay.addWidget(self.__prevBtn)
        lay.addWidget(self.__nextBtn)
        lay.setContentsMargins(0, 0, 0, 0)
        btnWidget = QWidget()
        btnWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(self.__view)
        lay.addWidget(btnWidget)
        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)

    def __toggleBtn(self):
        self.__prevBtn.setEnabled(not self.__cur_idx == 0)
        self.__nextBtn.setEnabled(not (self.__cur_idx == len(self.__current_dicom_file_info['data']) - 1))

    def __setNdArray(self):
        self.__view.setNdArray(dicom_file_data=self.__current_dicom_file_info['data'][self.__cur_idx],
                               width=self.__current_dicom_file_info['width'],
                               height=self.__current_dicom_file_info['height'])

    def setDicomArr(self, dicom_file_info):
        self.__cur_idx = 0
        self.__current_dicom_file_info = dicom_file_info
        self.__setNdArray()
        self.__toggleBtn()

    def __prev(self):
        self.__cur_idx -= 1
        self.__cur_idx = max(0, self.__cur_idx)
        self.__toggleBtn()
        self.__setNdArray()

    def __next(self):
        self.__cur_idx += 1
        self.__cur_idx = min(len(self.__current_dicom_file_info['data'])-1, self.__cur_idx)
        self.__toggleBtn()
        self.__setNdArray()

    def keyReleaseEvent(self, e):
        # 16777234 is left
        if e.key() == 16777234:
            self.__prev()
        # 16777236 is right
        elif e.key() == 16777236:
            self.__next()
        return super().keyReleaseEvent(e)

    def wheelEvent(self, e):
        if e.angleDelta().y() < 0:
            self.__next()
        else:
            self.__prev()
        return super().wheelEvent(e)