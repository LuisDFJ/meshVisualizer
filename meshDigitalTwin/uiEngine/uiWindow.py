from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from meshDigitalTwin.uiEngine.uiWindowS import uiWindowS

class uiWindow( QMainWindow, uiWindowS ):
    def __init__( self, parent=None ):
        QMainWindow.__init__(self, parent=parent)
        self.setupUI(self)
        fps_g = 60
        fps_v = 30
        self.timer_graphics = QTimer(self)
        self.timer_graphics.setInterval( int( 1000 / fps_g ) )
        self.timer_graphics.timeout.connect(self.updateGL)
        #timer_graphics.timeout.connect(self.glWidget.update)

        self.timer_video = QTimer(self)
        self.timer_video.setInterval( int( 1000 / fps_v ) )
        self.timer_video.timeout.connect( self.video.update )
        
        self.timer_graphics.start()
        self.timer_video.start()

        
        
        #self.video_thread = WThreadVideo(self)
        #self.video_thread.videoStream.connect(self.videoStreamCallback)
        #self.video_thread.start()
        #timer_keyboard = QTimer(self)
        #timer_keyboard.setInterval(20)
        #timer_keyboard.timeout.connect(self.keyboardHandler)
    
    def updateGL( self ):
        self.glWidget.mu = self.video.mu
        self.glWidget.update()

    def closeEvent(self, e):
        self.timer_graphics.stop()
        self.timer_video.stop()
        self.glWidget.deleteScene()
        self.glWidget.deleteLater()
        self.glWidget = None
        print( "Closing Window" )