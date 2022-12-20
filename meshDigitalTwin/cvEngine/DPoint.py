class DPoint:
    def __init__(self, x : int = None, y : int = None ):
        self.x = x
        self.y = y
    
    def set( self, x : int,  y : int ):
        self.x = int( x )
        self.y = int( y )

    def unset( self ):
        self.x = None
        self.y = None

    @property
    def x( self ):
        return self._x
    @x.setter
    def x( self, val : int = None ):
        self._x = val

    @property
    def y( self ):
        return self._y
    @y.setter
    def y( self, val : int = None ):
        self._y = val

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    def __bool__(self) -> bool:
        if not isinstance(self.x, type(None) ) and not isinstance(self.y, type(None) ):
            return True
        return False
    def __iter__(self):
        yield self.x
        yield self.y
    def __add__(self, A):
        return DPoint( self.x + A.x, self.y + A.y )
    def __sub__(self, A):
        return DPoint( self.x - A.x, self.y - A.y )
    def __neg__(self):
        return DPoint( -self.x, -self.y )
    def __truediv__(self, a):
        return DPoint( self.x / a, self.y / a )
    def __floordiv__(self, a):
        return DPoint( self.x // a, self.y // a )


    def max( pa, pb ):
        x = max( pa.x, pb.x )
        y = max( pa.y, pb.y )
        return DPoint( x,y )
    def min( pa, pb ):
        x = min( pa.x, pb.x )
        y = min( pa.y, pb.y )
        return DPoint( x,y )
    
