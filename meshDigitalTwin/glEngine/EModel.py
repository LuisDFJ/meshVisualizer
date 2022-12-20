import os
import csv
import math
import numpy as np
from meshDigitalTwin.glEngine.media import PATH_MEDIA
#PATH_MEDIA = r"C:\workspace\projects\MCI-stuff\meshVisualizer\glEngine\media"

class EModel:
    def __init__( self, model : str, nodes : np.ndarray, mumax = 5.5 ):
        _base_path = os.path.join( PATH_MEDIA, model )
        basis_path = os.path.join( _base_path, "basis.txt" )
        coeff_path = os.path.join( _base_path, "coefficients.txt" )
        self.basis = self.loadFile( basis_path, [0,4], np.float32 )
        self.coeff = self.loadFile( coeff_path, [0,2], np.float32 )
        self.ldis, self.lstr = self.initFunctions( self.coeff )
        self.nodes = nodes
        self.mumax = mumax
        self.adjustEquivalentStress( mumax )

    def loadFile( self, path, slice, dtype ):
        with open( path, 'r' ) as pFile:
            reader = csv.reader( pFile, delimiter='\t' )
            list_rows = [ row[ slice[0]:slice[1] ] for row in reader ]
        return np.array( list_rows, dtype=dtype )

    def initFunctions( self, coeff : np.ndarray ):
        ldis = lambda mu : 0.1 * ( coeff[0,0] + coeff[0,1] * mu )
        lstr = lambda mu : abs( coeff[0,0] + coeff[0,1] * mu )
        return ldis, lstr

    def adjustEquivalentStress( self, mumax ):
        Vmax = np.max( self.basis[ :, 3 ] )
        Vmin = np.min( self.basis[ :, 3 ] )
        vbasis = ( self.basis[ :, 3 ] - Vmin ) / (Vmax - Vmin)
        vbasis = vbasis / self.lstr( mumax )
        self.basis[ :, 3 ] = vbasis

    def eval( self, mu : float = 0.0 ):
        d = self.ldis( mu ) ; s = self.lstr( mu )
        nodes = self.nodes + d * self.basis[ :, 0:3 ]
        stress = s * self.basis[ :, 3 ].reshape( len( nodes ), 1 )
        return np.hstack( [ nodes, stress ] )

if __name__ == "__main__":
    model = EModel( "model" )
    model.eval(1)
