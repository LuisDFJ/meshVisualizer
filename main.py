import glfw
from OpenGL import GL
from meshDigitalTwin.glEngine.EMesh   import EMesh
from meshDigitalTwin.glEngine.EModel  import EModel
from meshDigitalTwin.glEngine.EShader import EShader
from meshDigitalTwin.glEngine.ECamera import ECamera
from meshDigitalTwin.glEngine.ELoader import ELoader

#nodes = [
#     0.5,  0.5,  0.5,
#     0.5, -0.5,  0.5,
#    -0.5, -0.5,  0.5,
#    -0.5,  0.5,  0.5,
#     0.5,  0.5, -0.5,
#     0.5, -0.5, -0.5,
#    -0.5, -0.5, -0.5,
#    -0.5,  0.5, -0.5 
#]
#nodes = np.array( nodes, dtype=np.float32)

#elements = [
#    7, 5, 4,
#    4, 7, 6,
#    2, 1, 0,
#    0, 3, 2,
#    3, 7, 6,
#    6, 2, 3,
#    0, 4, 5,
#    5, 1, 0,
#    6, 5, 1,
#    1, 2, 6,
#    7, 4, 0,
#    0, 3, 7 
#]
#elements = np.array(elements, dtype = np.uint32)

loader = ELoader( "Elements.txt", "Nodes.txt" )
nodes = loader.nodes
elements = loader.elements

model = EModel( "model", nodes )

def glInit( window ):
    # Compile The Program and shaders
    GL.glEnable( GL.GL_DEPTH_TEST )
    shader = EShader()
    mesh = EMesh( shader, nodes, elements )
    camera = ECamera( window, shader, [ 0.0, 0.0, 5.0 ] )
    return mesh, shader, camera


def main():
    dfps = 1/60
    if not glfw.init():
        return
    window = glfw.create_window(720, 600, "PyOpengl Window", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    [mesh, shader, camera] = glInit( window )
    print( "Entering polling loop" )
    #GL.glPolygonMode( GL.GL_FRONT_AND_BACK, GL.GL_LINE )

    t0 = glfw.get_time()
    d = 0.0
    while not glfw.window_should_close(window):
        t1 = glfw.get_time()
        if t1 - t0 > dfps:
            t0 = t1
            GL.glClearColor(0.5, 0.5, 0.5, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT )

            
            camera.updateView()
            mesh.draw()
            
            d = ( d + 0.01 ) % 10
            array = model.eval( d - 5 )
            mesh.updateData( array )

            glfw.swap_buffers(window)
            glfw.poll_events()
    print( "Closing window" )
    mesh.delete()
    shader.delete()
    
    glfw.terminate()

if __name__ == "__main__":
    main()    