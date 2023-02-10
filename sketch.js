
// Three JS Template
//----------------------------------------------------------------- BASIC parameters
var renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize( window.innerWidth, window.innerHeight );

if (window.innerWidth > 800) {
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.needsUpdate = true;
  renderer.toneMapping = THREE.ReinhardToneMapping;
};
//---

document.body.appendChild( renderer.domElement );

window.addEventListener('resize', onWindowResize, false);
function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize( window.innerWidth, window.innerHeight );
};

var camera = new THREE.PerspectiveCamera( 20, window.innerWidth / window.innerHeight, 1, 500 );
camera.lookAt(0,0,0)

camera.position.set(5, 10, 10);

var scene = new THREE.Scene();
var city = new THREE.Object3D();
var smoke = new THREE.Object3D();
var panels = []

var createCarPos = true;
var uSpeed = 0.00025;

//----------------------------------------------------------------- FOG background

var setcolor = 0xFFFFFF;

scene.background = new THREE.Color(setcolor);
scene.fog = new THREE.Fog(setcolor, 10, 20);
//scene.fog = new THREE.FogExp2(setcolor, 0.05);
//---------------------------------------------------------------- RANDOM Function
function mathRandom(num = 8) {
  var numValue = - Math.random() * num + Math.random() * num;
  return numValue;
};
//----------------------------------------------------------------- CHANGE bluilding colors
var setTintNum = true;
function setTintColor() {
  if (setTintNum) {
    setTintNum = false;
    var setColor = 0xC19A6B;
  } else {
    setTintNum = true;
    var setColor = 0xC19A6B;
  };
  return setColor;
};

//----------------------------------------------------------------- CREATE City

function init3(){

  var radius = 10;
  var width = 2 * radius * 0.86603;
  var hwidth = width/2;
  var HEXAGRID_MESH= new THREE.Object3D()
  var HEXAGRID_WIRE= new THREE.Object3D()
  var HEXAGRID_SHAPES = []

  var hexMaterial = new THREE.MeshStandardMaterial({
    wireframe:false,
    //opacity:0.9,
    //transparent:true,
    roughness: 0.3,
    //metalness: 1,
    shading: THREE.SmoothShading,
    //shading:THREE.FlatShading,
  })
  
  var scale = 0.05

  for (var r = -radius; r <= radius; r++) {
    for (var q = -radius; q <= radius; q++) {

      var x = (q*width);
              // This comes from a simplified version of:
              // stage.height()/2 + (tile.radius*Math.sin(30*Math.PI/180)+tile.radius)*r+2*tile.radius;
              var y = (1.5*r)*radius;
              var offset = 0;
              if (r % 2 !== 0) {
                // positive or negative
                offset = (r?r<0?-1:1:0)*(Math.abs(r) - 1)*hwidth + r%2*hwidth; 
              } else {
                offset = r*hwidth;
              }
              x += offset;
              
              var radius = radius;
              var z = 0
              
              var center = new THREE.Vector3((x+0)*scale, (y+radius)*scale, z*scale);

              var panel = new THREE.Object3D()

              var random_f = Math.random()/10
              console.log(random_f)

              hexMaterial.color = new THREE.Color(193/255, 154/255, 107/255)
              const geometry = new THREE.CylinderGeometry( radius*scale, radius*scale, 0.1+random_f, 6 );
              const cylinder = new THREE.Mesh( geometry, hexMaterial );
              panel.add( cylinder );


              

              const edges = new THREE.EdgesGeometry( geometry );
              const line = new THREE.LineSegments( edges, new THREE.LineBasicMaterial( { color: 0x808080 } ) );
              //panel.add( line );

              city.add(panel)

              panels.push(panel)

              panel.position.set(center.x, center.z, center.y)


                     
    }
  }
}
//-----------------------------------------------------------------

//----------------------------------------------------------------- MOUSE function
var raycaster = new THREE.Raycaster();;
var mouse = new THREE.Vector2(), INTERSECTED;
var intersected;
var mouseIn = false

function onMouseMove(event) {
  event.preventDefault();
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera( mouse, camera );

	// calculate objects intersecting the picking ray
	const intersects = raycaster.intersectObjects( panels );

    console.log(intersects)

	for ( let i = 0; i < intersects.length; i ++ ) {

        var intersected = intersects[ i ]

        intersected.object.translateY(0.1)

        

	}

    renderer.render( scene, camera );
};

function onMouseLeave(event) {
  event.preventDefault();
   
};

function onMouseLeave(event) {
  event.preventDefault();

  mouseIn = false;
   
};

