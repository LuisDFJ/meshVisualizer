from meshDigitalTwin.cvEngine.DLine import DLine

class DNodes:
    def __init__(self, node_list : list, relation_list : list) -> None:
        self.nodes = self.parse_nodes( node_list )
        self.rex = self.parse_rex( relation_list )
        self.lines = [ DLine() for _ in self.rex ]

    def parse_nodes( self, node_list : list ):
        nodes = {}
        for node in node_list:
            if bool( node ):
                nodes[ node.n ] = node
        return nodes

    def size( self ):
        return len( list( self.nodes.keys() ) )

    def parse_rex( self, relation_list : list ):
        rex = []
        relation_list = [ tuple( sorted(rex) ) for rex in relation_list ]
        nodes = list( self.nodes.keys() )
        for relation in relation_list:
            flag = True
            for node in relation:
                if node not in nodes:
                    flag = False
                    break
            if flag and relation not in rex :
                rex.append( relation )
        return rex

    def update( self ):
        for i, rex in enumerate( self.rex ):
            pa = self.nodes.get( rex[0] ).get_centre()
            pb = self.nodes.get( rex[1] ).get_centre()
            self.lines[ i ].set( pa, pb )

    def draw( self, img ):
        for line in self.lines:
            line.draw( img )
        for _,rect  in self.nodes.items():
            rect.draw( img )