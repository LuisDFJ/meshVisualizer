from PyQt5 import  QtWidgets
from meshDigitalTwin.uiEngine.uiWindow import uiWindow

if __name__ == "__main__":
    app     = QtWidgets.QApplication([])
    window = uiWindow()
    window.show()
    app.exec_()