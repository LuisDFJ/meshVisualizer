from OpenGL import GL
from glEngine.EShader import EShader
import numpy as np

class EMesh:
    def __init__(self, shader : EShader, nodes : np.ndarray, elements : np.ndarray ) -> None:
        self.VAO = GL.glGenVertexArrays(1)
        self.VBO = GL.glGenBuffers(1)
        self.EBO = GL.glGenBuffers(1)
        self.shader = shader
        self.elSize = elements.size

        self.activate()
        self.bindVBO( nodes )
        self.bindEBO( elements )
        
        self.setArrayf( "position", 3, 12 )
        

        # get the color from  shader
        #color = glGetAttribLocation(shader, 'color')
        #glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        #glEnableVertexAttribArray(color)
    
    def setArrayf( self, name : str, vals : int, size : int ):
        location = self.shader.getAttributeLocation( name )
        GL.glVertexAttribPointer(location, vals, GL.GL_FLOAT, GL.GL_FALSE, size, GL.ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(location)

    def activate( self ):
        GL.glBindVertexArray( self.VAO )
    
    def bindVBO( self, array : np.ndarray ):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * array.size, array, GL.GL_STATIC_DRAW)

    def bindEBO( self, array : np.ndarray ):
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, 4 * array.size, array, GL.GL_STATIC_DRAW)
    
    def draw( self ):
        self.shader.activate()
        GL.glBindVertexArray(self.VAO)
        GL.glDrawElements( GL.GL_TRIANGLES, self.elSize, GL.GL_UNSIGNED_INT,  None)

    def delete( self ):
        GL.glDeleteVertexArrays( 1, [self.VAO] )
        GL.glDeleteBuffers( 1, [self.VBO] )
        GL.glDeleteBuffers( 1, [self.EBO] )
