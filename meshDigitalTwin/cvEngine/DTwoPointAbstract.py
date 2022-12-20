from meshDigitalTwin.cvEngine.DPoint import DPoint

class DTwoPointAbstract:
    def __init__( self, pa: DPoint = None, pb : DPoint = None ):
        self.pa = DPoint()
        self.pb = DPoint()
        if not isinstance( pa, type(None) ):
            self.pa = pa
        if not isinstance( pb, type(None) ):
            self.pb = pb

    def set( self, pa:DPoint, pb:DPoint ):
        self.pa = pa
        self.pb = pb

    def unset( self ):
        self.pa.unset()
        self.pb.unset()

    def setBBox( self, x, y, w, h, cor : DPoint = None ):
        if isinstance( cor, DPoint ):
            self.pa.set( x + cor.x , y + cor.y )
            self.pb.set( x + w + cor.x, y + h + cor.y )
        else:
            self.pa.set( x , y )
            self.pb.set( x + w, y + h )

    def getBBox( self, cor : DPoint = None ):
        pmin = DPoint.min( self.pa, self.pb )
        pdif = DPoint.max( self.pa, self.pb ) - pmin
        if isinstance( cor,DPoint ):
            pmin = pmin + cor
        return pmin.x, pmin.y, pdif.x, pdif.y

    def get( self ):
        pmin = DPoint.min( self.pa, self.pb )
        pmax = DPoint.max( self.pa, self.pb )
        return pmin.x, pmax.x, pmin.y, pmax.y

    def get_centre( self ) -> DPoint:
        return self.pa + ( self.pb - self.pa ) // 2

    def draw( self, img ):
        pass

    def enum( self, iter, i : int = None ):
        if isinstance( i, type(None) ):
            try:
                n = next( iter )
            except StopIteration:
                raise Exception( "Max nodes reached" )
            return n
        else:
            return i

    def __bool__( self ) -> bool:
        if bool( self.pa ) and bool( self.pb ):
            return True
        return False
    def __str__(self) -> str:
        return f"{self.pa} : {self.pb}"

