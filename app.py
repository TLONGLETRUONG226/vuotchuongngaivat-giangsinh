import streamlit as st
import streamlit.components.v1 as components

# Cấu hình Streamlit tràn màn hình
st.set_page_config(
    page_title="Santa's Christmas Dash 3D Hyper-Realistic",
    page_icon="🎅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn các thành phần thừa của Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0rem !important;
    }
    iframe {
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Code HTML/Three.js siêu chân thực kèm sửa lỗi điều khiển
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Santa Dash 3D Hyper-Realistic</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@800;900&display=swap');

        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #020617;
            font-family: 'Nunito', sans-serif;
        }
        #canvas-container {
            width: 100vw;
            height: 100vh;
            display: block;
        }
        
        /* HUD UI */
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
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 12px 28px;
            border-radius: 24px;
            border: 2px solid rgba(255, 255, 255, 0.25);
            color: #ffffff;
            font-size: 22px;
            font-family: 'Fredoka One', cursive;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Screens Overlay */
        #start-screen, #gameover-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(15, 23, 42, 0.8) 0%, rgba(2, 6, 23, 0.96) 100%);
            backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            pointer-events: auto;
            color: white;
            text-align: center;
            z-index: 20;
            padding: 24px;
        }
        h1 {
            font-family: 'Fredoka One', cursive;
            font-size: 52px;
            background: linear-gradient(135deg, #ff4d4d 0%, #f9ca24 50%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            filter: drop-shadow(0 10px 15px rgba(255, 77, 77, 0.4));
        }
        p {
            font-size: 18px;
            color: #cbd5e1;
            max-width: 550px;
            line-height: 1.6;
            margin-bottom: 32px;
            font-weight: 800;
        }
        .btn {
            background: linear-gradient(135deg, #eb4d4b 0%, #ff7979 100%);
            color: white;
            border: none;
            padding: 18px 56px;
            font-size: 22px;
            font-family: 'Fredoka One', cursive;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 12px 30px rgba(235, 77, 75, 0.6);
            transition: all 0.2s ease;
            pointer-events: auto;
        }
        .btn:hover {
            transform: translateY(-3px) scale(1.03);
        }
        
        /* Controls Overlay Fix */
        #controls-wrapper {
            position: absolute;
            bottom: 30px;
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
            gap: 16px;
            pointer-events: auto;
        }
        .ctrl-btn {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 2px solid rgba(255, 255, 255, 0.5);
            color: white;
            font-size: 30px;
            width: 76px;
            height: 76px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            touch-action: manipulation;
        }
        .ctrl-btn:active {
            background: rgba(235, 77, 75, 0.9);
            transform: scale(0.88);
        }
        .btn-jump {
            width: 86px;
            height: 86px;
            background: rgba(249, 202, 36, 0.35);
            border-color: rgba(249, 202, 36, 0.9);
            font-size: 36px;
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

    <!-- On-screen Controls -->
    <div id="controls-wrapper">
        <div class="d-pad">
            <div class="ctrl-btn" id="btn-left">⬅️</div>
            <div class="ctrl-btn" id="btn-right">➡️</div>
        </div>
        <div class="action-pad">
            <div class="ctrl-btn btn-jump" id="btn-jump">🚀</div>
        </div>
    </div>

    <!-- Screens -->
    <div id="start-screen">
        <h1>🎅 SANTA'S DASH 3D ULTRA</h1>
        <p>Bầu trời tuyết rơi huyền ảo! Giúp Ông Già Noel thu thập quà và tránh chướng ngại vật trong đêm Giáng Sinh.<br><br><b>Điều khiển:</b> Bấm các nút mũi tên trên màn hình hoặc dùng phím <b>Mũi tên Trái / Phải</b> để chuyển làn, <b>Phím Cách / Mũi tên Lên</b> để nhảy.</p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI ❄️</button>
    </div>

    <div id="gameover-screen" style="display: none;">
        <h1>💥 VẤP PHẢI CHƯỚNG NGẠI VẬT!</h1>
        <p>Xe trượt tuyết bị lật rồi! Hãy thử lại để giành lại số quà đã mất nhé.<br><br>🎁 Tổng số quà: <b><span id="final-score">0</span></b></p>
        <button class="btn" onclick="restartGame()">CHƠI LẠI 🔄</button>
    </div>

    <script>
        // --- 1. AUDIO SYNTHESIZER ---
        class SoundFX {
            constructor() { this.ctx = null; }
            init() { if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)(); }
            bell() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator(), gain = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(1046.5, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1567.98, this.ctx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.4, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.4);
                osc.connect(gain); gain.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.4);
            }
            jump() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator(), gain = this.ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(180, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(450, this.ctx.currentTime + 0.2);
                gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
                osc.connect(gain); gain.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.2);
            }
            crash() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator(), gain = this.ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(140, this.ctx.currentTime);
                osc.frequency.linearRampToValueAtTime(40, this.ctx.currentTime + 0.4);
                gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.4);
                osc.connect(gain); gain.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.4);
            }
        }
        const sfx = new SoundFX();

        // --- 2. THREE.JS SCENE SETUP ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x030712);
        scene.fog = new THREE.FogExp2(0x030712, 0.01);

        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5.5, 11);
        camera.lookAt(0, 1.2, -5);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.25;
        container.appendChild(renderer.domElement);

        // --- 3. LIGHTING & MOON ---
        const ambientLight = new THREE.AmbientLight(0x38bdf8, 0.45);
        scene.add(ambientLight);

        const moonLight = new THREE.DirectionalLight(0xbfdbfe, 1.5);
        moonLight.position.set(-25, 50, 20);
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

        // Moon Mesh
        const moonGeo = new THREE.SphereGeometry(4, 32, 32);
        const moonMat = new THREE.MeshBasicMaterial({ color: 0xfffbe1 });
        const moon = new THREE.Mesh(moonGeo, moonMat);
        moon.position.set(-30, 45, -120);
        scene.add(moon);

        const santaLight = new THREE.PointLight(0xef4444, 2, 12);
        scene.add(santaLight);

        // --- 4. SNOW PARTICLES IN SKY (BẦU TRỜI TUYẾT RƠI) ---
        const snowCount = 1200;
        const snowGeo = new THREE.BufferGeometry();
        const snowPos = new Float32Array(snowCount * 3);
        const snowSpeeds = [];

        for(let i = 0; i < snowCount; i++) {
            snowPos[i*3] = (Math.random() - 0.5) * 80;
            snowPos[i*3 + 1] = Math.random() * 40;
            snowPos[i*3 + 2] = (Math.random() - 0.5) * 160 - 50;
            snowSpeeds.push({
                y: Math.random() * 0.12 + 0.05,
                x: Math.random() * 0.04 - 0.02
            });
        }
        snowGeo.setAttribute('position', new THREE.BufferAttribute(snowPos, 3));
        const snowMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.25, transparent: true, opacity: 0.85 });
        const snowSystem = new THREE.Points(snowGeo, snowMat);
        scene.add(snowSystem);

        // --- 5. MATERIALS ---
        const snowGroundMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.25, metalness: 0.1 });
        const iceTrackMat = new THREE.MeshStandardMaterial({ color: 0xbae6fd, roughness: 0.1, metalness: 0.25 });
        const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.8 });
        const leafMat = new THREE.MeshStandardMaterial({ color: 0x047857, roughness: 0.4 });
        const giftMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.2, metalness: 0.4 });
        const goldMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.1, metalness: 0.9 });
        const santaRedMat = new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.3 });
        const skinMat = new THREE.MeshStandardMaterial({ color: 0xfed7aa, roughness: 0.6 });
        const whiteFurMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 });

        // Track & Snowbanks
        const trackGeo = new THREE.PlaneGeometry(12, 300);
        const track = new THREE.Mesh(trackGeo, iceTrackMat);
        track.rotation.x = -Math.PI / 2;
        track.position.z = -100;
        track.receiveShadow = true;
        scene.add(track);

        const bankLeft = new THREE.Mesh(new THREE.BoxGeometry(30, 2, 300), snowGroundMat);
        bankLeft.position.set(-21, 0, -100);
        bankLeft.receiveShadow = true;
        scene.add(bankLeft);

        const bankRight = new THREE.Mesh(new THREE.BoxGeometry(30, 2, 300), snowGroundMat);
        bankRight.position.set(21, 0, -100);
        bankRight.receiveShadow = true;
        scene.add(bankRight);

        // Side Scenery
        const sideDecorations = [];
        function createPineTree() {
            const tree = new THREE.Group();
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.5, 2.5), woodMat);
            trunk.position.y = 1.25; trunk.castShadow = true; tree.add(trunk);
            for(let i = 0; i < 4; i++) {
                const cone = new THREE.Mesh(new THREE.ConeGeometry(2.2 - i*0.4, 2.8 - i*0.4, 8), leafMat);
                cone.position.y = 2.2 + i * 1.2; cone.castShadow = true; tree.add(cone);
            }
            return tree;
        }

        for(let z = -200; z < 20; z += 10) {
            const treeL = createPineTree(); treeL.position.set(-8 - Math.random()*8, 1, z); scene.add(treeL); sideDecorations.push(treeL);
            const treeR = createPineTree(); treeR.position.set(8 + Math.random()*8, 1, z + 5); scene.add(treeR); sideDecorations.push(treeR);
        }

        // --- 6. SANTA CHARACTER MODEL ---
        const santaGroup = new THREE.Group();
        const sleighBase = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.4, 2.2), santaRedMat);
        sleighBase.position.y = 0.5; sleighBase.castShadow = true; santaGroup.add(sleighBase);

        const runnerL = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), goldMat);
        runnerL.position.set(-0.6, 0.2, 0); santaGroup.add(runnerL);
        const runnerR = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), goldMat);
        runnerR.position.set(0.6, 0.2, 0); santaGroup.add(runnerR);

        const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 0.9, 16), santaRedMat);
        torso.position.set(0, 1.1, -0.1); torso.castShadow = true; santaGroup.add(torso);

        const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), skinMat);
        head.position.set(0, 1.75, -0.1); head.castShadow = true; santaGroup.add(head);

        const beard = new THREE.Mesh(new THREE.SphereGeometry(0.38, 16, 16), whiteFurMat);
        beard.position.set(0, 1.65, 0.08); santaGroup.add(beard);

        const hat = new THREE.Mesh(new THREE.ConeGeometry(0.38, 0.7, 16), santaRedMat);
        hat.position.set(0, 2.2, -0.15); hat.rotation.x = -0.3; santaGroup.add(hat);

        scene.add(santaGroup);

        // --- 7. GAME STATE & FIX MOVEMENT LOGIC ---
        let gameRunning = false;
        let score = 0, distance = 0, speed = 0.38;
        const lanes = [-3.2, 0, 3.2];
        let currentLane = 1;

        let isJumping = false, jumpVelocity = 0;
        const gravity = 0.016;

        let obstacles = [], gifts = [];

        function moveLeft() {
            if (gameRunning && currentLane > 0) {
                currentLane--;
            }
        }

        function moveRight() {
            if (gameRunning && currentLane < 2) {
                currentLane++;
            }
        }

        function jump() {
            if (gameRunning && !isJumping) {
                isJumping = true;
                jumpVelocity = 0.33;
                sfx.jump();
            }
        }

        // BIND EVENT LISTENERS CHO CẢ MÁY TÍNH VÀ CẢM ỨNG DI ĐỘNG
        const btnL = document.getElementById('btn-left');
        const btnR = document.getElementById('btn-right');
        const btnJ = document.getElementById('btn-jump');

        const bindTrigger = (elem, fn) => {
            elem.addEventListener('pointerdown', (e) => { e.preventDefault(); fn(); });
            elem.addEventListener('touchstart', (e) => { e.preventDefault(); fn(); }, {passive: false});
        };

        bindTrigger(btnL, moveLeft);
        bindTrigger(btnR, moveRight);
        bindTrigger(btnJ, jump);

        window.addEventListener('keydown', (e) => {
            if (!gameRunning) return;
            if (e.key === 'ArrowLeft' || e.key === 'a') moveLeft();
            if (e.key === 'ArrowRight' || e.key === 'd') moveRight();
            if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'w') jump();
        });

        // --- 8. SPAWN LOGIC ---
        function spawnEntities() {
            if (!gameRunning) return;
            const laneIdx = Math.floor(Math.random() * lanes.length);
            const xPos = lanes[laneIdx];
            const zPos = -130;

            if (Math.random() < 0.6) {
                const obsGroup = new THREE.Group();
                const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.85), new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.9 }));
                rock.position.y = 0.6; rock.castShadow = true; obsGroup.add(rock);
                obsGroup.position.set(xPos, 0, zPos); scene.add(obsGroup); obstacles.push(obsGroup);
            } else {
                const giftGroup = new THREE.Group();
                const box = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.85, 0.85), giftMat);
                box.position.y = 0.6; box.castShadow = true; giftGroup.add(box);
                const ribbon = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.9, 0.2), goldMat);
                ribbon.position.y = 0.6; giftGroup.add(ribbon);
                giftGroup.position.set(xPos, 0, zPos); scene.add(giftGroup); gifts.push(giftGroup);
            }
        }

        function startGame() {
            sfx.init();
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('gameover-screen').style.display = 'none';
            score = 0; distance = 0; speed = 0.38; currentLane = 1;
            santaGroup.position.set(lanes[1], 0, 0);

            obstacles.forEach(o => scene.remove(o));
            gifts.forEach(g => scene.remove(g));
            obstacles = []; gifts = [];
            gameRunning = true;
        }

        function restartGame() { startGame(); }

        setInterval(spawnEntities, 950);

        // --- 9. MAIN ANIMATION LOOP ---
        function animate() {
            requestAnimationFrame(animate);

            // Xử lý tuyết rơi bầu trời liên tục
            const pos = snowGeo.attributes.position.array;
            for(let i = 0; i < snowCount; i++) {
                pos[i*3 + 1] -= snowSpeeds[i].y;
                pos[i*3] += snowSpeeds[i].x;
                if(pos[i*3 + 1] < 0) pos[i*3 + 1] = 40;
            }
            snowGeo.attributes.position.needsUpdate = true;

            if (gameRunning) {
                distance += 0.85; speed += 0.00008;
                document.getElementById('distance').innerText = Math.floor(distance / 10);
                document.getElementById('score').innerText = score;

                // Di chuyển mượt sang làn
                const targetX = lanes[currentLane];
                santaGroup.position.x += (targetX - santaGroup.position.x) * 0.25;
                santaGroup.rotation.z = (santaGroup.position.x - targetX) * 0.06;

                // Vật lý nhảy
                if (isJumping) {
                    santaGroup.position.y += jumpVelocity;
                    jumpVelocity -= gravity;
                    if (santaGroup.position.y <= 0) {
                        santaGroup.position.y = 0;
                        isJumping = false;
                    }
                }

                santaLight.position.set(santaGroup.position.x, santaGroup.position.y + 2, santaGroup.position.z);

                // Cảnh quan di chuyển
                sideDecorations.forEach(dec => {
                    dec.position.z += speed;
                    if (dec.position.z > 20) dec.position.z -= 220;
                });

                // Chướng ngại vật
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    obstacles[i].position.z += speed;
                    let dx = santaGroup.position.x - obstacles[i].position.x;
                    let dz = santaGroup.position.z - obstacles[i].position.z;

                    if (Math.abs(dx) < 0.95 && Math.abs(dz) < 0.95 && santaGroup.position.y < 1.1) {
                        gameRunning = false;
                        sfx.crash();
                        document.getElementById('final-score').innerText = score;
                        document.getElementById('gameover-screen').style.display = 'flex';
                    }

                    if (obstacles[i].position.z > 15) {
                        scene.remove(obstacles[i]);
                        obstacles.splice(i, 1);
                    }
                }

                // Hộp quà
                for (let i = gifts.length - 1; i >= 0; i--) {
                    gifts[i].position.z += speed;
                    gifts[i].rotation.y += 0.05;

                    let dx = santaGroup.position.x - gifts[i].position.x;
                    let dz = santaGroup.position.z - gifts[i].position.z;

                    if (Math.abs(dx) < 1.05 && Math.abs(dz) < 1.05) {
                        score += 10;
                        sfx.bell();
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

# Render trong Streamlit
components.html(game_html, height=750, scrolling=False)
