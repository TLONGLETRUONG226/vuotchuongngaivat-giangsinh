import streamlit as st
import streamlit.components.v1 as components

# Cấu hình Streamlit tràn màn hình
st.set_page_config(
    page_title="Santa's Roblox-Style Dash 3D",
    page_icon="🦌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn header và footer mặc định của Streamlit
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

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Santa Roblox Style Dash 3D</title>
    <!-- Phông chữ Việt hóa hiện đại Be Vietnam Pro -->
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@700;800;900&family=Comfortaa:wght@700&display=swap');

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
            background: #0f172a;
            font-family: 'Be Vietnam Pro', sans-serif;
        }
        #canvas-container {
            width: 100vw;
            height: 100vh;
            display: block;
        }
        
        /* HUD UI Kính Mờ */
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
            padding: 24px;
            z-index: 10;
        }
        .hud-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }
        .score-box {
            background: rgba(30, 41, 59, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 14px 32px;
            border-radius: 30px;
            border: 2px solid rgba(255, 255, 255, 0.4);
            color: #ffffff;
            font-size: 24px;
            font-family: 'Comfortaa', cursive;
            font-weight: 700;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), inset 0 2px 4px rgba(255,255,255,0.4);
            display: flex;
            align-items: center;
            gap: 14px;
        }
        
        /* Giao Diện Màn Hình Khởi Đầu & Thua Cuộc */
        #start-screen, #gameover-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(15, 23, 42, 0.92) 0%, rgba(2, 6, 23, 0.99) 100%);
            backdrop-filter: blur(16px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            pointer-events: auto;
            color: white;
            text-align: center;
            z-index: 20;
            padding: 28px;
        }
        h1 {
            font-family: 'Be Vietnam Pro', sans-serif;
            font-weight: 900;
            font-size: 46px;
            background: linear-gradient(135deg, #ff4d4d 0%, #f9ca24 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            filter: drop-shadow(0 12px 20px rgba(56, 189, 248, 0.5));
        }
        p {
            font-size: 18px;
            color: #cbd5e1;
            max-width: 600px;
            line-height: 1.6;
            margin-bottom: 32px;
            font-weight: 700;
        }
        .btn {
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            color: white;
            border: none;
            padding: 20px 60px;
            font-size: 22px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-weight: 800;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 14px 35px rgba(56, 189, 248, 0.65), inset 0 2px 2px rgba(255,255,255,0.6);
            transition: all 0.25s ease;
            pointer-events: auto;
        }
        .btn:hover {
            transform: translateY(-4px) scale(1.04);
            box-shadow: 0 18px 42px rgba(56, 189, 248, 0.85);
        }
        
        /* Phím Bấm Cảm Ứng */
        #controls-wrapper {
            position: absolute;
            bottom: 30px;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 32px;
            pointer-events: none;
            z-index: 15;
        }
        .d-pad, .action-pad {
            display: flex;
            gap: 18px;
            pointer-events: auto;
        }
        .ctrl-btn {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 2px solid rgba(255, 255, 255, 0.6);
            color: white;
            font-size: 32px;
            width: 78px;
            height: 78px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 12px 28px rgba(0,0,0,0.5);
            touch-action: manipulation;
        }
        .ctrl-btn:active {
            background: rgba(56, 189, 248, 0.9);
            transform: scale(0.88);
        }
        .btn-jump {
            width: 88px;
            height: 88px;
            background: rgba(249, 202, 36, 0.4);
            border-color: rgba(249, 202, 36, 0.95);
            font-size: 38px;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="canvas-container"></div>

    <div id="ui-layer">
        <div class="hud-panel">
            <div class="score-box">🎁 Quà: <span id="score">0</span></div>
            <div class="score-box">⭐ Điểm: <span id="distance">0</span>m</div>
        </div>
    </div>

    <!-- Nút Điều Khiển Màn Hình -->
    <div id="controls-wrapper">
        <div class="d-pad">
            <div class="ctrl-btn" id="btn-left">⬅️</div>
            <div class="ctrl-btn" id="btn-right">➡️</div>
        </div>
        <div class="action-pad">
            <div class="ctrl-btn btn-jump" id="btn-jump">🚀</div>
        </div>
    </div>

    <!-- Màn Hình Khởi Đầu -->
    <div id="start-screen">
        <h1>🎄 SANTA ROBLOX DASH 3D</h1>
        <p>Đồ họa phong cách Roblox Low-Poly siêu bắt mắt! Bầy tuần lộc rực rỡ cùng xe trượt của Santa đã sẵn sàng.<br><br><b>Cách chơi:</b> Dùng phím <b>Mũi tên Trái / Phải / A / D</b> hoặc nút cảm ứng để đổi làn, phím <b>Cách (Space) / Lên</b> để nhảy.</p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI 🚀</button>
    </div>

    <!-- Màn Hình Thua -->
    <div id="gameover-screen" style="display: none;">
        <h1>💥 TÔNG TRÚNG RỒI! ĐÙÙÙÙÙÙNG!</h1>
        <p>Xe trượt đã va chạm nổ tung tóe! Hãy thử lại ngay.<br><br>🎁 Tổng số quà thu thập: <b><span id="final-score">0</span></b></p>
        <button class="btn" onclick="restartGame()">CHƠI LẠI 🔄</button>
    </div>

    <script>
        // --- 1. ÂM THANH & HIỆU ỨNG NỔ ĐÙÙÙÙÙÙNG ---
        class GameAudio {
            constructor() {
                this.ctx = null;
                this.bgmTimer = null;
                this.isPlaying = false;
                this.notes = [
                    {f: 659.25, d: 0.25}, {f: 659.25, d: 0.25}, {f: 659.25, d: 0.5},
                    {f: 659.25, d: 0.25}, {f: 659.25, d: 0.25}, {f: 659.25, d: 0.5},
                    {f: 659.25, d: 0.25}, {f: 783.99, d: 0.25}, {f: 523.25, d: 0.35}, {f: 587.33, d: 0.15}, {f: 659.25, d: 0.8},
                    {f: 698.46, d: 0.25}, {f: 698.46, d: 0.25}, {f: 698.46, d: 0.35}, {f: 698.46, d: 0.15},
                    {f: 698.46, d: 0.25}, {f: 659.25, d: 0.25}, {f: 659.25, d: 0.25}, {f: 659.25, d: 0.25},
                    {f: 659.25, d: 0.25}, {f: 587.33, d: 0.25}, {f: 587.33, d: 0.25}, {f: 659.25, d: 0.25}, {f: 587.33, d: 0.5}, {f: 783.99, d: 0.5}
                ];
                this.idx = 0;
            }
            init() {
                if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            }
            startBGM() {
                if (this.isPlaying) return;
                this.isPlaying = true;
                this.idx = 0;
                this.loopBGM();
            }
            stopBGM() {
                this.isPlaying = false;
                if (this.bgmTimer) clearTimeout(this.bgmTimer);
            }
            loopBGM() {
                if (!this.isPlaying || !this.ctx) return;
                const n = this.notes[this.idx];
                const osc = this.ctx.createOscillator(), g = this.ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(n.f, this.ctx.currentTime);
                g.gain.setValueAtTime(0.07, this.ctx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + n.d * 0.9);
                osc.connect(g); g.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + n.d);
                this.idx = (this.idx + 1) % this.notes.length;
                this.bgmTimer = setTimeout(() => this.loopBGM(), n.d * 1000);
            }
            bell() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator(), g = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(1046.5, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1567.98, this.ctx.currentTime + 0.15);
                g.gain.setValueAtTime(0.4, this.ctx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.4);
                osc.connect(g); g.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.4);
            }
            jump() {
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator(), g = this.ctx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(200, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(500, this.ctx.currentTime + 0.2);
                g.gain.setValueAtTime(0.25, this.ctx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
                osc.connect(g); g.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.2);
            }
            crashBoom() {
                if (!this.ctx) return;
                // Hiệu ứng âm thanh nổ cực đại "ĐÙÙÙÙÙÙNG!" với bộ dao động siêu trầm và tiếng ồn gầm rú
                const now = this.ctx.currentTime;
                
                // Sóng vuông siêu trầm (Bass Boom)
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(120, now);
                osc.frequency.exponentialRampToValueAtTime(20, now + 0.9);
                
                gain.gain.setValueAtTime(0.8, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.9);
                
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start(now);
                osc.stop(now + 0.9);
            }
        }
        const audio = new GameAudio();

        // --- 2. KHỞI TẠO THREE.JS ROBLOX STYLE ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a);
        scene.fog = new THREE.FogExp2(0x0f172a, 0.007);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 7, 13);
        camera.lookAt(0, 1.2, -4);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.45;
        container.appendChild(renderer.domElement);

        // --- 3. ÁNH SÁNG PHONG CÁCH ROBLOX VIVID ---
        const ambientLight = new THREE.AmbientLight(0x38bdf8, 0.7);
        scene.add(ambientLight);

        const sunLight = new THREE.DirectionalLight(0xffedd5, 1.8);
        sunLight.position.set(-20, 60, 30);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        sunLight.shadow.camera.near = 0.5;
        sunLight.shadow.camera.far = 160;
        sunLight.shadow.camera.left = -30;
        sunLight.shadow.camera.right = 30;
        sunLight.shadow.camera.top = 30;
        sunLight.shadow.camera.bottom = -30;
        scene.add(sunLight);

        // --- 4. BẦU TRỜI KHỐI LẬP PHƯƠNG & TUYẾT RƠI ---
        const snowCount = 1800;
        const snowGeo = new THREE.BufferGeometry();
        const snowPos = new Float32Array(snowCount * 3);
        const snowSpeeds = [];

        for(let i = 0; i < snowCount; i++) {
            snowPos[i*3] = (Math.random() - 0.5) * 110;
            snowPos[i*3 + 1] = Math.random() * 50;
            snowPos[i*3 + 2] = (Math.random() - 0.5) * 180 - 50;
            snowSpeeds.push({ y: Math.random() * 0.14 + 0.06, x: Math.random() * 0.04 - 0.02 });
        }
        snowGeo.setAttribute('position', new THREE.BufferAttribute(snowPos, 3));
        const snowMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.3, transparent: true, opacity: 0.95 });
        const snowSystem = new THREE.Points(snowGeo, snowMat);
        scene.add(snowSystem);

        // --- 5. CHẤT LIỆU ROBLOX LOW-POLY ---
        const trackMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.1, metalness: 0.2 });
        const snowBankMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.4 });
        const lineMat = new THREE.MeshBasicMaterial({ color: 0xf43f5e });
        
        const woodMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.9 });
        const leafMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.5 });
        const giftMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.2, metalness: 0.5 });
        const goldMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, roughness: 0.1, metalness: 0.8 });
        
        const santaRed = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.3 });
        const skinMat = new THREE.MeshStandardMaterial({ color: 0xffedd5, roughness: 0.5 });
        const whiteMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 });
        const deerBodyMat = new THREE.MeshStandardMaterial({ color: 0xa16207, roughness: 0.7 });
        const antlerMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.8 });

        // Đường chạy
        const trackGeo = new THREE.PlaneGeometry(16, 300);
        const track = new THREE.Mesh(trackGeo, trackMat);
        track.rotation.x = -Math.PI / 2;
        track.position.z = -100;
        track.receiveShadow = true;
        scene.add(track);

        const dividerL = new THREE.Mesh(new THREE.PlaneGeometry(0.25, 300), lineMat);
        dividerL.rotation.x = -Math.PI / 2; dividerL.position.set(-2.5, 0.02, -100); scene.add(dividerL);

        const dividerR = new THREE.Mesh(new THREE.PlaneGeometry(0.25, 300), lineMat);
        dividerR.rotation.x = -Math.PI / 2; dividerR.position.set(2.5, 0.02, -100); scene.add(dividerR);

        const bankLeft = new THREE.Mesh(new THREE.BoxGeometry(35, 3, 300), snowBankMat);
        bankLeft.position.set(-23.5, 0, -100); bankLeft.receiveShadow = true; scene.add(bankLeft);

        const bankRight = new THREE.Mesh(new THREE.BoxGeometry(35, 3, 300), snowBankMat);
        bankRight.position.set(23.5, 0, -100); bankRight.receiveShadow = true; scene.add(bankRight);

        // Cây cảnh 2 bên (Phong cách khối Roblox)
        const sideDecorations = [];
        function createRobloxBlockTree() {
            const tree = new THREE.Group();
            const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.8, 2, 0.8), woodMat);
            trunk.position.y = 1; trunk.castShadow = true; tree.add(trunk);
            const leaves = new THREE.Mesh(new THREE.BoxGeometry(3, 3, 3), leafMat);
            leaves.position.y = 3; leaves.castShadow = true; tree.add(leaves);
            return tree;
        }

        for(let z = -200; z < 20; z += 12) {
            const t1 = createRobloxBlockTree(); t1.position.set(-11 - Math.random()*6, 0, z); scene.add(t1); sideDecorations.push(t1);
            const t2 = createRobloxBlockTree(); t2.position.set(11 + Math.random()*6, 0, z + 6); scene.add(t2); sideDecorations.push(t2);
        }

        // --- 6. MÔ HÌNH SANTA & BẦY TUẦN LỘC PHONG CÁCH ROBLOX ---
        const santaGroup = new THREE.Group();

        // Xe trượt (Sleigh) khối hộp Roblox
        const sleigh = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.6, 2.2), santaRed);
        sleigh.position.set(0, 0.5, 1.6); sleigh.castShadow = true; santaGroup.add(sleigh);

        const runnerL = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.2, 2.6), goldMat);
        runnerL.position.set(-0.7, 0.2, 1.6); santaGroup.add(runnerL);
        const runnerR = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.2, 2.6), goldMat);
        runnerR.position.set(0.7, 0.2, 1.6); santaGroup.add(runnerR);

        // Ông già Noel khối vuông
        const santaTorso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.9, 0.8), santaRed);
        santaTorso.position.set(0, 1.1, 1.4); santaTorso.castShadow = true; santaGroup.add(santaTorso);

        const santaHead = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.6, 0.6), skinMat);
        santaHead.position.set(0, 1.8, 1.4); santaGroup.add(santaHead);

        const santaHat = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.5, 0.65), santaRed);
        santaHat.position.set(0, 2.25, 1.4); santaGroup.add(santaHat);

        const sack = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.9, 0.9), new THREE.MeshStandardMaterial({color: 0x15803d}));
        sack.position.set(0, 1.2, 2.2); santaGroup.add(sack);

        // Hàm tạo tuần lộc kiểu Roblox khối hộp
        function createRobloxReindeer(x, z, isRudolph = false) {
            const deer = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.7, 1.4), deerBodyMat);
            body.position.set(x, 0.9, z); body.castShadow = true; deer.add(body);

            const head = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.5, 0.6), deerBodyMat);
            head.position.set(x, 1.5, z - 0.7); deer.add(head);

            if(isRudolph) {
                const nose = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.2, 0.2), new THREE.MeshBasicMaterial({color: 0xef4444}));
                nose.position.set(x, 1.5, z - 1.0); deer.add(nose);
            }

            const antlerL = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.5, 0.1), antlerMat);
            antlerL.position.set(x - 0.25, 1.9, z - 0.7); deer.add(antlerL);
            const antlerR = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.5, 0.1), antlerMat);
            antlerR.position.set(x + 0.25, 1.9, z - 0.7); deer.add(antlerR);

            return deer;
        }

        // Bầy 6 con tuần lộc dẫn đường
        santaGroup.add(createRobloxReindeer(-0.6, 0));
        santaGroup.add(createRobloxReindeer(0.6, 0));
        santaGroup.add(createRobloxReindeer(-0.6, -1.5));
        santaGroup.add(createRobloxReindeer(0.6, -1.5));
        santaGroup.add(createRobloxReindeer(-0.6, -3.0, true));
        santaGroup.add(createRobloxReindeer(0.6, -3.0, true));

        // Đèn pha rực rỡ
        const headlight = new THREE.SpotLight(0xffedd5, 3.0, 40, Math.PI / 4, 0.5);
        headlight.position.set(0, 1.5, -1.0);
        headlight.target.position.set(0, 0.5, -15);
        santaGroup.add(headlight);
        santaGroup.add(headlight.target);

        scene.add(santaGroup);

        // --- 7. ĐIỀU KHIỂN & 3 LÀN ĐƯỜNG ---
        let gameRunning = false;
        let score = 0, distance = 0, speed = 0.4;
        
        const lanes = [-5.0, 0, 5.0];
        let currentLane = 1;

        let isJumping = false, jumpVelocity = 0;
        const gravity = 0.016;

        let obstacles = [], gifts = [];

        function moveLeft() {
            if (!gameRunning) return;
            if (currentLane > 0) currentLane--;
        }

        function moveRight() {
            if (!gameRunning) return;
            if (currentLane < 2) currentLane++;
        }

        function jump() {
            if (!gameRunning) return;
            if (!isJumping) {
                isJumping = true;
                jumpVelocity = 0.35;
                audio.jump();
            }
        }

        let canMoveLeft = true;
        let canMoveRight = true;

        const btnL = document.getElementById('btn-left');
        const btnR = document.getElementById('btn-right');
        const btnJ = document.getElementById('btn-jump');

        btnL.addEventListener('pointerdown', (e) => { e.preventDefault(); moveLeft(); });
        btnR.addEventListener('pointerdown', (e) => { e.preventDefault(); moveRight(); });
        btnJ.addEventListener('pointerdown', (e) => { e.preventDefault(); jump(); });

        window.addEventListener('keydown', (e) => {
            if (!gameRunning) return;
            if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && canMoveLeft) {
                canMoveLeft = false; moveLeft();
            }
            if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && canMoveRight) {
                canMoveRight = false; moveRight();
            }
            if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
                jump();
            }
        });

        window.addEventListener('keyup', (e) => {
            if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') canMoveLeft = true;
            if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') canMoveRight = true;
        });

        // --- 8. TẠO VẬT CẢN & HỘP QUÀ ROBLOX ---
        function spawnEntities() {
            if (!gameRunning) return;
            const laneIdx = Math.floor(Math.random() * lanes.length);
            const xPos = lanes[laneIdx];
            const zPos = -150;

            if (Math.random() < 0.6) {
                const obsGroup = new THREE.Group();
                const type = Math.random();

                if (type < 0.35) {
                    // Cây thông Roblox
                    const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.5, 0.8), woodMat);
                    trunk.position.y = 0.75; trunk.castShadow = true; obsGroup.add(trunk);
                    const leaves = new THREE.Mesh(new THREE.BoxGeometry(3, 3.5, 3), leafMat);
                    leaves.position.y = 2.8; leaves.castShadow = true; obsGroup.add(leaves);
                } else if (type < 0.7) {
                    // Người tuyết Roblox khối hộp
                    const body = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), snowBankMat);
                    body.position.y = 1.0; body.castShadow = true; obsGroup.add(body);
                    const head = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), snowBankMat);
                    head.position.y = 2.4; head.castShadow = true; obsGroup.add(head);
                } else {
                    // Khối đá tảng Roblox
                    const rock = new THREE.Mesh(new THREE.BoxGeometry(2.2, 2.2, 2.2), new THREE.MeshStandardMaterial({color: 0x475569}));
                    rock.position.y = 1.1; rock.castShadow = true; obsGroup.add(rock);
                }

                obsGroup.position.set(xPos, 0, zPos);
                scene.add(obsGroup);
                obstacles.push(obsGroup);
            } else {
                const giftGroup = new THREE.Group();
                const box = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.3, 1.3), giftMat);
                box.position.y = 0.65; box.castShadow = true; giftGroup.add(box);
                const ribbon = new THREE.Mesh(new THREE.BoxGeometry(1.35, 1.35, 0.3), goldMat);
                ribbon.position.y = 0.65; giftGroup.add(ribbon);

                giftGroup.position.set(xPos, 0, zPos);
                scene.add(giftGroup);
                gifts.push(giftGroup);
            }
        }

        function startGame() {
            audio.init();
            audio.startBGM();
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('gameover-screen').style.display = 'none';
            score = 0; distance = 0; speed = 0.4; currentLane = 1;
            santaGroup.position.set(lanes[1], 0, 0);

            obstacles.forEach(o => scene.remove(o));
            gifts.forEach(g => scene.remove(g));
            obstacles = []; gifts = [];
            gameRunning = true;
        }

        function restartGame() { startGame(); }

        setInterval(spawnEntities, 950);

        // --- 9. VÒNG LẶP ANIMATION ---
        function animate() {
            requestAnimationFrame(animate);

            const pos = snowGeo.attributes.position.array;
            for(let i = 0; i < snowCount; i++) {
                pos[i*3 + 1] -= snowSpeeds[i].y;
                pos[i*3] += snowSpeeds[i].x;
                if(pos[i*3 + 1] < 0) pos[i*3 + 1] = 50;
            }
            snowGeo.attributes.position.needsUpdate = true;

            if (gameRunning) {
                distance += 0.9; speed += 0.00009;
                document.getElementById('distance').innerText = Math.floor(distance / 10);
                document.getElementById('score').innerText = score;

                const targetX = lanes[currentLane];
                santaGroup.position.x += (targetX - santaGroup.position.x) * 0.22;
                santaGroup.rotation.z = (santaGroup.position.x - targetX) * 0.04;

                if (isJumping) {
                    santaGroup.position.y += jumpVelocity;
                    jumpVelocity -= gravity;
                    if (santaGroup.position.y <= 0) {
                        santaGroup.position.y = 0;
                        isJumping = false;
                    }
                }

                sideDecorations.forEach(dec => {
                    dec.position.z += speed;
                    if (dec.position.z > 20) dec.position.z -= 220;
                });

                for (let i = obstacles.length - 1; i >= 0; i--) {
                    obstacles[i].position.z += speed;
                    let dx = santaGroup.position.x - obstacles[i].position.x;
                    let dz = santaGroup.position.z - obstacles[i].position.z;

                    if (Math.abs(dx) < 1.4 && Math.abs(dz) < 1.5 && santaGroup.position.y < 1.3) {
                        gameRunning = false;
                        audio.stopBGM();
                        audio.crashBoom(); // Phát âm thanh nổ ĐÙÙÙÙÙÙNG!
                        document.getElementById('final-score').innerText = score;
                        document.getElementById('gameover-screen').style.display = 'flex';
                    }

                    if (obstacles[i].position.z > 15) {
                        scene.remove(obstacles[i]);
                        obstacles.splice(i, 1);
                    }
                }

                for (let i = gifts.length - 1; i >= 0; i--) {
                    gifts[i].position.z += speed;
                    gifts[i].rotation.y += 0.05;

                    let dx = santaGroup.position.x - gifts[i].position.x;
                    let dz = santaGroup.position.z - gifts[i].position.z;

                    if (Math.abs(dx) < 1.4 && Math.abs(dz) < 1.4) {
                        score += 10;
                        audio.bell();
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
