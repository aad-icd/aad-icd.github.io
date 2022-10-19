from js import window, document, console
from js import THREE, Math
from pyodide import create_proxy, to_js


def main():
    global objects, control_points, transform_control, action_select
    objects = []
    control_points = []

    global camera
    camera = THREE.PerspectiveCamera.new( 45, window.innerWidth / window.innerHeight, 1, 10000 )
    camera.position.set( 500, 800, 1300 )
    camera.lookAt( 0, 0, 0 )

    global scene
    scene = THREE.Scene.new()
    scene.background = THREE.Color.new( "rgb(40,40,40)" )

    #roll-over helpers
    roll_over_geom = THREE.CircleGeometry.new( 10, 20 )
    roll_over_material = THREE.MeshBasicMaterial.new()
    roll_over_material.color = THREE.Color.new(0,255,0)
    roll_over_material.opacity = 0.5
    roll_over_material.transparent = True
    
    global roll_over_mesh
    roll_over_mesh = THREE.Mesh.new( roll_over_geom, roll_over_material )
    roll_over_mesh.rotation.x = Math.PI * -0.5
    scene.add( roll_over_mesh )

    #spheres
    global sphere_geom, sphere_material
    sphere_geom = THREE.SphereGeometry.new( 10, 20, 20 )
    sphere_material = THREE.MeshBasicMaterial.new()
    sphere_material.color = THREE.Color.new( "rgb(255,255,255" )

	#grid
    grid_helper = THREE.GridHelper.new( 1000, 20 )
    grid_helper.position.y = -1
    scene.add( grid_helper )

    #raycaster
    global raycaster
    raycaster = THREE.Raycaster.new()
    global pointer
    pointer = THREE.Vector2.new()

    geometry = THREE.PlaneGeometry.new( 1000, 1000 )
    geometry.rotateX( - Math.PI / 2 )

    global plane
    plane = THREE.Mesh.new( geometry, THREE.MeshBasicMaterial.new())
    plane.visible = False
    scene.add( plane )

    #lights
    ambientLight = THREE.AmbientLight.new( 0x606060 )
    scene.add( ambientLight )

    directionalLight = THREE.DirectionalLight.new( 0xffffff )
    directionalLight.position.set( 1, 0.75, 0.5 ).normalize()
    scene.add( directionalLight )

    #renderer
    global renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize( window.innerWidth, window.innerHeight )
    document.body.appendChild(renderer.domElement )

    #transform_control
    transform_control = THREE.TransformControls.new(camera, renderer.domElement)
    transform_drag_proxy = create_proxy(transform_drag)
    transform_control.addEventListener('dragging-changed', transform_drag_proxy)
    
    #post processing
    global render_pass, fxaa_pass
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )

    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)
    

    #orbit controls
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    controls.update()
    
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy)

    pointer_move_proxy = create_proxy(on_pointer_move)
    document.addEventListener('pointermove', pointer_move_proxy)

    dbl_click_proxy = create_proxy(on_dbl_click)
    document.addEventListener('dblclick', dbl_click_proxy)
    
    #initiate empty curve
    global curve_object
    curve_object = None

    global extruded_curves
    extruded_curves = []

    render()


def transform_drag(event):
    event.preventDefault()

    if not event.value:
        update_curve()
        extrude_curve()
    

def update_curve():
    #curve
    #initiate the first segment
    global _range, curve_object
    _range = len(control_points)

    if _range == 2 and curve_object == None:
        js_control_points = to_js(control_points)
        geometry = THREE.BufferGeometry.new()
        geometry.setFromPoints( js_control_points )

        curve_material = THREE.LineBasicMaterial.new()
        curve_material.color = THREE.Color.new("rgb(255,255,255")

        curve_object = THREE.LineLoop.new( geometry, curve_material )
        scene.add(curve_object)

    elif _range>2:
        scene.remove(curve_object)

        js_control_points = to_js(control_points)
        geometry = THREE.BufferGeometry.new()
        geometry.setFromPoints( js_control_points )

        curve_material = THREE.LineBasicMaterial.new()
        curve_material.color = THREE.Color.new("rgb(255,255,255")

        curve_object = THREE.LineLoop.new( geometry, curve_material )

        scene.add(curve_object)
    
    global extruded_curves
    if len(extruded_curves) == 100:
        for curve in extruded_curves:
                scene.remove(curve)
                extruded_curves = []

def extrude_curve():
    global extruded_curves, curve_object
    if curve_object != None:
        if len(extruded_curves) < 100:
            pass
            for i in range(100):
                extrude_curve_mat = THREE.LineBasicMaterial.new()

                extrude_curve_mat.color = THREE.Color.new(0.5, 0.5, (i+1)/100)



                extrude_curve = THREE.LineLoop.new()
                extrude_curve.geometry.copy(curve_object.geometry)
                extrude_curve.position.y = (i+1)*20

                extrude_curve.material = extrude_curve_mat
            
                extruded_curves.append(extrude_curve)
                scene.add(extrude_curve)   
        
def render(*args):
    window.requestAnimationFrame(create_proxy(render))

    global composer
    composer.render()

def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing
    global render_pass, fxaa_pass
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )

    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)
    

def on_pointer_move(event):

    event.preventDefault()

    global raycaster, pointer, objects, roll_over_mesh

    pointer.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( pointer, camera )

    intersects = raycaster.intersectObjects( plane, True )

    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        
        roll_over_mesh.position.copy( intersect.point ).add( intersect.face.normal )

def on_drag (event):
    pass     

def on_dbl_click(event):
    event.preventDefault()

    global raycaster, pointer, objects, sphere_geom, sphere_material, control_points

    pointer.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( pointer, camera )

    intersects = raycaster.intersectObject( plane, True )

    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        point = THREE.Mesh.new( sphere_geom, sphere_material )
        point.rotation.x = Math.PI * -0.5
        point.position.copy( intersect.point ).add( intersect.face.normal )

        control_points.append(point.position)
        scene.add(point)

        objects.append(point)

    update_curve()
    extrude_curve()


if __name__ == '__main__':
        main()
