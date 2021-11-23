import pyqtgraph

from GUI.graphics.CustomViewBox import CustomViewBox


class CustomImageView(pyqtgraph.ImageView):
    """
    Subclass of PlotWidget
    """
    def __init__(self, parent=None):
        """
        Constructor of the widget
        """
        super(CustomImageView, self).__init__(parent, view= CustomViewBox())