import os

def read_shaders():
    vPath = os.path.join( os.path.dirname(__file__), "VertexShader.glsl" )
    fPath = os.path.join( os.path.dirname(__file__), "FragmentShader.glsl" )
    with open( vPath, "r" ) as vFile: vShader = vFile.read()
    with open( fPath, "r" ) as fFile: fShader = fFile.read()
    return vShader, fShader

[ VERTEX_SHADER, FRAGMENT_SHADER ] = read_shaders()