import glfw
import numpy as np
import glm
import math
from glEngine.EShader import EShader

class ECamera:
    def __init__(self, window, shader : EShader, ViewPosition : list = [0.0,5.0,-5.0], ViewPoint : list = [0.0,0.0,0.0], ViewUp : list = [0.0,1.0,0.0], fov : float = 45.0 ) -> None:
        [w,h] = glfw.get_window_size(window)
        ratio = w/h
        self.shader = shader
        self.ViewPosition   = glm.fvec3( *ViewPosition )
        self.ViewPoint      = glm.fvec3( *ViewPoint )
        self.ViewUp         = glm.fvec3( *ViewUp )
        
        self.perspective    = np.array( glm.perspective( glm.radians( fov ), ratio, 0.1, 100.0 ) ).astype( np.float32 )
        [self.rho, self.theta, self.phi] = ECamera.cartesian2spherical( self.ViewPosition - self.ViewPoint )
        self.setCallbacks( window )
        self.updateView()

    def updateView( self ):
        [view, perspective] = self.getView()
        self.shader.setMatrix4fv( "view", view )
        self.shader.setMatrix4fv( "perspective", perspective )

    def getView( self ):
        return np.array( glm.lookAt( self.ViewPosition, self.ViewPoint, self.ViewUp ) ).astype( np.float32 ), self.perspective

    def rotCamera( self, dtheta : float = 0.0, dphi : float = 0.0 ):
        self.theta = max( min( self.theta + dtheta, glm.radians( 179 ) ), -glm.radians(179) )
        self.phi = max( min( self.phi + dphi, glm.radians( 179 ) ), glm.radians(1) )
        self.updatePosition()

    def zoomCamera( self, drho : float = 0.0 ):
        self.rho = self.rho + drho
        self.updatePosition()

    def moveCamera( self, dx : float = 0.0, dy : float = 0.0 ):
        front = glm.normalize( self.ViewPoint - self.ViewPosition )
        right = glm.normalize( glm.cross( self.ViewUp, front ) )
        up = glm.cross( front, right )
        delta = dx * right + dy * up
        self.ViewPosition = self.ViewPosition - delta
        self.ViewPoint = self.ViewPoint - delta

    def spherical2cartesian( rho : float, theta : float, phi : float ):
        z = rho * glm.sin( phi ) * glm.cos( theta )
        x = rho * glm.sin( phi ) * glm.sin( theta )
        y = rho * glm.cos( phi )
        return glm.fvec3( x,y,z )

    def cartesian2spherical( pos : glm.fvec3 ):
        rho   = glm.length( pos )
        theta = math.atan2( pos[0], pos[2] )
        phi   = glm.acos( pos[1] / rho )
        return rho, theta, phi
        
    def updatePosition( self ):
        self.ViewPosition = ECamera.spherical2cartesian( self.rho, self.theta, self.phi ) + self.ViewPoint

    def setCallbacks( self, window ):
        self._pos = None
        self._flagL = False
        self._flagR = False
        self._time = 0
        glfw.set_cursor_pos_callback( window, self.cursor_pos_callback )
        glfw.set_mouse_button_callback( window, self.mouse_button_callback )
        glfw.set_scroll_callback( window, self.scroll_callback )


    def cursor_pos_callback( self, window, x, y ):
        if self._flagL or self._flagR:
            pos = glm.fvec2( x, y )
            time = glfw.get_time()
            delta = - 0.4 * ( pos - self._pos) * ( time - self._time )
            self._pos = pos
            self._time = time
            if self._flagL: self.rotCamera( *delta )
            else: self.moveCamera( *delta )

            

    def mouse_button_callback( self, window, button, action, mod ):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self._flagL = True
                self._flagR = False
                self._pos = glm.fvec2( glfw.get_cursor_pos( window ) )
                self._time = glfw.get_time()
            else: self._flagL = False
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            if action == glfw.PRESS:
                self._flagL = False
                self._flagR = True
                self._pos = glm.fvec2( glfw.get_cursor_pos( window ) )
                self._time = glfw.get_time()
            else: self._flagR = False

    def scroll_callback( self, window, xoffset, yoffset ):
        self.zoomCamera( 0.4 * yoffset )
        


    

