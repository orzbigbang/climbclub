<script setup>
import { onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { useShowStore } from '@/stores/show' 

const showStore = useShowStore()

let scene, camera, renderer, controls;
let model; // 添加模型的引用

// 初始化Three.js场景
const init = () => {
    scene = new THREE.Scene();
    const container = document.querySelector('#forest-house-container');
    const aspect = container.clientWidth / container.clientHeight;
    
    camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 2000);
    renderer = new THREE.WebGLRenderer({ 
        antialias: true,
        alpha: true  // 启用透明背景
    });

    // 使用容器的尺寸而不是窗口尺寸
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.setClearColor(0x000000, 0); // 设置透明背景
    
    // 将渲染器添加到组件的DOM元素中
    container.appendChild(renderer.domElement);

    // Create orbit controls
    controls = new OrbitControls(camera, renderer.domElement);
    camera.position.set(15, 10, 15);
    controls.target.set(0, 5, 0);
    
    // 禁用缩放
    controls.enableZoom = false;
    
    // 可选：如果你也想禁用其他控制
    // controls.enablePan = false;  // 禁用平移
    // controls.enableRotate = false;  // 禁用旋转
    
    controls.update();

    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
    directionalLight.position.set(10, 15, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.far = 1000;
    scene.add(directionalLight);

    // Load the forest house model
    const loader = new GLTFLoader();
    const modelPath = '/models/forest_house.glb';
    let loadStart = false
    
    loader.load(
        modelPath,
        function (gltf) {
            model = gltf.scene; // 保存模型引用
            model.traverse((node) => {
                if (node.isMesh) {
                    node.castShadow = true;
                    node.receiveShadow = true;
                }
            });
            
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            model.position.x -= center.x;
            model.position.z -= center.z;
            
            const scale = 90;
            model.scale.set(scale, scale, scale);
            
            scene.add(model);
            showStore.loading = false
        },
        function (xhr) {
            if (!loadStart) {
                loadStart = true
                showStore.loading = true
            }
            // console.log((xhr.loaded / xhr.total * 100) + '% loaded');
            
        },
        function (error) {
            // console.error('An error happened:', error);
        }
    );

    // 添加窗口调整事件监听
    window.addEventListener('resize', onWindowResize);
}

// 窗口大小调整处理函数
const onWindowResize = () => {
    const container = document.querySelector('#forest-house-container');
    const aspect = container.clientWidth / container.clientHeight;
    
    camera.aspect = aspect;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

// 动画循环
const animate = () => {
    requestAnimationFrame(animate);
    
    // 如果模型已加载，则旋转
    if (model) {
        model.rotation.y += 0.002; // 调整这个值可以改变旋转速度
    }
    
    controls.update();
    renderer.render(scene, camera);
}

// 组件挂载时初始化
onMounted(() => {
    init();
    animate();
});

// 组件卸载时清理
onBeforeUnmount(() => {
    window.removeEventListener('resize', onWindowResize);
    renderer?.dispose();
    scene?.clear();
});
</script>

<template>
  <div id="forest-house-container"></div>
</template>

<style lang='less' scoped>
#forest-house-container {
  width: 100%;
  height: 100%;
}
</style>