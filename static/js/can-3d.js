import * as THREE from 'three';
import {
    GLTFLoader
} from 'three/addons/loaders/GLTFLoader.js';
import {
    MeshoptDecoder
} from 'three/addons/libs/meshopt_decoder.module.js';
import {
    RoomEnvironment
} from 'three/addons/environments/RoomEnvironment.js';

const container = document.getElementById('can-viewer');

if (container) {
    const modelUrl = container.dataset.modelUrl;

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(35, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 0, 5);

    const renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.5;
    container.appendChild(renderer.domElement);

    // Soft studio-style reflections so PBR materials don't render flat/black —
    // without this, metal surfaces have nothing to reflect and look dark.
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;

    scene.add(new THREE.AmbientLight(0xffffff, -1.5));

    let can = null;
    // Spins the can back and forth on its own Y axis, like a gentle "look left, look right".
    // Independent left/right bounds (in degrees) since the tilt makes the swing look
    // asymmetric visually even though a symmetric sine amplitude would be mathematically even.
    const swingSpeed = 0.30;
    const swingLeftDeg = -45;
    const swingRightDeg = 30;

    // Starts at -15deg (validated look), swinging toward swingLeftDeg first, then swingRightDeg.
    const swingStartPhase = 3.343;

    // Fixed tilt lives on this parent group so the can spins on its own axis
    // instead of the tilt/spin angles being recomposed together every frame (which wobbles).
    const tiltGroup = new THREE.Group();
    tiltGroup.rotation.z = THREE.MathUtils.degToRad(-30);
    tiltGroup.rotation.x = THREE.MathUtils.degToRad(12);
    scene.add(tiltGroup);

    const loader = new GLTFLoader();
    // The model ships meshopt-compressed to keep it small (~1 MB vs ~10 MB).
    loader.setMeshoptDecoder(MeshoptDecoder);
    loader.load(
        modelUrl,
        /**
         * Tones down the loaded model's metalness/roughness so it doesn't
         * look like a mirror, then centers and scales it inside the tilt group.
         * @param {Object} gltf - The loaded glTF asset.
         */
        (gltf) => {
            can = gltf.scene;

            can.traverse((child) => {
                if (child.isMesh && child.material) {
                    const materials = Array.isArray(child.material) ? child.material : [child.material];
                    materials.forEach((material) => {
                        if ('metalness' in material) {
                            material.metalness = Math.min(material.metalness, 0.3);
                            material.roughness = Math.max(material.roughness, 0.5);
                        }
                    });
                }
            });

            const box = new THREE.Box3().setFromObject(can);
            const size = box.getSize(new THREE.Vector3());
            const center = box.getCenter(new THREE.Vector3());

            can.position.sub(center);
            const maxDimension = Math.max(size.x, size.y, size.z);
            const scale = 2.2 / maxDimension;
            can.scale.setScalar(scale);

            tiltGroup.add(can);

            // Re-center after tilting: a tilted bounding box isn't symmetric around
            // the origin anymore, so without this the can visually drifts off-center.
            tiltGroup.updateMatrixWorld(true);
            const tiltedCenter = new THREE.Box3().setFromObject(tiltGroup).getCenter(new THREE.Vector3());
            tiltGroup.position.sub(tiltedCenter);
        },
        undefined,
        (error) => console.error('Failed to load can model:', error)
    );

    const clock = new THREE.Clock();

    /**
     * Renders one frame and schedules the next: swings the loaded can back
     * and forth on its Y axis, then draws the scene.
     */
    function animate() {
        requestAnimationFrame(animate);

        if (can) {
            const t = (Math.sin(clock.getElapsedTime() * swingSpeed + swingStartPhase) + 1) / 2;
            can.rotation.y = THREE.MathUtils.degToRad(THREE.MathUtils.lerp(swingLeftDeg, swingRightDeg, t));
        }

        renderer.render(scene, camera);
    }
    animate();

    /**
     * Resizes the renderer and updates the camera aspect ratio to match the
     * viewer container's current dimensions.
     */
    function handleResize() {
        const width = container.clientWidth;
        const height = container.clientHeight;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    }
    window.addEventListener('resize', handleResize);
}