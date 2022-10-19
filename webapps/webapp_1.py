from js import window, document, console
from js import THREE, Math
from pyodide import create_proxy, to_js


def main():
    global objects
    objects = []

    global camera
    camera = THREE.PerspectiveCamera.new( 45, window.innerWidth / window.innerHeight, 1, 10000 )
    camera.position.set( 500, 800, 1300 )
    camera.lookAt( 0, 0, 0 )

    global scene
    scene = THREE.Scene.new()
    scene.background = THREE.Color.new( 0xf0f0f0 )

    #roll-over helpers
    rollOverGeo = THREE.BoxGeometry.new( 50, 50, 50 )
    rollOverMaterial = THREE.MeshBasicMaterial.new()
    rollOverMaterial.color = THREE.Color.new( 0xff0000 )
    rollOverMaterial.opacity = 0.5
    rollOverMaterial.transparent = True

    global rollOverMesh
    rollOverMesh = THREE.Mesh.new( rollOverGeo, rollOverMaterial )
    scene.add( rollOverMesh )

    #cubes
    global cubeGeo, cubeMaterial
    cubeGeo = THREE.BoxGeometry.new( 50, 50, 50 )
    cubeMaterial = THREE.MeshNormalMaterial.new()
    #cubeMaterial.color = THREE.Color.new( 0xfeb74c )

	#grid
    gridHelper = THREE.GridHelper.new( 1000, 20 )
    scene.add( gridHelper )

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

    objects.append( plane)


    #lights
    ambientLight = THREE.AmbientLight.new( 0x606060 )
    scene.add( ambientLight )

    directionalLight = THREE.DirectionalLight.new( 0xffffff )
    directionalLight.position.set( 1, 0.75, 0.5 ).normalize()
    scene.add( directionalLight )

    global renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize( window.innerWidth, window.innerHeight )
    document.body.appendChild(renderer.domElement )

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
    

    render()


def render(*args):
    global composer1, composer2
    window.requestAnimationFrame(create_proxy(render))
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

    global raycaster, pointer, objects

    pointer.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( pointer, camera )

    js_objects = to_js(objects)
    intersects = raycaster.intersectObjects( js_objects, True )

    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        
        rollOverMesh.position.copy( intersect.point ).add( intersect.face.normal )
        rollOverMesh.position.divideScalar( 50 ).floor().multiplyScalar( 50 ).addScalar( 25 )

def on_dbl_click(event):
    event.preventDefault()

    global raycaster, pointer, objects, cubeGeo, cubeMaterial

    pointer.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( pointer, camera )

    js_objects = to_js(objects)
    intersects = raycaster.intersectObjects( js_objects, True )

    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        voxel = THREE.Mesh.new( cubeGeo, cubeMaterial )
        voxel.position.copy( intersect.point ).add( intersect.face.normal )
        voxel.position.divideScalar( 50 ).floor().multiplyScalar( 50 ).addScalar( 25 )

        scene.add(voxel)

        objects.append(voxel)




if __name__ == '__main__':
        main()
