from random import randint
from meshDigitalTwin.cvEngine.DPoint import DPoint
from meshDigitalTwin.cvEngine.DTwoPointAbstract import DTwoPointAbstract

import cv2 as cv

class DRectangle (DTwoPointAbstract):
    MAX_ENUM = 10
    __enumarator = ( i for i in range( 1, MAX_ENUM + 1 ) )
    colors = {}
    EVENT_LPRESS   = 0
    EVENT_LRELEASE = 1
    EVENT_LHOVER   = 2

    def __init__(self, n : int = None, pa: DPoint = None, pb: DPoint = None):
        super().__init__(pa, pb)
        self.n = self.enum( self.__enumarator, n )
        self.color = self.set_color()
        self._flag = False

    def set_color( self ):
        if self.n in list( self.colors.keys() ):
            return self.colors[ self.n ]
        else:
            color = ( randint( 0,255 ), randint( 0,255 ), randint( 0,255 ) )
            self.colors[ self.n ] = color
            return color

    def crop( self, img ):
        x_min, x_max, y_min, y_max = self.get()
        return img[ y_min:y_max, x_min:x_max ], DPoint( x_min, y_min )

    def mouse_callback( self, event, x, y ):
        if event == self.EVENT_LPRESS:
            self.pa.set( x,y )
            self.pb.unset()
            self._flag = True
        elif event == self.EVENT_LRELEASE:
            self.pb.set( x,y )
            self._flag = False
            return True

        if self._flag:
            if event == self.EVENT_LHOVER:
                self.pb.set( x,y )

        return False

    def draw( self, img ):
        if bool( self ):
            cv.rectangle( img, tuple( self.pa ), tuple( self.pb ), self.color, 2 )
            cv.rectangle( img, tuple( self.pa + DPoint( -1, 0 ) ), tuple( self.pa + DPoint( 15,-10 ) ), self.color, -1 )
            cv.putText( img, str( self.n ), tuple( self.pa ), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv.LINE_AA )
