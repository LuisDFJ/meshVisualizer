import cv2 as cv
from utils.DMouseTracker import DMouseTracker
from utils.DTracker import DTracker

node_list = [
    ( 1,2 ),
    ( 2,3 ),
    ( 3,4 ),
    ( 4,1 ),
]



if __name__ == "__main__":
    
    cap = cv.VideoCapture( 1, cv.CAP_DSHOW )
    
    mt = DMouseTracker( 5 )
    
    cv.namedWindow( 'Video' )
    cv.setMouseCallback( 'Video', mt.mouse_callback )
    if cap.isOpened():
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            mt.draw( frame )

            cv.imshow( 'Video', frame )

            key = cv.waitKey( 1 )
            if key == ord( 'q' ):
                break

        nodes = mt.get( node_list )
        mc = DMouseTracker( nodes.size(), False )
        cv.setMouseCallback( 'Video', mc.mouse_callback )
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            mt.draw( frame )
            mc.draw( frame )

            cv.imshow( 'Video', frame )

            key = cv.waitKey( 1 )
            if key == ord( 'q' ):
                break

        cv.setMouseCallback( 'Video', lambda *_: None )
        tracker = DTracker( frame, nodes, mc.get_rects() )

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            
            tracker.update( frame )
            nodes.update()
            nodes.draw( frame )

            cv.imshow( 'Video', frame )

            key = cv.waitKey( 1 )
            if key == ord( 'q' ):
                break

    cv.destroyAllWindows()
