from meshDigitalTwin.cvEngine.DNodes import DNodes
from meshDigitalTwin.cvEngine.DPoint import DPoint
import cv2 as cv

class DTracker:
    TRACK_ALGORITHM = {
        "CSRT"  : cv.legacy.TrackerCSRT.create,
        "MOSSE" : cv.legacy.TrackerMOSSE.create,
        "KCF"   : cv.legacy.TrackerKCF.create
    }
    def __init__( self, img, nodes : DNodes, crops : list, alg = 'CSRT' ):
        self.nodes = nodes
        self.crops = self.parse_crops( crops )
        self.tracker = [ self.TRACK_ALGORITHM[ alg ]() for _ in self.nodes.nodes ]
        self.init_tracker( img )

    def parse_crops( self, crops_list ):
        crops = {}
        for rect in crops_list:
            if bool( rect ):
                crops[ rect.n ] = rect
        return crops

    def get_crop_image( self, img, i ):
        if i in list( self.crops.keys() ):
            return self.crops[ i ].crop( img )
        return img, DPoint( 0,0 )

    def init_tracker( self, img ):
        for i, rect in enumerate( self.nodes.nodes.items() ):
            frame, cor = self.get_crop_image( img, rect[0] )
            self.tracker[i].init( frame, rect[1].getBBox( -cor ) )

    def update( self, img ):
        for i, rect in enumerate( self.nodes.nodes.items() ):
            frame, cor = self.get_crop_image( img, rect[0] )
            success, bbox = self.tracker[i].update( frame )
            if success: rect[1].setBBox( *bbox, cor )
            