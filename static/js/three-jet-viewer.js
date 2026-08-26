/**
 * NovaJet Private - Interactive 3D Jet Avionics & Radar Showcase
 * Powered by Three.js (WebGL)
 */

document.addEventListener('DOMContentLoaded', () => {
  initThreeJetViewer();
});

function initThreeJetViewer() {
  const container = document.getElementById('threeJetViewerContainer');
  if (!container || typeof THREE === 'undefined') return;

  // 1. Scene, Camera, Renderer
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.set(0, 15, 38);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // 2. Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);

  const dirLight1 = new THREE.DirectionalLight(0x60a5fa, 1.8);
  dirLight1.position.set(20, 40, 20);
  scene.add(dirLight1);

  const dirLight2 = new THREE.DirectionalLight(0xffffff, 1.0);
  dirLight2.position.set(-20, -20, -20);
  scene.add(dirLight2);

  // 3. Build 3D Flagship Jet Group
  const jetGroup = new THREE.Group();

  // Materials
  const fuselageMat = new THREE.MeshStandardMaterial({
    color: 0x0f1f38,
    metalness: 0.85,
    roughness: 0.25,
  });

  const chromeMat = new THREE.MeshStandardMaterial({
    color: 0xe2e8f0,
    metalness: 0.95,
    roughness: 0.1,
  });

  const blueGlowMat = new THREE.MeshBasicMaterial({
    color: 0x3b82f6,
    wireframe: true,
  });

  const glassMat = new THREE.MeshStandardMaterial({
    color: 0x06b6d4,
    metalness: 0.9,
    roughness: 0.1,
    transparent: true,
    opacity: 0.65,
  });

  // A. Fuselage (Streamlined body)
  const fuselageGeo = new THREE.CylinderGeometry(1.6, 1.1, 24, 32);
  const fuselage = new THREE.Mesh(fuselageGeo, fuselageMat);
  fuselage.rotation.x = Math.PI / 2;
  jetGroup.add(fuselage);

  // B. Nose Cone
  const noseGeo = new THREE.ConeGeometry(1.6, 7, 32);
  const nose = new THREE.Mesh(noseGeo, chromeMat);
  nose.rotation.x = -Math.PI / 2;
  nose.position.z = 15.5;
  jetGroup.add(nose);

  // Cockpit Windshield
  const cockpitGeo = new THREE.SphereGeometry(1.4, 16, 16, 0, Math.PI, 0, Math.PI / 2);
  const cockpit = new THREE.Mesh(cockpitGeo, glassMat);
  cockpit.position.set(0, 0.8, 10.5);
  cockpit.rotation.x = -Math.PI / 4;
  jetGroup.add(cockpit);

  // C. Swept Main Wings
  const wingShape = new THREE.Shape();
  wingShape.moveTo(0, 0);
  wingShape.lineTo(16, -6);
  wingShape.lineTo(15.5, -7.5);
  wingShape.lineTo(0, -3.5);
  wingShape.closePath();

  const extrudeSettings = { depth: 0.35, bevelEnabled: true, bevelSegments: 2, steps: 1, bevelSize: 0.1, bevelThickness: 0.1 };
  const wingGeo = new THREE.ExtrudeGeometry(wingShape, extrudeSettings);

  // Right Wing
  const rightWing = new THREE.Mesh(wingGeo, fuselageMat);
  rightWing.rotation.x = Math.PI / 2;
  rightWing.position.set(1.2, 0, 4);
  jetGroup.add(rightWing);

  // Left Wing
  const leftWing = new THREE.Mesh(wingGeo, fuselageMat);
  leftWing.rotation.x = Math.PI / 2;
  leftWing.scale.x = -1;
  leftWing.position.set(-1.2, 0, 4);
  jetGroup.add(leftWing);

  // Winglets
  const wingletGeo = new THREE.BoxGeometry(0.2, 1.8, 1.2);
  const rightWinglet = new THREE.Mesh(wingletGeo, chromeMat);
  rightWinglet.position.set(17.2, 0.8, -2.5);
  jetGroup.add(rightWinglet);

  const leftWinglet = new THREE.Mesh(wingletGeo, chromeMat);
  leftWinglet.position.set(-17.2, 0.8, -2.5);
  jetGroup.add(leftWinglet);

  // D. Turbofan Engines (Mounted Aft)
  const engineGeo = new THREE.CylinderGeometry(0.9, 0.8, 5.5, 24);
  const engineMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.9, roughness: 0.2 });

  const rightEngine = new THREE.Mesh(engineGeo, engineMat);
  rightEngine.rotation.x = Math.PI / 2;
  rightEngine.position.set(2.4, 0.6, -7);
  jetGroup.add(rightEngine);

  const leftEngine = new THREE.Mesh(engineGeo, engineMat);
  leftEngine.rotation.x = Math.PI / 2;
  leftEngine.position.set(-2.4, 0.6, -7);
  jetGroup.add(leftEngine);

  // Engine exhaust glows
  const exhaustGeo = new THREE.RingGeometry(0.2, 0.7, 16);
  const exhaustMat = new THREE.MeshBasicMaterial({ color: 0x60a5fa, side: THREE.DoubleSide });
  const rightExhaust = new THREE.Mesh(exhaustGeo, exhaustMat);
  rightExhaust.position.set(2.4, 0.6, -9.8);
  jetGroup.add(rightExhaust);

  const leftExhaust = new THREE.Mesh(exhaustGeo, exhaustMat);
  leftExhaust.position.set(-2.4, 0.6, -9.8);
  jetGroup.add(leftExhaust);

  // E. T-Tail Vertical & Horizontal Stabilizers
  const tailFinGeo = new THREE.BoxGeometry(0.3, 5.5, 4.5);
  const tailFin = new THREE.Mesh(tailFinGeo, fuselageMat);
  tailFin.position.set(0, 3.2, -10);
  tailFin.rotation.x = -Math.PI / 8;
  jetGroup.add(tailFin);

  const horizTailGeo = new THREE.BoxGeometry(9, 0.25, 2.5);
  const horizTail = new THREE.Mesh(horizTailGeo, chromeMat);
  horizTail.position.set(0, 5.8, -11.5);
  jetGroup.add(horizTail);

  // 4. Rotating Radar Avionics Rings
  const ring1Geo = new THREE.TorusGeometry(20, 0.08, 16, 100);
  const ring1 = new THREE.Mesh(ring1Geo, blueGlowMat);
  ring1.rotation.x = Math.PI / 2;
  scene.add(ring1);

  const ring2Geo = new THREE.TorusGeometry(24, 0.05, 16, 100);
  const ring2 = new THREE.Mesh(ring2Geo, new THREE.MeshBasicMaterial({ color: 0x06b6d4, wireframe: true, transparent: true, opacity: 0.4 }));
  ring2.rotation.x = Math.PI / 2.3;
  scene.add(ring2);

  // Coordinate Radar Grid
  const gridHelper = new THREE.GridHelper(50, 20, 0x3b82f6, 0x1e293b);
  gridHelper.position.y = -8;
  scene.add(gridHelper);

  scene.add(jetGroup);

  // 5. Mouse Interaction for 3D Pitch/Yaw
  let targetRotationY = 0;
  let targetRotationX = 0;
  let mouseX = 0;
  let mouseY = 0;

  container.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    mouseX = ((e.clientX - rect.left) / container.clientWidth) * 2 - 1;
    mouseY = -((e.clientY - rect.top) / container.clientHeight) * 2 + 1;

    targetRotationY = mouseX * 0.8;
    targetRotationX = mouseY * 0.4;
  });

  // Touch Support
  container.addEventListener('touchmove', (e) => {
    if (e.touches.length > 0) {
      const rect = container.getBoundingClientRect();
      mouseX = ((e.touches[0].clientX - rect.left) / container.clientWidth) * 2 - 1;
      mouseY = -((e.touches[0].clientY - rect.top) / container.clientHeight) * 2 + 1;
      targetRotationY = mouseX * 0.8;
      targetRotationX = mouseY * 0.4;
    }
  });

  // 6. Animation Loop
  let clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    // Idle gentle flight oscillation
    jetGroup.position.y = Math.sin(elapsedTime * 1.5) * 0.6;
    jetGroup.rotation.z = Math.sin(elapsedTime * 1.2) * 0.05;

    // Smooth lerp to mouse orientation
    jetGroup.rotation.y += (targetRotationY + elapsedTime * 0.15 - jetGroup.rotation.y) * 0.05;
    jetGroup.rotation.x += (targetRotationX - jetGroup.rotation.x) * 0.05;

    // Rotate Radar Rings
    ring1.rotation.z = elapsedTime * 0.2;
    ring2.rotation.z = -elapsedTime * 0.15;

    renderer.render(scene, camera);
  }

  animate();

  // Resize Handler
  window.addEventListener('resize', () => {
    if (!container) return;
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
}
