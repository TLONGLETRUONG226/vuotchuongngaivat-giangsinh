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

# Mã nguồn HTML / Three.js siêu chân thực kèm Âm thanh
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Santa's Dash Ultra 3D</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@800;900&display=swap');

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
            background: #020617;
            font-family: 'Nunito', sans-serif;
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
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 12px 28px;
            border-radius: 24px;
            border: 2px solid rgba(255, 255, 255, 0.25);
            color: #ffffff;
            font-size: 22px;
            font-family: 'Fredoka One', cursive;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255,255,255,0.4);
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: 1px;
        }
        
        /* UI Screens */
        #start-screen, #gameover-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(15, 23, 42, 0.85) 0%, rgba(2, 6, 23, 0.98) 100%);
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
            box-shadow: 0 12px 30px rgba(235, 77, 75, 0.6), inset 0 2px 2px rgba(255,255,255,0.5);
            transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: auto;
            letter-spacing: 1px;
        }
        .btn:hover {
            transform: translateY(-4px) scale(1.05);
            box-shadow: 0 18px 40px rgba(235, 77, 75, 0.8);
        }
        
        /* Controller Buttons */
        #controls-wrapper {
            position: absolute;
            bottom: 25px;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 35px;
            pointer-events: none;
            z-index: 15;
        }
        .d-pad, .action-pad {
            display: flex;
            gap: 16px;
            pointer-events: auto;
        }
        .ctrl-btn {
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 2px solid rgba(255, 255, 255, 0.4);
            color: white;
            font-size: 28px;
            width: 72px;
            height: 72px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            transition: all 0.1s ease;
        }
        .ctrl-btn:active {
            background: rgba(235, 77, 75, 0.8);
            transform: scale(0.9);
        }
        .btn-jump {
            width: 84px;
            height: 84px;
            background: rgba(249, 202, 36, 0.3);
            border-color: rgba(249, 202, 36, 0.8);
            font-size: 34px;
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

    <!-- Controls -->
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
        <p>Đồng hành cùng Ông Già Noel lướt qua rừng tuyết đêm Giáng Sinh siêu chân thực! Tránh chướng ngại vật và thu thập thật nhiều hộp quà.<br><br><b>Điều khiển:</b> Nút cảm ứng trên màn hình hoặc phím <b>Mũi tên Trái / Phải</b> để chuyển làn, <b>Phím Cách (Space) / Mũi tên Lên</b> để nhảy.</p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI 🎄</button>
    </div>

    <!-- Game Over Screen -->
    <div id="gameover-screen" style="display: none;">
        <h1>💥 VẤP PHẢI CHƯỚNG NGẠI VẬT!</h1>
        <p>Xe trượt tuyết của Santa đã bị lật! Hãy thử lại để đạt điểm số kỷ lục nhé.<br><br>🎁 Tổng số quà thu thập: <b><span id="final-score">0</span></b></p>
        <button class="btn" onclick="restartGame()">CHƠI LẠI 🔄</button>
    </div>

    <script>
        // --- 1. WEB AUDIO SYNTHESIZER (Hệ thống âm thanh không tệp) ---
        class SoundEffects {
            constructor() {
                this.ctx = null;
            }
            init() {
                if (!this.ctx) {
                    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
                }
            }
            playBell() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(987.77, this.ctx.currentTime); // B5
                osc.frequency.exponentialRampToValueAtTime(1318.51, this.ctx.currentTime + 0.1); // E6
                gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.5);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.5);
            }
            playJump() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(150, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(400, this.ctx.currentTime + 0.2);
                gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.2);
            }
            playCrash() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(120, this.ctx.currentTime);
                osc.frequency.linearRampToValueAtTime(30, this.ctx.currentTime + 0.4);
                gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.4);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.4);
            }
        }
        const sfx = new SoundEffects();

        // --- 2. THREE.JS SCENE SETUP ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020617);
        scene.fog = new THREE.FogExp2(0x020617, 0.012);

        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5.5, 11);
        camera.lookAt(0, 1.2, -5);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        container.appendChild(renderer.domElement);

        // --- 3. LIGHTING ---
        const ambientLight = new THREE.AmbientLight(0xdff9fb, 0.5);
        scene.add(ambientLight);

        const moonLight = new THREE.DirectionalLight(0x38bdf8, 1.4);
        moonLight.position.set(-20, 45, 20);
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

        const santaLight = new THREE.PointLight(0xff7675, 2, 12);
        scene.add(santaLight);

        // --- 4. MATERIALS ---
        const snowMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.2, metalness: 0.1 });
        const iceTrackMat = new THREE.MeshStandardMaterial({ color: 0xe0f2fe, roughness: 0.1, metalness: 0.3 });
        const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.8 });
        const leafMat = new THREE.MeshStandardMaterial({ color: 0x065f46, roughness: 0.4 });
        const giftMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.2, metalness: 0.4 });
        const goldMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.1, metalness: 0.9 });
        const redMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.3 });
        const santaRedMat = new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.3 });
        const skinMat = new THREE.MeshStandardMaterial({ color: 0xfed7aa, roughness: 0.6 });
        const whiteFurMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 });

        // --- 5. ENVIRONMENT BUILDER ---
        const trackGeo = new THREE.PlaneGeometry(12, 300);
        const track = new THREE.Mesh(trackGeo, iceTrackMat);
        track.rotation.x = -Math.PI / 2;
        track.position.z = -100;
        track.receiveShadow = true;
        scene.add(track);

        const bankLeft = new THREE.Mesh(new THREE.BoxGeometry(30, 2, 300), snowMat);
        bankLeft.position.set(-21, 0, -100);
        bankLeft.receiveShadow = true;
        scene.add(bankLeft);

        const bankRight = new THREE.Mesh(new THREE.BoxGeometry(30, 2, 300), snowMat);
        bankRight.position.set(21, 0, -100);
        bankRight.receiveShadow = true;
        scene.add(bankRight);

        // Dynamic Side Objects
        const sideDecorations = [];

        function createPineTree() {
            const tree = new THREE.Group();
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.5, 2.5), woodMat);
            trunk.position.y = 1.25;
            trunk.castShadow = true;
            tree.add(trunk);

            for(let i = 0; i < 4; i++) {
                const cone = new THREE.Mesh(new THREE.ConeGeometry(2.2 - i*0.4, 2.8 - i*0.4, 8), leafMat);
                cone.position.y = 2.2 + i * 1.2;
                cone.castShadow = true;
                tree.add(cone);
            }
            return tree;
        }

        function createSnowman() {
            const snowman = new THREE.Group();
            const base = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 16), snowMat);
            base.position.y = 0.8;
            base.castShadow = true;
            snowman.add(base);

            const head = new THREE.Mesh(new THREE.SphereGeometry(0.65, 16, 16), snowMat);
            head.position.y = 2.1;
            head.castShadow = true;
            snowman.add(head);

            const nose = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.6, 8), new THREE.MeshStandardMaterial({ color: 0xea580c }));
            nose.rotation.x = Math.PI / 2;
            nose.position.set(0, 2.1, 0.7);
            snowman.add(nose);

            return snowman;
        }

        function createStreetLamp() {
            const lamp = new THREE.Group();
            const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 5.5), woodMat);
            pole.position.y = 2.75;
            pole.castShadow = true;
            lamp.add(pole);

            const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.45, 16, 16), new THREE.MeshBasicMaterial({ color: 0xfacc15 }));
            bulb.position.y = 5.5;
            lamp.add(bulb);

            const pLight = new THREE.PointLight(0xfacc15, 1.2, 10);
            pLight.position.y = 5.5;
            lamp.add(pLight);
            return lamp;
        }

        for(let z = -200; z < 20; z += 10) {
            const treeL = createPineTree();
            treeL.position.set(-8 - Math.random()*8, 1, z);
            scene.add(treeL);
            sideDecorations.push(treeL);

            const treeR = createPineTree();
            treeR.position.set(8 + Math.random()*8, 1, z + 5);
            scene.add(treeR);
            sideDecorations.push(treeR);

            if(Math.random() > 0.6) {
                const sm = createSnowman();
                sm.position.set(Math.random() > 0.5 ? -6.8 : 6.8, 0, z + 2);
                scene.add(sm);
                sideDecorations.push(sm);
            } else if(Math.random() > 0.5) {
                const lamp = createStreetLamp();
                lamp.position.set(Math.random() > 0.5 ? -6.8 : 6.8, 0, z);
                scene.add(lamp);
                sideDecorations.push(lamp);
            }
        }

        // --- 6. REALISTIC SANTA MODEL ---
        const santaGroup = new THREE.Group();

        // Sleigh (Xe trượt tuyết)
        const sleighBase = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.4, 2.2), santaRedMat);
        sleighBase.position.y = 0.5;
        sleighBase.castShadow = true;
        santaGroup.add(sleighBase);

        const runnerL = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), goldMat);
        runnerL.position.set(-0.6, 0.2, 0);
        santaGroup.add(runnerL);

        const runnerR = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), goldMat);
        runnerR.position.set(0.6, 0.2, 0);
        santaGroup.add(runnerR);

        // Santa Body
        const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 0.9, 16), santaRedMat);
        torso.position.set(0, 1.1, -0.1);
        torso.castShadow = true;
        santaGroup.add(torso);

        // Belt
        const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.56, 0.56, 0.15, 16), new THREE.MeshStandardMaterial({ color: 0x0f172a }));
        belt.position.set(0, 0.95, -0.1);
        santaGroup.add(belt);

        // Head & Beard
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), skinMat);
        head.position.set(0, 1.75, -0.1);
        head.castShadow = true;
        santaGroup.add(head);

        const beard = new THREE.Mesh(new THREE.SphereGeometry(0.38, 16, 16), whiteFurMat);
        beard.position.set(0, 1.65, 0.08);
        santaGroup.add(beard);

        // Hat
        const hat = new THREE.Mesh(new THREE.ConeGeometry(0.38, 0.7, 16), santaRedMat);
        hat.position.set(0, 2.2, -0.15);
        hat.rotation.x = -0.3;
        santaGroup.add(hat);

        const pompom = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), whiteFurMat);
        pompom.position.set(0, 2.5, -0.3);
        santaGroup.add(pompom);

        scene.add(santaGroup);

        // --- 7. GAME LOGIC ---
        let gameRunning = false;
        let score = 0;
        let distance = 0;
        let speed = 0.38;
        const lanes = [-3.2, 0, 3.2];
        let currentLane = 1;

        let isJumping = false;
        let jumpVelocity = 0;
        const gravity = 0.016;

        let obstacles = [];
        let gifts = [];

        function spawnEntities() {
            if (!gameRunning) return;

            const laneIdx = Math.floor(Math.random() * lanes.length);
            const xPos = lanes[laneIdx];
            const zPos = -130;

            if (Math.random() < 0.6) {
                // Obstacle (Rock / Ice Block)
                const obsGroup = new THREE.Group();
                const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.85), new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.9 }));
                rock.position.y = 0.6;
                rock.castShadow = true;
                obsGroup.add(rock);

                obsGroup.position.set(xPos, 0, zPos);
                scene.add(obsGroup);
                obstacles.push(obsGroup);
            } else {
                // Gift Box
                const giftGroup = new THREE.Group();
                const box = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.85, 0.85), giftMat);
                box.position.y = 0.6;
                box.castShadow = true;
                giftGroup.add(box);

                const ribbon = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.9, 0.2), goldMat);
                ribbon.position.y = 0.6;
                giftGroup.add(ribbon);

                giftGroup.position.set(xPos, 0, zPos);
                scene.add(giftGroup);
                gifts.push(giftGroup);
            }
        }

        // Controls
        function moveLeft() {
            if (gameRunning && currentLane > 0) currentLane--;
        }

        function moveRight() {
            if (gameRunning && currentLane < 2) currentLane--;
            if (gameRunning && currentLane < 2) currentLane++;
        }

        function jump() {
            if (gameRunning && !isJumping) {
                isJumping = true;
                jumpVelocity = 0.33;
                sfx.playJump();
            }
        }

        document.getElementById('btn-left').addEventListener('pointerdown', (e) => { e.preventDefault(); moveLeft(); });
        document.getElementById('btn-right').addEventListener('pointerdown', (e) => { e.preventDefault(); moveRight(); });
        document.getElementById('btn-jump').addEventListener('pointerdown', (e) => { e.preventDefault(); jump(); });

        window.addEventListener('keydown', (e) => {
            if (!gameRunning) return;
            if (e.key === 'ArrowLeft' || e.key === 'a') moveLeft();
            if (e.key === 'ArrowRight' || e.key === 'd') moveRight();
            if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'w') jump();
        });

        function startGame() {
            sfx.init();
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('gameover-screen').style.display = 'none';
            score = 0;
            distance = 0;
            speed = 0.38;
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

        setInterval(spawnEntities, 900);

        function animate() {
            requestAnimationFrame(animate);

            if (gameRunning) {
                distance += 0.85;
                speed += 0.00009;

                document.getElementById('distance').innerText = Math.floor(distance / 10);
                document.getElementById('score').innerText = score;

                // Smooth Lane Switching
                const targetX = lanes[currentLane];
                santaGroup.position.x += (targetX - santaGroup.position.x) * 0.22;
                santaGroup.rotation.z = (santaGroup.position.x - targetX) * 0.08;

                // Jump Physics
                if (isJumping) {
                    santaGroup.position.y += jumpVelocity;
                    jumpVelocity -= gravity;
                    if (santaGroup.position.y <= 0) {
                        santaGroup.position.y = 0;
                        isJumping = false;
                    }
                }

                santaLight.position.set(santaGroup.position.x, santaGroup.position.y + 2, santaGroup.position.z);

                // Side scenery movement
                sideDecorations.forEach(dec => {
                    dec.position.z += speed;
                    if (dec.position.z > 20) dec.position.z -= 220;
                });

                // Obstacles Logic
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    obstacles[i].position.z += speed;

                    let dx = santaGroup.position.x - obstacles[i].position.x;
                    let dz = santaGroup.position.z - obstacles[i].position.z;
                    if (Math.abs(dx) < 0.95 && Math.abs(dz) < 0.95 && santaGroup.position.y < 1.1) {
                        gameRunning = false;
                        sfx.playCrash();
                        document.getElementById('final-score').innerText = score;
                        document.getElementById('gameover-screen').style.display = 'flex';
                    }

                    if (obstacles[i].position.z > 15) {
                        scene.remove(obstacles[i]);
                        obstacles.splice(i, 1);
                    }
                }

                // Gifts Logic
                for (let i = gifts.length - 1; i >= 0; i--) {
                    gifts[i].position.z += speed;
                    gifts[i].rotation.y += 0.05;

                    let dx = santaGroup.position.x - gifts[i].position.x;
                    let dz = santaGroup.position.z - gifts[i].position.z;
                    if (Math.abs(dx) < 1.05 && Math.abs(dz) < 1.05) {
                        score += 10;
                        sfx.playBell();
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
