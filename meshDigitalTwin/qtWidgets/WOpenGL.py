from PyQt5 import QtWidgets, QtGui, QtCore
from OpenGL import GL
from meshDigitalTwin.glEngine.EMesh   import EMesh
from meshDigitalTwin.glEngine.EModel  import EModel
from meshDigitalTwin.glEngine.EShader import EShader
from meshDigitalTwin.glEngine.ECamera import ECamera
from meshDigitalTwin.glEngine.ELoader import ELoader
import glm

class WOpenGL( QtWidgets.QOpenGLWidget ):
    def __init__(self, parent=None):
        super( QtWidgets.QOpenGLWidget, self ).__init__( parent=parent )
        self.setObjectName("OpenGL")
        self.loader = ELoader( "Elements.txt", "Nodes.txt" )
        self.model = EModel( "model", self.loader.nodes )
        self.mu = 0.0
        self.setMouseCallbacks()

    def initializeGL(self):
        ratio = self.size().width() / self.size().height()
        GL.glEnable( GL.GL_DEPTH_TEST )
        self.shader  = EShader()
        self.mesh    = EMesh( self.shader, self.loader.nodes, self.loader.elements )
        self.camera  = ECamera( self.shader, [ 0.0, 0.0, 10.0 ], ratio=ratio )
        #GL.glPolygonMode( GL.GL_FRONT_AND_BACK, GL.GL_LINE )
        print( "Entering polling loop" )
        
    def paintGL(self):
        self._open()

        self.mesh.draw()

        self._close()

    def _open(self):
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glClear( GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    def _close(self):
        self.camera.updateView()
        array = self.model.eval( self.mu )
        self.mesh.updateData( array )

    def deleteScene( self ):
        self.mesh.delete()
        self.shader.delete()

    def setMouseCallbacks( self ):
        self._pos   = None
        self._flagL = False
        self._flagR = False
        self._time  = 0
        self.setMouseTracking( True )

    def _getPos( e : QtGui.QMouseEvent ):
        pos = e.pos()
        return glm.fvec2( pos.x(), pos.y() )

    def mouseMoveEvent( self, e : QtGui.QMouseEvent ):
        flagL = e.buttons() & QtCore.Qt.MouseButton.LeftButton
        flagR = e.buttons() & QtCore.Qt.MouseButton.RightButton
        if flagL or flagR:
            pos = WOpenGL._getPos( e )
            #time = e.timestamp()
            delta = - 0.01 * ( pos - self._pos) #/ ( time - self._time )
            self._pos = pos
            #self._time = time
            if flagL and not flagR: self.camera.rotCamera( *delta )
            else: self.camera.moveCamera( *delta )
        else:
            self._pos  = WOpenGL._getPos( e )
            #self._time = e.timestamp()
    
    def wheelEvent( self, e : QtGui.QWheelEvent ):
        if e.angleDelta().y() > 0: self.camera.zoomCamera( 0.4 )
        else: self.camera.zoomCamera( -0.4 )