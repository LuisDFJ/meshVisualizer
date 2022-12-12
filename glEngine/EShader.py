from OpenGL import GL
from glEngine.shaders import VERTEX_SHADER, FRAGMENT_SHADER


class EShader:
    def __init__(self) -> None:
        import OpenGL.GL.shaders
        self.id = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL.GL_FRAGMENT_SHADER)
        )

    def getAttributeLocation( self, name: str ):
        return GL.glGetAttribLocation( self.id, name )

    def getUniformLocation( self, name: str ):
        return GL.glGetUniformLocation( self.id, name )

    def setMatrix4fv( self, name, t ):
        self.activate()
        location = self.getUniformLocation( name )
        GL.glUniformMatrix4fv( location, 1, GL.GL_TRUE, t )
    
    def activate( self ):
        GL.glUseProgram( self.id )

    def delete( self ):
        GL.glDeleteProgram( self.id )
    
