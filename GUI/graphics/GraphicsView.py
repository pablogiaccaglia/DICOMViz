import pyqtgraph
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene


class GraphicsView(QGraphicsView):

    def __init__(self, centralWidget):
        super().__init__(centralWidget)

        self.fatherWidget = centralWidget
        self.setObjectName("graphicsView")
        self.scene = QGraphicsScene()
        self.image = pyqtgraph.ImageView()
        self.proxySceneWidget = None

        self.noimg = None

    def setImageToView(self, img):
        if img is None:  # if the image is None use the default "no image" object
            img = self.noimg
            # elif len(img.shape)==3: # multi-channel or multi-dimensional image, use average of dimensions
            #    img=np.mean(img,axis=2)

        self.image.clear()
        self.image = pyqtgraph.image(img, title = "DICOM")

        self.proxySceneWidget = self.scene.addWidget(self.image)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setScene(self.scene)
        self.resizeEvent()

    def resizeEvent(self, event = None):
        try:
            self.proxySceneWidget.setMinimumSize(
                self.fatherWidget.size().width() - self.fatherWidget.size().width() / 30,
                self.fatherWidget.size().height() - self.fatherWidget.size().height() / 30)
            self.proxySceneWidget.setMaximumSize(
                self.fatherWidget.size().width() - self.fatherWidget.size().width() / 30,
                self.fatherWidget.size().height() - self.fatherWidget.size().height() / 30)
        except:
            pass