function onMouseEnter(event) {
  event.preventDefault();

  mouseIn = true;
   
};

function onDocumentTouchStart( event ) {
  if ( event.touches.length == 1 ) {
    event.preventDefault();
    mouse.x = event.touches[ 0 ].pageX -  window.innerWidth / 2;
    mouse.y = event.touches[ 0 ].pageY - window.innerHeight / 2;
  };
};
function onDocumentTouchMove( event ) {
  if ( event.touches.length == 1 ) {
    event.preventDefault();
    mouse.x = event.touches[ 0 ].pageX -  window.innerWidth / 2;
    mouse.y = event.touches[ 0 ].pageY - window.innerHeight / 2;
  }
}
window.addEventListener('mousemove', onMouseMove, false);
window.addEventListener('mouseleave', onMouseLeave, false)
window.addEventListener('mouseenter', onMouseEnter, false)
window.addEventListener('touchstart', onDocumentTouchStart, false );
window.addEventListener('touchmove', onDocumentTouchMove, false );

//----------------------------------------------------------------- Lights
var ambientLight = new THREE.AmbientLight(0xFFFFFF, 4);
var lightFront = new THREE.SpotLight(0xFFFFFF, 20, 10);
var lightBack = new THREE.PointLight(0xFFFFFF, 0.5);

var spotLightHelper = new THREE.SpotLightHelper( lightFront );
//scene.add( spotLightHelper );

lightFront.rotation.x = 45 * Math.PI / 180;
lightFront.rotation.z = -45 * Math.PI / 180;
lightFront.position.set(5, 5, 5);
lightFront.castShadow = true;
lightFront.shadow.mapSize.width = 6000;
lightFront.shadow.mapSize.height = lightFront.shadow.mapSize.width;
lightFront.penumbra = 0.1;
lightBack.position.set(0,6,0);

smoke.position.y = 2;


scene.add(ambientLight);
city.add(lightFront);
scene.add(lightBack);
scene.add(city);
city.add(smoke);

//----------------------------------------------------------------- GRID Helper
var gridHelper = new THREE.GridHelper( 60, 120, 0xFF0000, 0x000000);
//city.add( gridHelper );

var createCars = function(cScale = 2, cPos = 20, cColor = 0xFFFFFF) {
  var cMat = new THREE.MeshToonMaterial({color:cColor, side:THREE.DoubleSide});
  var cGeo = new THREE.BoxGeometry(1, cScale/40, cScale/40);
  var cElem = new THREE.Mesh(cGeo, cMat);
  var cAmp = 3;
  
  if (createCarPos) {
    createCarPos = false;
    cElem.position.x = -cPos;
    cElem.position.z = (mathRandom(cAmp));

    TweenMax.to(cElem.position, 3, {x:cPos, repeat:-1, yoyo:true, delay:mathRandom(3)});
  } else {
    createCarPos = true;
    cElem.position.x = (mathRandom(cAmp));
    cElem.position.z = -cPos;
    cElem.rotation.y = 90 * Math.PI / 180;
  
    TweenMax.to(cElem.position, 5, {z:cPos, repeat:-1, yoyo:true, delay:mathRandom(3), ease:Power1.easeInOut});
  };
  cElem.receiveShadow = true;
  cElem.castShadow = true;
  cElem.position.y = Math.abs(mathRandom(5));
  city.add(cElem);
};

var generateLines = function() {
  for (var i = 0; i<60; i++) {
    //createCars(0.1, 20);
  };
};

//----------------------------------------------------------------- CAMERA position

var cameraSet = function() {
  createCars(0.1, 20, 0xFFFFFF);
  TweenMax.to(camera.position, 1, {y:1+Math.random()*4, ease:Expo.easeInOut})
};

//----------------------------------------------------------------- ANIMATE

var animate = function() {
  var time = Date.now() * 0.00005;
  requestAnimationFrame(animate);

  //console.log(mouse.x)
  
  city.rotation.y -= ((mouse.x * 2) - camera.rotation.y) * uSpeed;
  city.rotation.x -= (-(mouse.y * 2) - camera.rotation.x) * uSpeed;
  if (city.rotation.x < -0.05) city.rotation.x = -0.05;
  else if (city.rotation.x>1) city.rotation.x = 1;

  
  smoke.rotation.y += 0.01;
  smoke.rotation.x += 0.01;
  
  camera.lookAt(city.position);
  renderer.render( scene, camera );  

  
}

//----------------------------------------------------------------- START functions
generateLines();
init3();
animate();