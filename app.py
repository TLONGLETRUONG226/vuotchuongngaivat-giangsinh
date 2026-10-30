import streamlit as st
import streamlit.components.v1 as components

# Cấu hình giao diện Streamlit rộng toàn màn hình
st.set_page_config(
    page_title="Santa's Christmas Dash 3D Ultra",
    page_icon="🎅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn header và footer mặc định của Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Mã nguồn HTML / Three.js nâng cấp giao diện siêu chân thực
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-select=none">
    <title>Santa's Christmas Dash Ultra 3D</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
        }
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #050b14;
            font-family: 'Montserrat', 'Segoe UI', Roboto, sans-serif;
        }
        #canvas-container {
            width: 100vw;
            height: 100vh;
            display: block;
        }
        
        /* UI Overlay */
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px;
            z-index: 10;
        }
        .hud-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }
        .score-box {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 12px 24px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
            font-size: 20px;
            font-weight: 800;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Screens */
        #start-screen, #gameover-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(10, 25, 47, 0.88) 0%, rgba(5, 11, 20, 0.96) 100%);
            backdrop-filter: blur(8px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            pointer-events: auto;
            color: white;
            text-align: center;
            z-index: 20;
            padding: 20px;
        }
        h1 {
            font-size: 46px;
            background: linear-gradient(135deg, #ff4d4d 0%, #f9ca24 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            text-shadow: 0 10px 20px rgba(0,0,0,0.5);
            font-weight: 900;
        }
        p {
            font-size: 16px;
            color: #cbd5e1;
            max-width: 520px;
            line-height: 1.6;
            margin-bottom: 28px;
        }
        .btn {
            background: linear-gradient(135deg, #eb4d4b, #ff7979);
            color: white;
            border: none;
            padding: 16px 48px;
            font-size: 20px;
            font-weight: 800;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(235, 77, 75, 0.5);
            transition: all 0.25s ease;
            pointer-events: auto;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .btn:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: 0 15px 30px rgba(235, 77, 75, 0.7);
        }
        
        /* Controller Buttons On-Screen */
        #controls-wrapper {
            position: absolute;
            bottom: 25px;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 30px;
            pointer-events: none;
            z-index: 15;
        }
        .d-pad, .action-pad {
            display: flex;
            gap: 15px;
            pointer-events: auto;
        }
        .ctrl-btn {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            font-size: 26px;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            transition: background 0.1s, transform 0.1s;
        }
        .ctrl-btn:active {
            background: rgba(235, 77, 75, 0.6);
            transform: scale(0.92);
        }
        .btn-jump {
            width: 80px;
            height: 80px;
            background: rgba(249, 202, 36, 0.25);
            border-color: rgba(249, 202, 36, 0.6);
            font-size: 30px;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="canvas-container"></div>

    <div id="ui-layer">
        <div class="hud-panel">
            <div class="score-box">🎁 <span id="score">0</span></div>
            <div class="score-box">⭐ <span id="distance">0</span>m</div>
        </div>
    </div>

    <!-- On-Screen Controls -->
    <div id="controls-wrapper">
        <div class="d-pad">
            <div class="ctrl-btn" id="btn-left">⬅️</div>
            <div class="ctrl-btn" id="btn-right">➡️</div>
        </div>
        <div class="action-pad">
            <div class="ctrl-btn btn-jump" id="btn-jump">🚀</div>
        </div>
    </div>

    <!-- Start Screen -->
    <div id="start-screen">
        <h1>🎅 SANTA'S DASH 3D ULTRA</h1>
        <p>Phiêu lưu qua rừng thông tuyết siêu chân thực! Thu thập hộp quà Noel và tránh các chướng ngại vật.<br><br><b>Điều khiển:</b> Nút cảm ứng trên màn hình hoặc phím <b>Mũi tên Trái / Phải</b> để chuyển làn, <b>Phím Cách (Space) / Mũi tên Lên</b> để nhảy.</p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI</button>
    </div>

    <!-- Game Over Screen -->
    <div id="gameover-screen" style="display: none;">
        <h1>💥 VẤP PHẢI CHƯỚNG NGẠI VẬT!</h1>
        <p>Xe trượt tuyết của Santa đã va chạm! Hãy thử lại để đạt kỷ lục cao hơn nhé.<br><br>🎁 Tổng số quà: <b><span id="final-score">0</span></b></p>
        <button class="btn" onclick="restartGame()">CHƠI LẠI</button>
    </div>

    <script>
        // --- 1. SETUP THREE.JS SCENE ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050b14);
        scene.fog = new THREE.FogExp2(0x050b14, 0.012);

        const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 6, 12);
        camera.lookAt(0, 1.5, -5);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        container.appendChild(renderer.domElement);

        // --- 2. LIGHTING & ATMOSPHERE ---
        const ambientLight = new THREE.AmbientLight(0xdff9fb, 0.4);
        scene.add(ambientLight);

        const moonLight = new THREE.DirectionalLight(0x74b9ff, 1.2);
        moonLight.position.set(-20, 40, 20);
        moonLight.castShadow = true;
        moonLight.shadow.mapSize.width = 2048;
        moonLight.shadow.mapSize.height = 2048;
        moonLight.shadow.camera.near = 0.5;
        moonLight.shadow.camera.far = 150;
        moonLight.shadow.camera.left = -25;
        moonLight.shadow.camera.right = 25;
        moonLight.shadow.camera.top = 25;
        moonLight.shadow.camera.bottom = -25;
        scene.add(moonLight);

        // Warm Warm Warm Warm Accent Lights
        const santaLight = new THREE.PointLight(0xff7675, 1.5, 10);
        scene.add(santaLight);

        // --- 3. MATERIALS ---
        const snowMat = new THREE.MeshStandardMaterial({ color: 0xf1f2f6, roughness: 0.3, metalness: 0.1 });
        const iceTrackMat = new THREE.MeshStandardMaterial({ color: 0xdff9fb, roughness: 0.1, metalness: 0.2 });
        const woodMat = new THREE.MeshStandardMaterial({ color: 0x546de5, roughness: 0.8 });
        const leafMat = new THREE.MeshStandardMaterial({ color: 0x079992, roughness: 0.5 });
        const giftMat = new THREE.MeshStandardMaterial({ color: 0xe15f41, roughness: 0.2, metalness: 0.3 });
        const goldMat = new THREE.MeshStandardMaterial({ color: 0xf7b731, roughness: 0.2, metalness: 0.8 });

        // --- 4. ENVIRONMENT BUILDER ---
        // Ice Track
        const trackGeo = new THREE.PlaneGeometry(12, 300);
        const track = new THREE.Mesh(trackGeo, iceTrackMat);
        track.rotation.x = -Math.PI / 2;
        track.position.z = -100;
        track.receiveShadow = true;
        scene.add(track);

        // Side Snowbanks
        const bankLeft = new THREE.Mesh(new THREE.BoxGeometry(30, 2, 300), snowMat);
        bankLeft.position.set(-21, 0, -100);
        bankLeft.receiveShadow = true;
        scene.add(bankLeft);

        const bankRight = new THREE.Mesh(new THREE.BoxGeometry(30, 2, 300), snowMat);
        bankRight.position.set(21, 0, -100);
        bankRight.receiveShadow = true;
        scene.add(bankRight);

        // --- 5. DECORATIONS (TREES, LAMPS, ROCKS ON SIDES) ---
        const sideDecorations = [];

        function createPineTree() {
            const tree = new THREE.Group();
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.5, 2), woodMat);
            trunk.position.y = 1;
            trunk.castShadow = true;
            tree.add(trunk);

            for(let i = 0; i < 3; i++) {
                const cone = new THREE.Mesh(new THREE.ConeGeometry(2 - i*0.4, 2.5 - i*0.3, 8), leafMat);
                cone.position.y = 2 + i * 1.3;
                cone.castShadow = true;
                tree.add(cone);
            }
            return tree;
        }

        function createStreetLamp() {
            const lamp = new THREE.Group();
            const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 5), woodMat);
            pole.position.y = 2.5;
            pole.castShadow = true;
            lamp.add(pole);

            const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.4, 16, 16), new THREE.MeshBasicMaterial({ color: 0xf7b731 }));
            bulb.position.y = 5;
            lamp.add(bulb);

            const pLight = new THREE.PointLight(0xf7b731, 1, 8);
            pLight.position.y = 5;
            lamp.add(pLight);
            return lamp;
        }

        // Populate side trees & lamps
        for(let z = -200; z < 20; z += 12) {
            // Left side
            const treeL = createPineTree();
            treeL.position.set(-8 - Math.random()*8, 1, z);
            scene.add(treeL);
            sideDecorations.push(treeL);

            // Right side
            const treeR = createPineTree();
            treeR.position.set(8 + Math.random()*8, 1, z + 6);
            scene.add(treeR);
            sideDecorations.push(treeR);

            if(Math.random() > 0.5) {
                const lamp = createStreetLamp();
                lamp.position.set(Math.random() > 0.5 ? -6.8 : 6.8, 1, z);
                scene.add(lamp);
                sideDecorations.push(lamp);
            }
        }

        // --- 6. SANTA CHARACTER (CHARACTER MODEL) ---
        const santa = new THREE.Group();
        
        // Sleigh / Body
        const bodyMesh = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.8, 1.6), new THREE.MeshStandardMaterial({ color: 0xc0392b, roughness: 0.3 }));
        bodyMesh.position.y = 0.6;
        bodyMesh.castShadow = true;
        santa.add(bodyMesh);

        const headMesh = new THREE.Mesh(new THREE.SphereGeometry(0.4, 16, 16), new THREE.MeshStandardMaterial({ color: 0xffdbac }));
        headMesh.position.set(0, 1.3, 0.1);
        headMesh.castShadow = true;
        santa.add(headMesh);

        const hatMesh = new THREE.Mesh(new THREE.ConeGeometry(0.45, 0.8, 16), new THREE.MeshStandardMaterial({ color: 0xd63031 }));
        hatMesh.position.set(0, 1.8, 0);
        hatMesh.rotation.x = -0.2;
        santa.add(hatMesh);

        scene.add(santa);

        // --- 7. GAME STATE & VARIABLES ---
        let gameRunning = false;
        let score = 0;
        let distance = 0;
        let speed = 0.35;
        const lanes = [-3.2, 0, 3.2];
        let currentLane = 1;
        
        let isJumping = false;
        let jumpVelocity = 0;
        const gravity = 0.016;

        let obstacles = [];
        let gifts = [];

        // --- 8. SPAWN OBSTACLES & GIFTS ---
        function spawnEntities() {
            if (!gameRunning) return;

            const laneIdx = Math.floor(Math.random() * lanes.length);
            const xPos = lanes[laneIdx];
            const zPos = -120;

            if (Math.random() < 0.55) {
                // Obstacle (Rock / Snowman / Barrier)
                const obsGroup = new THREE.Group();
                const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.8), new THREE.MeshStandardMaterial({ color: 0x7f8c8d, roughness: 0.9 }));
                rock.position.y = 0.6;
                rock.castShadow = true;
                obsGroup.add(rock);

                obsGroup.position.set(xPos, 0, zPos);
                scene.add(obsGroup);
                obstacles.push(obsGroup);
            } else {
                // Gift Box
                const giftGroup = new THREE.Group();
                const box = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, 0.8), giftMat);
                box.position.y = 0.6;
                box.castShadow = true;
                giftGroup.add(box);

                const ribbon = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.85, 0.2), goldMat);
                ribbon.position.y = 0.6;
                giftGroup.add(ribbon);

                giftGroup.position.set(xPos, 0, zPos);
                scene.add(giftGroup);
                gifts.push(giftGroup);
            }
        }

        // --- 9. CONTROLS ---
        function moveLeft() {
            if (gameRunning && currentLane > 0) currentLane--;
        }

        function moveRight() {
            if (gameRunning && currentLane < 2) currentLane++;
        }

        function jump() {
            if (gameRunning && !isJumping) {
                isJumping = true;
                jumpVelocity = 0.32;
            }
        }

        // Event Listeners for UI Buttons
        document.getElementById('btn-left').addEventListener('pointerdown', (e) => { e.preventDefault(); moveLeft(); });
        document.getElementById('btn-right').addEventListener('pointerdown', (e) => { e.preventDefault(); moveRight(); });
        document.getElementById('btn-jump').addEventListener('pointerdown', (e) => { e.preventDefault(); jump(); });

        // Keyboard Controls
        window.addEventListener('keydown', (e) => {
            if (!gameRunning) return;
            if (e.key === 'ArrowLeft' || e.key === 'a') moveLeft();
            if (e.key === 'ArrowRight' || e.key === 'd') moveRight();
            if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'w') jump();
        });

        // --- 10. GAME LOOP ---
        function startGame() {
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('gameover-screen').style.display = 'none';
            score = 0;
            distance = 0;
            speed = 0.35;
            currentLane = 1;

            obstacles.forEach(o => scene.remove(o));
            gifts.forEach(g => scene.remove(g));
            obstacles = [];
            gifts = [];

            gameRunning = true;
        }

        function restartGame() {
            startGame();
        }

        setInterval(spawnEntities, 1000);

        function animate() {
            requestAnimationFrame(animate);

            if (gameRunning) {
                distance += 0.8;
                speed += 0.00008;

                document.getElementById('distance').innerText = Math.floor(distance / 10);
                document.getElementById('score').innerText = score;

                // Smooth Lane Interpolation
                const targetX = lanes[currentLane];
                santa.position.x += (targetX - santa.position.x) * 0.2;

                // Jump Physics
                if (isJumping) {
                    santa.position.y += jumpVelocity;
                    jumpVelocity -= gravity;
                    if (santa.position.y <= 0) {
                        santa.position.y = 0;
                        isJumping = false;
                    }
                }

                santaLight.position.set(santa.position.x, santa.position.y + 2, santa.position.z);

                // Move side scenery
                sideDecorations.forEach(dec => {
                    dec.position.z += speed;
                    if (dec.position.z > 20) dec.position.z -= 220;
                });

                // Obstacle Logic
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    obstacles[i].position.z += speed;

                    // Collision Detection
                    let dx = santa.position.x - obstacles[i].position.x;
                    let dz = santa.position.z - obstacles[i].position.z;
                    if (Math.abs(dx) < 0.9 && Math.abs(dz) < 0.9 && santa.position.y < 1.0) {
                        gameRunning = false;
                        document.getElementById('final-score').innerText = score;
                        document.getElementById('gameover-screen').style.display = 'flex';
                    }

                    if (obstacles[i].position.z > 15) {
                        scene.remove(obstacles[i]);
                        obstacles.splice(i, 1);
                    }
                }

                // Gift Logic
                for (let i = gifts.length - 1; i >= 0; i--) {
                    gifts[i].position.z += speed;
                    gifts[i].rotation.y += 0.04;

                    let dx = santa.position.x - gifts[i].position.x;
                    let dz = santa.position.z - gifts[i].position.z;
                    if (Math.abs(dx) < 1.0 && Math.abs(dz) < 1.0) {
                        score += 10;
                        scene.remove(gifts[i]);
                        gifts.splice(i, 1);
                    } else if (gifts[i].position.z > 15) {
                        scene.remove(gifts[i]);
                        gifts.splice(i, 1);
                    }
                }
            }

            renderer.render(scene, camera);
        }

        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

# Hiển thị game trên Streamlit
components.html(game_html, height=750, scrolling=False)
