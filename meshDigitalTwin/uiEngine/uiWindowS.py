from PyQt5 import QtCore, QtGui, QtWidgets
from meshDigitalTwin.qtWidgets.WOpenGL import WOpenGL
from meshDigitalTwin.qtWidgets.WVideoFrame import WVideoFrame

class uiWindowS(object):
    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 490)
        # Central Widget Init
        self.centralwidget  = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.setup()
        # MainWindow Setup
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup(self):
        self._setupCentralWidget( self.centralwidget )

    def _setupCentralWidget(self, widget : QtWidgets.QWidget ):
        layout = QtWidgets.QHBoxLayout()
        sublayout2 = QtWidgets.QVBoxLayout()
        # OpenGL Widget
        size = widget.parentWidget().size()
        self.glWidget = WOpenGL( widget )
        self.glWidget.setGeometry(QtCore.QRect(0, 0, int( 1/2 * size.width() ), size.height()))
        layout.addWidget( self.glWidget )

        self.video = WVideoFrame( widget )
        print( self.video.size() )
        #self.label = QtWidgets.QLabel( widget )
        #self.label.setText( "Hello" )
        #self.label.setGeometry(QtCore.QRect(0, 0, int( 1/2 * size.width() ), size.height()))
        sublayout2.addWidget( self.video )
        
        label = QtWidgets.QLabel( widget )
        sublayout2.addWidget( label )

        layout.addLayout( sublayout2 )
        widget.setLayout( layout )
        