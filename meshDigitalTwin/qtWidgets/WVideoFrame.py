from PyQt5 import QtWidgets, QtGui, QtCore
from meshDigitalTwin.cvEngine.DTracker import DTracker
from meshDigitalTwin.cvEngine.DRectangle import DRectangle
from meshDigitalTwin.cvEngine.DMouseTracker import DMouseTracker
import cv2
import glm

node_list = [
    ( 1,2 ),
    ( 2,3 ),
    ( 3,4 ),
    ( 4,1 ),
]

class WVideoFrame( QtWidgets.QLabel ):
    STATE_NODES = 0
    STATE_BOXES = 1
    STATE_READY = 2

    def __init__( self, parent=None ):
        super( QtWidgets.QLabel, self ).__init__( parent=parent )
        self.setObjectName( "VideoFrame" )
        self.setMouseCallbacks()
        self.mt = DMouseTracker( 5 )
        self.mc = None
        self.nodes = None
        self.tracker = None
        self.mu = 0.0
        self.gen = self.run()
        self.update()
        self.resize( self.sizeHint() )
    
    def update( self ):
        frame = next( self.gen )
        if not frame == None:
            self.setPixmap( QtGui.QPixmap.fromImage( frame ) )
    
    def run( self ):
        self.active = True
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            if self.active:
                ret, frame = capture.read()
                if ret:
                    #image = frame
                    image   = cv2.flip( cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1 )
                    self._draw( image )
                    imageQt = QtGui.QImage( image.data, image.shape[1], image.shape[0], QtGui.QImage.Format.Format_RGB888 )
                    #pic     = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    yield imageQt
            else:
                yield None

    def stop( self ):
        self.active = False

    def setMouseCallbacks( self ):
        self._pos    = None
        self._flagL  = False
        self._states = self._genState()
        self._state  = next( self._states )
        self.setMouseTracking( True )

    def _getPos( e : QtGui.QMouseEvent ):
        pos = e.pos()
        return glm.fvec2( pos.x(), pos.y() )

    def _updateMu( self ):
        if not isinstance( self.nodes, type( None ) ):
            line = self.nodes.lines[ 0 ]
            a = line.pa.x
            b = line.pb.x
            #print( a, b )
            self.mu = - 0.2 * ( b - a )

    def _genState( self ):
        yield WVideoFrame.STATE_NODES
        yield WVideoFrame.STATE_BOXES
        while True: yield WVideoFrame.STATE_READY

    def _getMc( self ):
        if isinstance( self.nodes, type(None) ):
            self.nodes = self.mt.get( node_list )
            self.mc = DMouseTracker( self.nodes.size(), False )
        return self.mc

    def _getTracker( self, frame ):
        if isinstance( self.tracker, type(None) ):
            self.tracker = DTracker( frame, self.nodes, self.mc.get_rects() )
        return self.tracker

    def _mouse_callback( self, *args ):
        if self._state == self.STATE_NODES:
            self.mt.mouse_callback( *args )
        elif self._state == self.STATE_BOXES:
            self._getMc().mouse_callback( *args )
        elif self._state == self.STATE_READY:
            pass

    def _draw( self, image ):
        if self._state == self.STATE_NODES:
            self.mt.draw( image )
        elif self._state == self.STATE_BOXES:
            self.mt.draw( image )
            self._getMc().draw( image )
        elif self._state == self.STATE_READY:
            self._getTracker( image ).update( image )
            self.nodes.update()
            self.nodes.draw( image )
            self._updateMu()

    def mouseMoveEvent( self, e : QtGui.QMouseEvent ):
        if self._flagL:
            pos = WVideoFrame._getPos( e )
            self._mouse_callback( DRectangle.EVENT_LHOVER, *pos )
        
    def mousePressEvent( self, e : QtGui.QMouseEvent ):
        flagL = e.buttons() & QtCore.Qt.MouseButton.LeftButton
        flagC = e.buttons() & QtCore.Qt.MouseButton.MiddleButton
        if flagL:
            if not self._flagL:
                self._flagL = True
                pos = WVideoFrame._getPos( e )
                self._mouse_callback( DRectangle.EVENT_LPRESS, *pos )
        if flagC:
            self._state = next( self._states )

    def mouseReleaseEvent( self, e : QtGui.QMouseEvent ):
        flagL = e.buttons() & QtCore.Qt.MouseButton.LeftButton
        if not flagL:
            if self._flagL:
                self._flagL = False
                pos = WVideoFrame._getPos( e )
                self._mouse_callback( DRectangle.EVENT_LRELEASE, *pos )