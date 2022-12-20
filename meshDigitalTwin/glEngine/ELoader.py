import os
import csv
import numpy as np
from meshDigitalTwin.glEngine.media import PATH_MEDIA

class ELoader( object ):
    def __init__( self, elementsFile:str, nodesFile:str, interpretor:str = "ANSYS-TET10" ):
        self.elements_path  = os.path.join( PATH_MEDIA, elementsFile )
        self.nodes_path     = os.path.join( PATH_MEDIA, nodesFile )
        if interpretor == "ANSYS-TET10":
            facets          = self._get_boundary_elements( self.loadFile( self.elements_path, [2,-1] , np.uint ) )
            self.elements   = self._split_facet( facets ) - 1
        else:
            self.elements   = self.loadFile( self.elements_path, [0,3] , np.uint ) - 1
        self.nodes          = 0.1 * self.loadFile( self.nodes_path, [1,-1] , np.float32 )
    
    def _get_tet10_facet( self, e : np.ndarray ):
        idx = [
            [ 0, 2, 1, 6, 5, 4 ],
            [ 2, 3, 1, 9, 8, 5 ],
            [ 0, 3, 2, 7, 9, 6 ],
            [ 0, 1, 3, 4, 8, 7 ]
        ]
        idx = np.array( idx, np.int32 )
        return e[ :, idx ].reshape( 4 * len( e ), 6 )

    def _get_boundary_elements( self, elements ):
        f   = self._get_tet10_facet( elements )
        e   = np.sort( f, axis=1 )
        _, i, c = np.unique( e, return_index=True, return_counts=True, axis=0 )
        idx = np.sort( i[c==1] )
        return f[ idx ]
    
    def _split_facet( self, facets ):
        # Nodes [1 4 6; 4 5 6; 4 2 5; 6 5 3]
        e1 = facets[ :, [0,3,5] ]
        e2 = facets[ :, [3,4,5] ]
        e3 = facets[ :, [3,1,4] ]
        e4 = facets[ :, [5,4,2] ]
        els = np.append( e1, e2, axis=0 )
        els = np.append( els, e3, axis=0 )
        els = np.append( els, e4, axis=0 )
        return els

    def loadFile( self, path, slice, dtype ):
        with open( path, 'r' ) as pFile:
            reader = csv.reader( pFile, delimiter='\t' ); next( reader )
            list_rows = [ row[ slice[0]:slice[1] ] for row in reader ]
        return np.array( list_rows, dtype=dtype )

if __name__ == "__main__":
    loader = ELoader( "Elements.txt", "Nodes.txt" )
    elements = loader.elements
    print( elements )
    print( elements.shape )