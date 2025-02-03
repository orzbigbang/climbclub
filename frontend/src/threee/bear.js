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

// 首先添加纹理加载器
const textureLoader = new THREE.TextureLoader();

// 创建熊的模型
function createBear() {
    const bear = new THREE.Group();

    // 创建基础材质属性
    const furTexture = textureLoader.load('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='); // 使用1x1像素的base64图片作为临时纹理
    const furNormal = furTexture.clone(); // 复用相同的纹理作为法线贴图
    
    // 创建熊的基础材质
    const bearMaterial = new THREE.MeshStandardMaterial({ 
        color: 0x8B4513,
        roughness: 0.8,         // 增加粗糙度
        metalness: 0.1,         // 降低金属感
        map: furTexture,        // 添加毛发纹理
        normalMap: furNormal,   // 添加法线贴图
        normalScale: new THREE.Vector2(0.5, 0.5),
        bumpMap: furTexture,    // 添加凹凸贴图
        bumpScale: 0.05,        // 控制凹凸程度
    });

    // 调整纹理重复和旋转
    furTexture.wrapS = furTexture.wrapT = THREE.RepeatWrapping;
    furTexture.repeat.set(2, 2);
    furTexture.rotation = Math.PI / 4;
    
    // 身体
    const bodyGeometry = new THREE.SphereGeometry(2.5, 64, 64); // 增加细分度
    const body = new THREE.Mesh(bodyGeometry, bearMaterial);
    body.position.y = 1.5;
    body.scale.y = 1.2;
    bear.add(body);

    // 头部 - 使用相同的材质但调整纹理缩放
    const headGeometry = new THREE.SphereGeometry(2.2, 64, 64);
    const headMaterial = bearMaterial.clone();
    headMaterial.map.repeat.set(1.5, 1.5);
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.y = 4.2;
    bear.add(head);

    // 耳朵 - 使用更深色的材质
    const earMaterial = bearMaterial.clone();
    earMaterial.color.setHex(0x704214);
    const earGeometry = new THREE.SphereGeometry(0.7, 32, 32);
    
    const leftEar = new THREE.Mesh(earGeometry, earMaterial);
    leftEar.position.set(-1.7, 5.8, 0);
    
    const rightEar = new THREE.Mesh(earGeometry, earMaterial);
    rightEar.position.set(1.7, 5.8, 0);
    
    bear.add(leftEar);
    bear.add(rightEar);

    // 眼睛 - 添加光泽
    const eyeMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x000000,
        shininess: 100,
        specular: 0x444444
    });
    const eyeGeometry = new THREE.SphereGeometry(0.3, 32, 32);
    
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.9, 4.4, 1.7);
    
    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.9, 4.4, 1.7);
    
    bear.add(leftEye);
    bear.add(rightEye);

    // 鼻子 - 使用光滑的黑色材质
    const noseMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x000000,
        shininess: 100,
        specular: 0x222222
    });
    const noseGeometry = new THREE.SphereGeometry(0.4, 32, 32);
    const nose = new THREE.Mesh(noseGeometry, noseMaterial);
    nose.position.set(0, 4.0, 2.0);
    bear.add(nose);

    // 简化的手掌设计 - 调整大小和位置
    const handGeometry = new THREE.SphereGeometry(0.6, 32, 32);
    const handMaterial = new THREE.MeshPhongMaterial({ color: 0x8B4513 });
    
    const leftHand = new THREE.Mesh(handGeometry, handMaterial);
    leftHand.position.set(-2.8, 1.8, 0.5);
    leftHand.scale.set(1.2, 1, 0.8); // 调整形状
    
    const rightHand = new THREE.Mesh(handGeometry, handMaterial);
    rightHand.position.set(2.8, 1.8, 0.5);
    rightHand.scale.set(1.2, 1, 0.8);
    
    bear.add(leftHand);
    bear.add(rightHand);

    // 腿 - 圆柱体 - 调整位置
    const legGeometry = new THREE.CylinderGeometry(0.7, 0.9, 1.8, 32);
    const legMaterial = new THREE.MeshPhongMaterial({ color: 0x8B4513 });
    
    const leftLeg = new THREE.Mesh(legGeometry, legMaterial);
    leftLeg.position.set(-1.2, -0.3, 0);
    
    const rightLeg = new THREE.Mesh(legGeometry, legMaterial);
    rightLeg.position.set(1.2, -0.3, 0);
    
    // 脚掌 - 调整大小
    const footGeometry = new THREE.SphereGeometry(0.8, 32, 32);
    const footMaterial = new THREE.MeshPhongMaterial({ color: 0x8B4513 });
    
    const leftFoot = new THREE.Mesh(footGeometry, footMaterial);
    leftFoot.position.set(-1.2, -1.1, 0.3);
    leftFoot.scale.set(1.2, 0.5, 1.3);
    
    const rightFoot = new THREE.Mesh(footGeometry, footMaterial);
    rightFoot.position.set(1.2, -1.1, 0.3);
    rightFoot.scale.set(1.2, 0.5, 1.3);
    
    bear.add(leftLeg);
    bear.add(rightLeg);
    bear.add(leftFoot);
    bear.add(rightFoot);

    return bear;
}

// 增强光照效果
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
directionalLight.castShadow = true;

// 改进阴影质量
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 500;
directionalLight.shadow.bias = -0.0001;

scene.add(directionalLight);

// 添加第二个方向光源增强细节
const backLight = new THREE.DirectionalLight(0xffffff, 0.5);
backLight.position.set(-5, 5, -5);
scene.add(backLight);

// 创建并添加熊到场景
const bear = createBear();
scene.add(bear);

// 添加简单的动画
function animate() {
    requestAnimationFrame(animate);
    
    // 让熊轻微摇摆
    bear.rotation.y = Math.sin(Date.now() * 0.001) * 0.2;
    
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