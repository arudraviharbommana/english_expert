// frontend/main.js
// Three.js Scene + App Initialization

// ===== THREE.JS SCENE SETUP =====
const canvas = document.getElementById('bg');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x050505, 0.0012);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 2000);
camera.position.set(0, 0, 80);

// Create particle system
const particles = new THREE.BufferGeometry();
const count = 800;
const positions = new Float32Array(count * 3);

for (let i = 0; i < count; i++) {
  positions[i*3 + 0] = (Math.random() - 0.5) * 400;
  positions[i*3 + 1] = (Math.random() - 0.5) * 200;
  positions[i*3 + 2] = (Math.random() - 0.5) * 400;
}

particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const particleMaterial = new THREE.PointsMaterial({ 
  size: 1.2, 
  transparent: true, 
  opacity: 0.85,
  color: 0xffd766
});
const points = new THREE.Points(particles, particleMaterial);
scene.add(points);

// Animation loop for scene
let animationTime = 0;

function animateScene() {
  animationTime += 0.002;
  
  // Gentle camera motion
  camera.position.x = Math.sin(animationTime * 0.6) * 20;
  camera.position.y = Math.sin(animationTime * 0.3) * 6;
  camera.lookAt(0, 0, 0);
  
  renderer.render(scene, camera);
  requestAnimationFrame(animateScene);
}

animateScene();

// Handle window resize
window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

// ===== UI INITIALIZATION =====
let uiController;

document.addEventListener('DOMContentLoaded', () => {
  // Initialize UI Controller
  uiController = new UIController({
    backend: "http://localhost:8000"
  });
  
  // Add sample text on load
  uiController.setInputText("He don't knows where is the market.");
  
  console.log("✓ NLP Expert System UI loaded");
});

// ===== PARTICLE ANIMATION ON ANALYSIS =====
function flashParticles() {
  let start = performance.now();
  const duration = 600;
  
  function step(now) {
    let progress = Math.min(1, (now - start) / duration);
    particleMaterial.opacity = 0.85 + Math.sin(progress * Math.PI) * 0.5;
    
    if (progress < 1) {
      requestAnimationFrame(step);
    } else {
      particleMaterial.opacity = 0.85;
    }
  }
  
  requestAnimationFrame(step);
}

// Hook into UI controller to flash particles after analysis
const originalAnalyze = UIController.prototype.analyze;
UIController.prototype.analyze = async function() {
  await originalAnalyze.call(this);
  flashParticles();
};

// ===== UTILITY: AUTO-ANALYZE ON DEMO MODE =====
function analyzeDemo(sentence) {
  if (uiController) {
    uiController.setInputText(sentence);
    uiController.analyze();
  }
}
