import streamlit as st
import streamlit.components.v1 as components

# Cấu hình Streamlit tràn màn hình
st.set_page_config(
    page_title="Ông Già Noel Vượt Chướng Ngại Vật 3D",
    page_icon="🎅",
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
    <title>Ông Già Noel Vượt Chướng Ngại Vật 3D</title>
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
            background: #010409;
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
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            padding: 14px 32px;
            border-radius: 30px;
            border: 2px solid rgba(255, 255, 255, 0.45);
            color: #ffffff;
            font-size: 24px;
            font-family: 'Comfortaa', cursive;
            font-weight: 700;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7), inset 0 2px 5px rgba(255,255,255,0.5);
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
            background: radial-gradient(circle at center, rgba(15, 23, 42, 0.94) 0%, rgba(1, 4, 9, 0.99) 100%);
            backdrop-filter: blur(22px);
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
            font-size: 38px;
            background: linear-gradient(135deg, #38bdf8 0%, #facc15 50%, #ef4444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
            filter: drop-shadow(0 15px 25px rgba(56, 189, 248, 0.6));
        }
        .subtitle {
            font-size: 16px;
            color: #facc15;
            font-weight: 800;
            margin-bottom: 14px;
            text-shadow: 0 2px 10px rgba(250, 204, 21, 0.4);
        }
        p {
            font-size: 14px;
            color: #cbd5e1;
            max-width: 580px;
            line-height: 1.4;
            margin-bottom: 16px;
            font-weight: 700;
        }
        
        .config-section {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
            width: 100%;
            max-width: 440px;
        }
        .config-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.7);
            padding: 8px 18px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .config-label {
            font-size: 15px;
            font-weight: 800;
            color: #e2e8f0;
        }
        .btn-group {
            display: flex;
            gap: 6px;
        }
        .option-btn {
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: #cbd5e1;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 800;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .option-btn.active {
            background: #38bdf8;
            color: #0f172a;
            border-color: #38bdf8;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.6);
        }

        .btn {
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            color: white;
            border: none;
            padding: 16px 45px;
            font-size: 19px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-weight: 800;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 15px 40px rgba(56, 189, 248, 0.7), inset 0 2px 3px rgba(255,255,255,0.7);
            transition: all 0.25s ease;
            pointer-events: auto;
        }
        .btn:hover {
            transform: translateY(-4px) scale(1.04);
            box-shadow: 0 20px 45px rgba(56, 189, 248, 0.9);
        }
        
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
            border: 2px solid rgba(255, 255, 255, 0.65);
            color: white;
            font-size: 32px;
            width: 78px;
            height: 78px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 12px 28px rgba(0,0,0,0.6);
            touch-action: manipulation;
        }
        .ctrl-btn:active {
            background: rgba(56, 189, 248, 0.9);
            transform: scale(0.88);
        }
        .btn-jump {
            width: 88px;
            height: 88px;
            background: rgba(249, 202, 36, 0.45);
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

    <div id="controls-wrapper">
        <div class="d-pad">
            <div class="ctrl-btn" id="btn-left">⬅️</div>
            <div class="ctrl-btn" id="btn-right">➡️</div>
        </div>
        <div class="action-pad">
            <div class="ctrl-btn btn-jump" id="btn-jump">🚀</div>
        </div>
    </div>

    <div id="start-screen">
        <h1>🎅 ÔNG GIÀ NOEL VƯỢT CHƯỚNG NGẠI VẬT 3D</h1>
        <div class="subtitle">hãy giúp ông vượt chướng ngại vật để ông phát quà nhé</div>
        
        <div class="config-section">
            <div class="config-row">
                <span class="config-label">⚡ Mức độ:</span>
                <div class="btn-group">
                    <button class="option-btn" id="diff-easy" onclick="setDifficulty('easy')">Dễ</button>
                    <button class="option-btn" id="diff-medium" onclick="setDifficulty('medium')">Trung bình</button>
                    <button class="option-btn active" id="diff-hard" onclick="setDifficulty('hard')">Khó (Siêu Tốc 1.0)</button>
                </div>
            </div>
            <div class="config-row">
                <span class="config-label">🔊 Âm thanh:</span>
                <div class="btn-group">
                    <button class="option-btn active" id="sound-on" onclick="setSound(true)">Bật</button>
                    <button class="option-btn" id="sound-off" onclick="setSound(false)">Tắt</button>
                </div>
            </div>
        </div>

        <p><b>Cách chơi:</b> Đổi làn né Cây thông & Người tuyết. Dùng phím Nhảy để vượt qua Cục đá!<br>Điều khiển: <b>Trái / Phải / A / D</b> | Nhảy: <b>Space / Lên</b>.</p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI 🚀</button>
    </div>

    <div id="gameover-screen" style="display: none;">
        <h1>💥 VA CHẠM CỰC MẠNH!</h1>
        <p>Đã xảy ra va chạm trên đường băng tuyết!<br><br>🎁 Tổng số quà thu thập: <b><span id="final-score">0</span></b></p>
        <button class="btn" onclick="restartGame()">CHƠI LẠI 🔄</button>
    </div>

    <script>
        let selectedDifficulty = 'hard'; 
        let soundEnabled = true;

        function setDifficulty(level) {
            selectedDifficulty = level;
            document.getElementById('diff-easy').classList.remove('active');
            document.getElementById('diff-medium').classList.remove('active');
            document.getElementById('diff-hard').classList.remove('active');
            document.getElementById('diff-' + level).classList.add('active');
        }

        function setSound(status) {
            soundEnabled = status;
            document.getElementById('sound-on').classList.remove('active');
            document.getElementById('sound-off').classList.remove('active');
            if(status) {
                document.getElementById('sound-on').classList.add('active');
            } else {
                document.getElementById('sound-off').classList.add('active');
            }
        }

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
                if (!this.ctx && soundEnabled) {
                    try { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e){}
                }
            }
            startBGM() {
                if (!soundEnabled || this.isPlaying) return;
                this.isPlaying = true;
                this.idx = 0;
                this.loopBGM();
            }
            stopBGM() {
                this.isPlaying = false;
                if (this.bgmTimer) clearTimeout(this.bgmTimer);
            }
            loopBGM() {
                if (!soundEnabled || !this.isPlaying || !this.ctx) return;
                const n = this.notes[this.idx];
                const osc = this.ctx.createOscillator(), g = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(n.f, this.ctx.currentTime);
                g.gain.setValueAtTime(0.06, this.ctx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + n.d * 0.9);
                osc.connect(g); g.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + n.d);
                this.idx = (this.idx + 1) % this.notes.length;
                this.bgmTimer = setTimeout(() => this.loopBGM(), n.d * 1000);
            }
            bell() {
                if (!soundEnabled || !this.ctx) return;
                const osc = this.ctx.createOscillator(), g = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(1046.5, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1567.98, this.ctx.currentTime + 0.15);
                g.gain.setValueAtTime(0.35, this.ctx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.4);
                osc.connect(g); g.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.4);
            }
            jump() {
                if (!soundEnabled || !this.ctx) return;
                const osc = this.ctx.createOscillator(), g = this.ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(180, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(450, this.ctx.currentTime + 0.2);
                g.gain.setValueAtTime(0.3, this.ctx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
                osc.connect(g); g.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.2);
            }
            crashBoomCinematic() {
                if (!soundEnabled || !this.ctx) return;
                const now = this.ctx.currentTime;
                const osc1 = this.ctx.createOscillator();
                const gain1 = this.ctx.createGain();
                osc1.type = 'sine';
                osc1.frequency.setValueAtTime(180, now);
                osc1.frequency.exponentialRampToValueAtTime(20, now + 1.0);
                gain1.gain.setValueAtTime(1.2, now);
                gain1.gain.exponentialRampToValueAtTime(0.001, now + 1.0);
                
                const osc2 = this.ctx.createOscillator();
                const gain2 = this.ctx.createGain();
                osc2.type = 'sawtooth';
                osc2.frequency.setValueAtTime(95, now);
                osc2.frequency.exponentialRampToValueAtTime(12, now + 0.6);
                gain2.gain.setValueAtTime(0.8, now);
                gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

                osc1.connect(gain1); gain1.connect(this.ctx.destination);
                osc2.connect(gain2); gain2.connect(this.ctx.destination);
                osc1.start(now); osc2.start(now);
                osc1.stop(now + 1.0); osc2.stop(now + 0.6);
            }
        }
        const audio = new GameAudio();

        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x010409);
        scene.fog = new THREE.FogExp2(0x010409, 0.0065);

        const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 6.8, 13);
        camera.lookAt(0, 1.2, -4);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.55;
        container.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0x38bdf8, 0.65);
        scene.add(ambientLight);

        const moonLight = new THREE.DirectionalLight(0xe0f2fe, 2.3);
        moonLight.position.set(-25, 60, 25);
        moonLight.castShadow = true;
        moonLight.shadow.mapSize.width = 2048;
        moonLight.shadow.mapSize.height = 2048;
        moonLight.shadow.camera.near = 0.5;
        moonLight.shadow.camera.far = 160;
        moonLight.shadow.camera.left = -30;
        moonLight.shadow.camera.right = 30;
        moonLight.shadow.camera.top = 30;
        moonLight.shadow.camera.bottom = -30;
        scene.add(moonLight);

        const moon = new THREE.Mesh(new THREE.SphereGeometry(6.5, 32, 32), new THREE.MeshBasicMaterial({ color: 0xfffbe1 }));
        moon.position.set(-35, 52, -130);
        scene.add(moon);

        const snowCount = 2000;
        const snowGeo = new THREE.BufferGeometry();
        const snowPos = new Float32Array(snowCount * 3);
        const snowSpeeds = [];

        for(let i = 0; i < snowCount; i++) {
            snowPos[i*3] = (Math.random() - 0.5) * 120;
            snowPos[i*3 + 1] = Math.random() * 55;
            snowPos[i*3 + 2] = (Math.random() - 0.5) * 190 - 50;
            snowSpeeds.push({ y: Math.random() * 0.12 + 0.05, x: Math.random() * 0.04 - 0.02 });
        }
        snowGeo.setAttribute('position', new THREE.BufferAttribute(snowPos, 3));
        const snowMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.26, transparent: true, opacity: 0.9 });
        const snowSystem = new THREE.Points(snowGeo, snowMat);
        scene.add(snowSystem);

        const snowGroundMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.28, metalness: 0.05 });
        const iceTrackMat = new THREE.MeshStandardMaterial({ color: 0xbae6fd, roughness: 0.06, metalness: 0.4 });
        const laneDividerMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.65 });
        
        const woodTrunkMat = new THREE.MeshStandardMaterial({ color: 0x3e2723, roughness: 0.9 });
        const pineLeafMat = new THREE.MeshStandardMaterial({ color: 0x064e3b, roughness: 0.45 });
        const snowCapMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });

        const luxuryGiftMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.15, metalness: 0.3, emissive: 0x500000, emissiveIntensity: 0.2 });
        const luxuryGoldRibbonMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.05, metalness: 0.95 });

        const snowmanBodyMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4 });
        const scarfMat = new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.25 });
        const coalMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.1 });
        const carrotMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.35 });
        const topHatMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.15 });

        const santaRedMat = new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.25 });
        const skinMat = new THREE.MeshStandardMaterial({ color: 0xfed7aa, roughness: 0.5 });
        const whiteFurMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.85 });
        const deerMat = new THREE.MeshStandardMaterial({ color: 0x854d0e, roughness: 0.55 });
        const antlerMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.7 });

        const trackGeo = new THREE.PlaneGeometry(16, 300);
        const track = new THREE.Mesh(trackGeo, iceTrackMat);
        track.rotation.x = -Math.PI / 2;
        track.position.z = -100;
        track.receiveShadow = true;
        scene.add(track);

        const dividerL = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 300), laneDividerMat);
        dividerL.rotation.x = -Math.PI / 2; dividerL.position.set(-2.5, 0.01, -100); scene.add(dividerL);

        const dividerR = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 300), laneDividerMat);
        dividerR.rotation.x = -Math.PI / 2; dividerR.position.set(2.5, 0.01, -100); scene.add(dividerR);

        const bankLeft = new THREE.Mesh(new THREE.BoxGeometry(32, 2.2, 300), snowGroundMat);
        bankLeft.position.set(-24, 0, -100); bankLeft.receiveShadow = true; scene.add(bankLeft);

        const bankRight = new THREE.Mesh(new THREE.BoxGeometry(32, 2.2, 300), snowGroundMat);
        bankRight.position.set(24, 0, -100); bankRight.receiveShadow = true; scene.add(bankRight);

        function createSceneryPineTree() {
            const tree = new THREE.Group();
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.55, 2.8), woodTrunkMat);
            trunk.position.y = 1.4; trunk.castShadow = true; tree.add(trunk);
            for(let i = 0; i < 4; i++) {
                const cone = new THREE.Mesh(new THREE.ConeGeometry(2.4 - i*0.45, 2.6, 12), pineLeafMat);
                cone.position.y = 2.0 + i * 1.1; cone.castShadow = true; tree.add(cone);
                const snowCap = new THREE.Mesh(new THREE.ConeGeometry(2.1 - i*0.4, 0.6, 12), snowCapMat);
                snowCap.position.y = 3.1 + i * 1.1; tree.add(snowCap);
            }
            return tree;
        }

        function createObstaclePineTree() {
            const tree = new THREE.Group();
            const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.48, 1.8), woodTrunkMat);
            trunk.position.y = 0.9; trunk.castShadow = true; tree.add(trunk);
            for(let i = 0; i < 3; i++) {
                const cone = new THREE.Mesh(new THREE.ConeGeometry(1.8 - i*0.32, 1.9, 12), pineLeafMat);
                cone.position.y = 1.6 + i * 0.85; cone.castShadow = true; tree.add(cone);
                const snowCap = new THREE.Mesh(new THREE.ConeGeometry(1.55 - i*0.25, 0.5, 12), snowCapMat);
                snowCap.position.y = 2.45 + i * 0.85; tree.add(snowCap);
            }
            return tree;
        }

        const sideDecorations = [];
        for(let z = -200; z < 20; z += 10) {
            const treeL = createSceneryPineTree(); treeL.position.set(-11 - Math.random()*9, 0, z); scene.add(treeL); sideDecorations.push(treeL);
            const treeR = createSceneryPineTree(); treeR.position.set(11 + Math.random()*9, 0, z + 5); scene.add(treeR); sideDecorations.push(treeR);
        }

        const santaGroup = new THREE.Group();

        const sleighMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.6, 2.4), santaRedMat);
        sleighMesh.position.set(0, 0.5, 1.8); sleighMesh.castShadow = true; santaGroup.add(sleighMesh);

        const runnerL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.18, 2.8), luxuryGoldRibbonMat);
        runnerL.position.set(-0.65, 0.16, 1.8); santaGroup.add(runnerL);
        const runnerR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.18, 2.8), luxuryGoldRibbonMat);
        runnerR.position.set(0.65, 0.16, 1.8); santaGroup.add(runnerR);

        const santaCharacter = new THREE.Group();
        const santaTorso = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.42, 0.8), santaRedMat);
        santaTorso.position.set(0, 0.9, 1.6); santaTorso.castShadow = true; santaCharacter.add(santaTorso);
        const santaHead = new THREE.Mesh(new THREE.SphereGeometry(0.3, 16, 16), skinMat);
        santaHead.position.set(0, 1.45, 1.6); santaCharacter.add(santaHead);
        const santaBeard = new THREE.Mesh(new THREE.SphereGeometry(0.32, 16, 16), whiteFurMat);
        santaBeard.position.set(0, 1.32, 1.76); santaCharacter.add(santaBeard);
        const santaHat = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.65, 16), santaRedMat);
        santaHat.position.set(0, 1.88, 1.55); santaHat.rotation.x = -0.3; santaCharacter.add(santaHat);
        const sack = new THREE.Mesh(new THREE.SphereGeometry(0.5, 16, 16), new THREE.MeshStandardMaterial({color: 0x15803d, roughness: 0.6}));
        sack.position.set(0, 0.9, 2.4); santaCharacter.add(sack);
        santaGroup.add(santaCharacter);

        const reindeers = [];
        const reindeerSquad = new THREE.Group();

        function createPhotorealisticReindeer(x, z, isRudolph = false) {
            const deer = new THREE.Group();
            
            const body = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.5, 1.1), deerMat);
            body.position.set(x, 0.75, z); body.castShadow = true; deer.add(body);

            const head = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.35, 0.42), deerMat);
            head.position.set(x, 1.2, z - 0.5); deer.add(head);

            if(isRudolph) {
                const nose = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 16), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
                nose.position.set(x, 1.2, z - 0.78); deer.add(nose);
            }

            const antlerL = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.4, 0.06), antlerMat);
            antlerL.position.set(x - 0.16, 1.6, z - 0.5); antlerL.rotation.z = -0.35; deer.add(antlerL);
            const antlerR = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.4, 0.06), antlerMat);
            antlerR.position.set(x + 0.16, 1.6, z - 0.5); antlerR.rotation.z = 0.35; deer.add(antlerR);

            const legGeo = new THREE.CylinderGeometry(0.05, 0.04, 0.6);
            const legFL = new THREE.Mesh(legGeo, deerMat); legFL.position.set(x - 0.2, 0.3, z - 0.35); deer.add(legFL);
            const legFR = new THREE.Mesh(legGeo, deerMat); legFR.position.set(x + 0.2, 0.3, z - 0.35); deer.add(legFR);
            const legBL = new THREE.Mesh(legGeo, deerMat); legBL.position.set(x - 0.2, 0.3, z + 0.35); deer.add(legBL);
            const legBR = new THREE.Mesh(legGeo, deerMat); legBR.position.set(x + 0.2, 0.3, z + 0.35); deer.add(legBR);

            const angle = Math.random() * Math.PI * 2;
            const speedVel = 0.15 + Math.random() * 0.15;
            deer.userData = { 
                origX: x, origZ: z, 
                vx: Math.cos(angle) * speedVel, 
                vz: Math.sin(angle) * speedVel,
                legs: [legFL, legFR, legBL, legBR],
                offset: Math.random() * Math.PI
            };
            reindeers.push(deer);
            return deer;
        }

        reindeerSquad.add(createPhotorealisticReindeer(-0.32, 0.4));
        reindeerSquad.add(createPhotorealisticReindeer(0.32, 0.4));
        reindeerSquad.add(createPhotorealisticReindeer(-0.32, -0.2));
        reindeerSquad.add(createPhotorealisticReindeer(0.32, -0.2));
        reindeerSquad.add(createPhotorealisticReindeer(-0.32, -0.8));
        reindeerSquad.add(createPhotorealisticReindeer(0.32, -0.8));
        reindeerSquad.add(createPhotorealisticReindeer(-0.32, -1.4));
        reindeerSquad.add(createPhotorealisticReindeer(0.32, -1.4));
        reindeerSquad.add(createPhotorealisticReindeer(-0.32, -2.0, true));
        reindeerSquad.add(createPhotorealisticReindeer(0.32, -2.0, true));

        santaGroup.add(reindeerSquad);

        const headlight = new THREE.SpotLight(0xfffae0, 2.8, 40, Math.PI / 5, 0.4);
        headlight.position.set(0, 1, -1.0);
        headlight.target.position.set(0, 0.5, -12);
        santaGroup.add(headlight);
        santaGroup.add(headlight.target);

        scene.add(santaGroup);

        let crashedGifts = [];
        let activeCrashType = null;

        let gameRunning = false;
        let isGameOverAnim = false;
        let score = 0, distance = 0, speed = 1.0, accelerationRate = 0.005; // Tốc độ xuất phát 1.0 & Gia tốc 0.005
        
        const lanes = [-5.0, 0, 5.0];
        let currentLane = 1;

        let isJumping = false, jumpVelocity = 0;
        const gravity = 0.016;

        let obstacles = [], gifts = [];

        function moveLeft() {
            if (!gameRunning || isGameOverAnim) return;
            if (currentLane > 0) currentLane--;
        }

        function moveRight() {
            if (!gameRunning || isGameOverAnim) return;
            if (currentLane < 2) currentLane++;
        }

        function jump() {
            if (!gameRunning || isGameOverAnim) return;
            if (!isJumping) {
                isJumping = true;
                jumpVelocity = 0.33;
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
            if (!gameRunning || isGameOverAnim) return;
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

        function createGift3D() {
            const giftGroup = new THREE.Group();
            const box = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), luxuryGiftMat);
            box.position.y = 0.6; box.castShadow = true; giftGroup.add(box);

            const ribbonV = new THREE.Mesh(new THREE.BoxGeometry(1.24, 1.24, 0.22), luxuryGoldRibbonMat);
            ribbonV.position.y = 0.6; giftGroup.add(ribbonV);

            const ribbonH = new THREE.Mesh(new THREE.BoxGeometry(0.22, 1.24, 1.24), luxuryGoldRibbonMat);
            ribbonH.position.y = 0.6; giftGroup.add(ribbonH);

            const bowTop = new THREE.Mesh(new THREE.SphereGeometry(0.28, 16, 16), luxuryGoldRibbonMat);
            bowTop.position.y = 1.28; giftGroup.add(bowTop);

            const giftLight = new THREE.PointLight(0xfacc15, 1.2, 4);
            giftLight.position.y = 0.8; giftGroup.add(giftLight);

            return giftGroup;
        }

        function spawnEntities() {
            if (!gameRunning || isGameOverAnim) return;
            const laneIdx = Math.floor(Math.random() * lanes.length);
            const xPos = lanes[laneIdx];
            const zPos = -140;

            const randType = Math.random();
            if (randType < 0.65) {
                const obsGroup = new THREE.Group();
                const type = Math.random();

                if (type < 0.35) {
                    const obstacleTree = createObstaclePineTree();
                    obsGroup.add(obstacleTree);
                    obsGroup.userData = { type: 'high' };
                } else if (type < 0.75) {
                    const bodyLower = new THREE.Mesh(new THREE.SphereGeometry(1.25, 24, 24), snowmanBodyMat);
                    bodyLower.position.y = 1.25; bodyLower.castShadow = true; obsGroup.add(bodyLower);
                    const bodyUpper = new THREE.Mesh(new THREE.SphereGeometry(0.9, 24, 24), snowmanBodyMat);
                    bodyUpper.position.y = 2.65; bodyUpper.castShadow = true; obsGroup.add(bodyUpper);
                    const head = new THREE.Mesh(new THREE.SphereGeometry(0.62, 24, 24), snowmanBodyMat);
                    head.position.y = 3.6; head.castShadow = true; obsGroup.add(head);

                    const scarf = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.68, 0.3, 24), scarfMat);
                    scarf.position.y = 3.2; scarf.castShadow = true; obsGroup.add(scarf);
                    const scarfTail = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.7, 0.1), scarfMat);
                    scarfTail.position.set(0.35, 2.9, 0.45); obsGroup.add(scarfTail);

                    const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 12), coalMat);
                    eyeL.position.set(-0.18, 3.75, 0.52); obsGroup.add(eyeL);
                    const eyeR = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 12), coalMat);
                    eyeR.position.set(0.18, 3.75, 0.52); obsGroup.add(eyeR);

                    const nose = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.45, 16), carrotMat);
                    nose.rotation.x = Math.PI / 2; nose.position.set(0, 3.6, 0.72); obsGroup.add(nose);

                    for(let m = -1; m <= 1; m++) {
                        const mouthDot = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 8), coalMat);
                        mouthDot.position.set(m * 0.1, 3.38, 0.58); obsGroup.add(mouthDot);
                    }

                    const hatBrim = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.08, 24), topHatMat);
                    hatBrim.position.y = 4.0; obsGroup.add(hatBrim);
                    const hatTop = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.45, 24), topHatMat);
                    hatTop.position.y = 4.25; obsGroup.add(hatTop);

                    obsGroup.userData = { type: 'high' };
                } else {
                    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(1.2), new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.8 }));
                    rock.position.y = 0.9; rock.castShadow = true; obsGroup.add(rock);
                    obsGroup.userData = { type: 'jumpable' };
                }

                obsGroup.position.set(xPos, 0, zPos);
                scene.add(obsGroup);
                obstacles.push(obsGroup);
            } else {
                const giftGroup = createGift3D();
                giftGroup.position.set(xPos, 0, zPos);
                scene.add(giftGroup);
                gifts.push(giftGroup);
            }
        }

        function triggerGameOverEffect(obstacleType) {
            gameRunning = false;
            isGameOverAnim = true;
            activeCrashType = obstacleType;
            audio.stopBGM();
            audio.crashBoomCinematic();

            crashedGifts.forEach(g => scene.remove(g));
            crashedGifts = [];

            if (obstacleType === 'rock') {
                sleighMesh.rotation.set(0.3, 0, -Math.PI / 2.5);
                sleighMesh.position.set(0, 0.6, 1.8);
                santaCharacter.position.set(0, 0.8, 1.2);
                santaCharacter.rotation.set(Math.PI / 3, 0, 0.2);
            } else {
                sleighMesh.position.y = 2.4;
                sleighMesh.rotation.x = Math.PI / 35;
                sleighMesh.rotation.z = -Math.PI / 6;
                santaCharacter.position.set(0.8, 0.3, -1.8);
                santaCharacter.rotation.set(Math.PI / 2.2, 0.4, 0);
            }

            for (let i = 0; i < 20; i++) {
                const miniGift = createGift3D();
                miniGift.position.set(
                    santaGroup.position.x + (Math.random() - 0.5) * 6.0,
                    0.2,
                    santaGroup.position.z + (Math.random() - 0.5) * 6.0
                );
                miniGift.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
                scene.add(miniGift);
                crashedGifts.push(miniGift);
            }

            setTimeout(() => {
                document.getElementById('final-score').innerText = score;
                document.getElementById('gameover-screen').style.display = 'flex';
            }, 5000);
        }

        function startGame() {
            audio.init();
            audio.startBGM();
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('gameover-screen').style.display = 'none';
            
            score = 0; distance = 0; currentLane = 1;
            activeCrashType = null;

            if (selectedDifficulty === 'easy') {
                speed = 0.38;
                accelerationRate = 0.00008;
            } else if (selectedDifficulty === 'medium') {
                speed = 0.54;
                accelerationRate = 0.0002;
            } else if (selectedDifficulty === 'hard') {
                speed = 1.0;
                accelerationRate = 0.005;
            }

            sleighMesh.rotation.set(0, 0, 0);
            sleighMesh.position.set(0, 0.5, 1.8);

            santaCharacter.position.set(0, 0, 0);
            santaCharacter.rotation.set(0, 0, 0);

            reindeers.forEach(d => {
                d.position.set(d.userData.origX, 0, d.userData.origZ);
                d.rotation.set(0, 0, 0);
            });

            santaGroup.position.set(lanes[1], 0, 0);

            obstacles.forEach(o => scene.remove(o));
            gifts.forEach(g => scene.remove(g));
            crashedGifts.forEach(cg => scene.remove(cg));

            obstacles = []; gifts = []; crashedGifts = [];
            isGameOverAnim = false;
            gameRunning = true;
        }

        function restartGame() {
            document.getElementById('gameover-screen').style.display = 'none';
            document.getElementById('start-screen').style.display = 'flex';
        }

        setInterval(spawnEntities, 380);

        function animate() {
            requestAnimationFrame(animate);

            const time = Date.now() * 0.01;

            const pos = snowGeo.attributes.position.array;
            for(let i = 0; i < snowCount; i++) {
                pos[i*3 + 1] -= snowSpeeds[i].y;
                pos[i*3] += snowSpeeds[i].x;
                if(pos[i*3 + 1] < 0) pos[i*3 + 1] = 55;
            }
            snowGeo.attributes.position.needsUpdate = true;

            if (gameRunning) {
                distance += 2.0; 
                speed += accelerationRate; 
                document.getElementById('distance').innerText = Math.floor(distance / 10);
                document.getElementById('score').innerText = score;

                const targetX = lanes[currentLane];
                santaGroup.position.x += (targetX - santaGroup.position.x) * 0.3;
                santaGroup.rotation.z = (santaGroup.position.x - targetX) * 0.04;

                reindeers.forEach((d) => {
                    const legCycle = Math.sin(time * 5.5 + d.userData.offset) * 0.5;
                    d.userData.legs[0].rotation.x = legCycle;
                    d.userData.legs[1].rotation.x = -legCycle;
                    d.userData.legs[2].rotation.x = -legCycle;
                    d.userData.legs[3].rotation.x = legCycle;
                });

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

                    if (Math.abs(dx) < 1.3 && Math.abs(dz) < 1.4) {
                        let isHighObstacle = obstacles[i].userData && obstacles[i].userData.type === 'high';
                        let collisionThreshold = isHighObstacle ? 3.5 : 1.2;

                        if (santaGroup.position.y < collisionThreshold) {
                            triggerGameOverEffect(isHighObstacle ? 'high' : 'rock');
                        }
                    }

                    if (obstacles[i].position.z > 15) {
                        scene.remove(obstacles[i]);
                        obstacles.splice(i, 1);
                    }
                }

                for (let i = gifts.length - 1; i >= 0; i--) {
                    gifts[i].position.z += speed;
                    gifts[i].rotation.y += 0.1;

                    let dx = santaGroup.position.x - gifts[i].position.x;
                    let dz = santaGroup.position.z - gifts[i].position.z;

                    if (Math.abs(dx) < 1.35 && Math.abs(dz) < 1.35) {
                        score += 10;
                        audio.bell();
                        scene.remove(gifts[i]);
                        gifts.splice(i, 1);
                    } else if (gifts[i].position.z > 15) {
                        scene.remove(gifts[i]);
                        gifts.splice(i, 1);
                    }
                }
            } else if (isGameOverAnim) {
                reindeers.forEach(d => {
                    d.position.x += d.userData.vx * 1.6;
                    d.position.z += d.userData.vz * 1.6;
                    d.rotation.y += 0.12;
                });
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

components.html(game_html, height=750, scrolling=False)
