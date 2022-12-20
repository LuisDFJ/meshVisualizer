from meshDigitalTwin.cvEngine.DNodes import DNodes
from meshDigitalTwin.cvEngine.DRectangle import DRectangle

class DMouseTracker:
    def __init__( self, n, autoenum : bool = True ):
        self.n = n
        if  autoenum: self.rectangles = [ DRectangle() for _ in range( n ) ]
        else        : self.rectangles = [ DRectangle( n=i ) for i in range( 1, n + 1 ) ]
        self.pRect = self.gen_iter()
        self.cRect = next( self.pRect )

    def gen_iter( self ):
        while True:
            for rect in self.rectangles:
                yield rect

    def mouse_callback( self, event, x, y ):
        if self.cRect.mouse_callback( event, x, y ):
            self.cRect = next( self.pRect )

    def draw( self, img ):
        for rect in self.rectangles:
            rect.draw( img )

    def get( self, *args ):
        return DNodes( self.rectangles, *args )

    def get_rects( self ):
        return self.rectangles