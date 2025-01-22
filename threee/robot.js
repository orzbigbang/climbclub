import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

// 创建场景、相机和渲染器
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

// 创建轨道控制器
const controls = new OrbitControls(camera, renderer.domElement);
camera.position.z = 15;

// 创建机器人
function createRobot() {
    const robot = new THREE.Group();

    // 头部 - 立方体
    const headGeometry = new THREE.BoxGeometry(2, 2, 2);
    const headMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.y = 4;
    robot.add(head);

    // 眼睛 - 球体
    const eyeGeometry = new THREE.SphereGeometry(0.3, 32, 32);
    const eyeMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
    
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.5, 4.5, 1);
    
    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.5, 4.5, 1);
    
    robot.add(leftEye);
    robot.add(rightEye);

    // 身体 - 圆柱体
    const bodyGeometry = new THREE.CylinderGeometry(1.5, 1.5, 4, 32);
    const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0x0000ff });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.y = 1;
    robot.add(body);

    // 手臂 - 圆柱体
    const armGeometry = new THREE.CylinderGeometry(0.3, 0.3, 3, 32);
    const armMaterial = new THREE.MeshPhongMaterial({ color: 0xff00ff });
    
    const leftArm = new THREE.Mesh(armGeometry, armMaterial);
    leftArm.position.set(-2, 2, 0);
    leftArm.rotation.z = Math.PI / 2;
    
    const rightArm = new THREE.Mesh(armGeometry, armMaterial);
    rightArm.position.set(2, 2, 0);
    rightArm.rotation.z = -Math.PI / 2;
    
    robot.add(leftArm);
    robot.add(rightArm);

    // 腿 - 圆柱体
    const legGeometry = new THREE.CylinderGeometry(0.4, 0.4, 3, 32);
    const legMaterial = new THREE.MeshPhongMaterial({ color: 0xffff00 });
    
    const leftLeg = new THREE.Mesh(legGeometry, legMaterial);
    leftLeg.position.set(-0.8, -1, 0);
    
    const rightLeg = new THREE.Mesh(legGeometry, legMaterial);
    rightLeg.position.set(0.8, -1, 0);
    
    robot.add(leftLeg);
    robot.add(rightLeg);

    return robot;
}

// 添加光源
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
directionalLight.castShadow = true;
scene.add(directionalLight);

// 创建并添加机器人到场景
const robot = createRobot();
scene.add(robot);

// 动画循环
function animate() {
    requestAnimationFrame(animate);
    
    // 让机器人旋转
    robot.rotation.y += 0.01;
    
    renderer.render(scene, camera);
}

// 处理窗口大小变化
window.addEventListener('resize', onWindowResize, false);

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

animate(); 