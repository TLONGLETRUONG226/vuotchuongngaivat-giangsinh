import streamlit as st
import streamlit.components.v1 as components

# Cấu hình Streamlit tràn màn hình
st.set_page_config(
    page_title="Santa's Cinematic Photorealistic Dash 3D",
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
    <title>Santa Photorealistic Cinematic Dash</title>
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
        
        /* HUD UI Kính Mờ Đẳng Cấp */
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
            background: radial-gradient(circle at center, rgba(15, 23, 42, 0.9) 0%, rgba(1, 4, 9, 0.99) 100%);
            backdrop-filter: blur(20px);
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
            font-size: 48px;
            background: linear-gradient(135deg, #38bdf8 0%, #facc15 50%, #ef4444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            filter: drop-shadow(0 15px 25px rgba(56, 189, 248, 0.6));
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
            box-shadow: 0 15px 40px rgba(56, 189, 248, 0.7), inset 0 2px 3px rgba(255,255,255,0.7);
            transition: all 0.25s ease;
            pointer-events: auto;
        }
        .btn:hover {
            transform: translateY(-4px) scale(1.04);
            box-shadow: 0 20px 45px rgba(56, 189, 248, 0.9);
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
        <h1>🎄 SANTA CINEMATIC DASH 3D</h1>
        <p>Đồ họa siêu chân thực cao cấp! Khám phá con đường tuyết trắng lung linh với rừng thông tự nhiên và người tuyết cực kỳ sống động.<br><br><b>Cách chơi:</b> Dùng phím <b>Mũi tên Trái / Phải / A / D</b> hoặc nút cảm ứng để đổi làn, phím <b>Cách (Space) / Lên</b> để nhảy.</p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI 🚀</button>
    </div>

    <!-- Màn Hình Thua -->
    <div id="gameover-screen" style="display: none;">
        <h1>💥 VẤP PHẢI CHƯỚNG NGẠI VẬT!</h1>
        <p>Xe trượt đã va chạm! Hãy thử lại ngay.<br><br>🎁 Tổng số quà thu thập: <b><span id="final-score">0</span></b></p>
        <button class="btn" onclick="restartGame()">CHƠI LẠI 🔄</button>
    </div>

    <script>
        // --- 1. ÂM THANH NỔ "ĐÙNG!" CINEMATIC ---
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
                if (!this.ctx) return;
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
                if (!this.ctx) return;
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
                if (!this.ctx) return;
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

        // --- 2. KHỞI TẠO THREE.JS PHOTOREALISTIC ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x010409);
        scene.fog = new THREE.FogExp2(0x010409, 0.0065);

        const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 6.5, 12);
        camera.lookAt(0, 1.2, -4);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.55;
        container.appendChild(renderer.domElement);

        // --- 3. ÁNH SÁNG CHIỀU SÂU CINEMATIC ---
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

        // --- 4. HỆ THỐNG TUYẾT RƠI TINH TẾ ---
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

        // --- 5. CHẤT LIỆU CAO CẤP & ĐƯỜNG BĂNG ---
        const snowGroundMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.28, metalness: 0.05 });
        const iceTrackMat = new THREE.MeshStandardMaterial({ color: 0xbae6fd, roughness: 0.06, metalness: 0.4 });
        const laneDividerMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.65 });
        
        const woodTrunkMat = new THREE.MeshStandardMaterial({ color: 0x3e2723, roughness: 0.9 });
        const pineLeafMat = new THREE.MeshStandardMaterial({ color: 0x064e3b, roughness: 0.45 });
        const snowCapMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });

        // Hộp quà siêu cấp
        const luxuryGiftMat = new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.12, metalness: 0.35, emissive: 0x450a0a, emissiveIntensity: 0.3 });
        const luxuryGoldRibbonMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.08, metalness: 0.98 });

        // Người tuyết siêu thực
        const snowmanBodyMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4 });
        const scarfMat = new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.25 });
        const coalMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.1 });
        const carrotMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.35 });
        const topHatMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.15 });

        const santaRedMat = new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.25 });
        const skinMat = new THREE.MeshStandardMaterial({ color: 0xfed7aa, roughness: 0.5 });
        const whiteFurMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.85 });
        const deerMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.6 });
        const antlerMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.7 });

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

        // --- HÀM TẠO CÂY THÔNG CHUẨN PHOTOREALISTIC (DÙNG CHUNG CHO CẢ 2 BÊN & CHƯỚNG NGẠI VẬT) ---
        function createPhotorealisticPineTree() {
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

        const sideDecorations = [];
        for(let z = -200; z < 20; z += 10) {
            const treeL = createPhotorealisticPineTree(); treeL.position.set(-11 - Math.random()*9, 0, z); scene.add(treeL); sideDecorations.push(treeL);
            const treeR = createPhotorealisticPineTree(); treeR.position.set(11 + Math.random()*9, 0, z + 5); scene.add(treeR); sideDecorations.push(treeR);
        }

        // --- 6. XE TRƯỢT & BẦY TUẦN LỘC ---
        const santaGroup = new THREE.Group();

        const sleigh = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.55, 2.1), santaRedMat);
        sleigh.position.set(0, 0.45, 1.8); sleigh.castShadow = true; santaGroup.add(sleigh);

        const runnerL = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.15, 2.5), luxuryGoldRibbonMat);
        runnerL.position.set(-0.6, 0.15, 1.8); santaGroup.add(runnerL);
        const runnerR = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.15, 2.5), luxuryGoldRibbonMat);
        runnerR.position.set(0.6, 0.15, 1.8); santaGroup.add(runnerR);

        const santaTorso = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.4, 0.75), santaRedMat);
        santaTorso.position.set(0, 0.85, 1.6); santaTorso.castShadow = true; santaGroup.add(santaTorso);

        const santaHead = new THREE.Mesh(new THREE.SphereGeometry(0.3, 16, 16), skinMat);
        santaHead.position.set(0, 1.4, 1.6); santaGroup.add(santaHead);

        const santaBeard = new THREE.Mesh(new THREE.SphereGeometry(0.32, 16, 16), whiteFurMat);
        santaBeard.position.set(0, 1.3, 1.75); santaGroup.add(santaBeard);

        const santaHat = new THREE.Mesh(new THREE.ConeGeometry(0.32, 0.6, 16), santaRedMat);
        santaHat.position.set(0, 1.8, 1.55); santaHat.rotation.x = -0.3; santaGroup.add(santaHat);

        const sack = new THREE.Mesh(new THREE.SphereGeometry(0.48, 16, 16), new THREE.MeshStandardMaterial({color: 0x16a34a, roughness: 0.6}));
        sack.position.set(0, 0.85, 2.35); santaGroup.add(sack);

        function createPhotorealisticReindeer(x, z, isRudolph = false) {
            const deer = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.6, 1.3), deerMat);
            body.position.set(x, 0.8, z); body.castShadow = true; deer.add(body);

            const head = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.45, 0.5), deerMat);
            head.position.set(x, 1.3, z - 0.6); deer.add(head);

            if(isRudolph) {
                const nose = new THREE.Mesh(new THREE.SphereGeometry(0.13, 16, 16), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
                nose.position.set(x, 1.3, z - 0.92); deer.add(nose);
            }

            const antlerL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.45, 0.08), antlerMat);
            antlerL.position.set(x - 0.2, 1.75, z - 0.6); antlerL.rotation.z = -0.3; deer.add(antlerL);

            const antlerR = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.45, 0.08), antlerMat);
            antlerR.position.set(x + 0.2, 1.75, z - 0.6); antlerR.rotation.z = 0.3; deer.add(antlerR);

            return deer;
        }

        santaGroup.add(createPhotorealisticReindeer(-0.55, 0.2));
        santaGroup.add(createPhotorealisticReindeer(0.55, 0.2));
        santaGroup.add(createPhotorealisticReindeer(-0.55, -1.2));
        santaGroup.add(createPhotorealisticReindeer(0.55, -1.2));
        santaGroup.add(createPhotorealisticReindeer(-0.55, -2.6, true));
        santaGroup.add(createPhotorealisticReindeer(0.55, -2.6, true));

        const headlight = new THREE.SpotLight(0xfffae0, 2.8, 40, Math.PI / 5, 0.4);
        headlight.position.set(0, 1, -1.0);
        headlight.target.position.set(0, 0.5, -12);
        santaGroup.add(headlight);
        santaGroup.add(headlight.target);

        scene.add(santaGroup);

        // --- 7. ĐIỀU KHIỂN & LÀN ĐƯỜNG ---
        let gameRunning = false;
        let score = 0, distance = 0, speed = 0.38;
        
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

        // --- 8. TẠO VẬT CẢN & HỘP QUÀ SIÊU THỰC ---
        function spawnEntities() {
            if (!gameRunning) return;
            const laneIdx = Math.floor(Math.random() * lanes.length);
            const xPos = lanes[laneIdx];
            const zPos = -140;

            const randType = Math.random();
            if (randType < 0.6) {
                const obsGroup = new THREE.Group();
                const type = Math.random();

                if (type < 0.35) {
                    // Cây thông chướng ngại vật nay dùng chung hàm với rừng cây 2 bên cho cực kỳ chân thực
                    const obstacleTree = createPhotorealisticPineTree();
                    obsGroup.add(obstacleTree);
                } else if (type < 0.75) {
                    // --- NGƯỜI TUYẾT SỐNG ĐỘNG NHƯ THẬT ---
                    const bodyLower = new THREE.Mesh(new THREE.SphereGeometry(1.15, 24, 24), snowmanBodyMat);
                    bodyLower.position.y = 1.15; bodyLower.castShadow = true; obsGroup.add(bodyLower);

                    const bodyUpper = new THREE.Mesh(new THREE.SphereGeometry(0.82, 24, 24), snowmanBodyMat);
                    bodyUpper.position.y = 2.45; bodyUpper.castShadow = true; obsGroup.add(bodyUpper);

                    const head = new THREE.Mesh(new THREE.SphereGeometry(0.58, 24, 24), snowmanBodyMat);
                    head.position.y = 3.35; head.castShadow = true; obsGroup.add(head);

                    const scarf = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.62, 0.28, 24), scarfMat);
                    scarf.position.y = 3.0; scarf.castShadow = true; obsGroup.add(scarf);
                    const scarfTail = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.65, 0.1), scarfMat);
                    scarfTail.position.set(0.32, 2.7, 0.42); obsGroup.add(scarfTail);

                    const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 12), coalMat);
                    eyeL.position.set(-0.18, 3.48, 0.5); obsGroup.add(eyeL);
                    const eyeR = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 12), coalMat);
                    eyeR.position.set(0.18, 3.48, 0.5); obsGroup.add(eyeR);

                    const nose = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.42, 16), carrotMat);
                    nose.rotation.x = Math.PI / 2;
                    nose.position.set(0, 3.35, 0.68); obsGroup.add(nose);

                    for(let m = -1; m <= 1; m++) {
                        const mouthDot = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 8), coalMat);
                        mouthDot.position.set(m * 0.1, 3.16, 0.54); obsGroup.add(mouthDot);
                    }

                    const hatBrim = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.48, 0.08, 24), topHatMat);
                    hatBrim.position.y = 3.72; obsGroup.add(hatBrim);
                    const hatTop = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.42, 24), topHatMat);
                    hatTop.position.y = 3.96; obsGroup.add(hatTop);

                } else {
                    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(1.35), new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.8 }));
                    rock.position.y = 1.0; rock.castShadow = true; obsGroup.add(rock);
                }

                obsGroup.position.set(xPos, 0, zPos);
                scene.add(obsGroup);
                obstacles.push(obsGroup);
            } else {
                // Hộp quà phát sáng cao cấp
                const giftGroup = new THREE.Group();
                const box = new THREE.Mesh(new THREE.BoxGeometry(1.25, 1.25, 1.25), luxuryGiftMat);
                box.position.y = 0.62; box.castShadow = true; giftGroup.add(box);

                const ribbonV = new THREE.Mesh(new THREE.BoxGeometry(1.31, 1.31, 0.24), luxuryGoldRibbonMat);
                ribbonV.position.y = 0.62; giftGroup.add(ribbonV);

                const ribbonH = new THREE.Mesh(new THREE.BoxGeometry(0.24, 1.31, 1.31), luxuryGoldRibbonMat);
                ribbonH.position.y = 0.62; giftGroup.add(ribbonH);

                const bowTop = new THREE.Mesh(new THREE.SphereGeometry(0.3, 16, 16), luxuryGoldRibbonMat);
                bowTop.position.y = 1.34; giftGroup.add(bowTop);

                const giftLight = new THREE.PointLight(0xfacc15, 1.0, 5);
                giftLight.position.y = 0.8;
                giftGroup.add(giftLight);

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
            score = 0; distance = 0; speed = 0.38; currentLane = 1;
            santaGroup.position.set(lanes[1], 0, 0);

            obstacles.forEach(o => scene.remove(o));
            gifts.forEach(g => scene.remove(g));
            obstacles = []; gifts = [];
            gameRunning = true;
        }

        function restartGame() { startGame(); }

        setInterval(spawnEntities, 1000);

        // --- 9. VÒNG LẶP ANIMATION ---
        function animate() {
            requestAnimationFrame(animate);

            const pos = snowGeo.attributes.position.array;
            for(let i = 0; i < snowCount; i++) {
                pos[i*3 + 1] -= snowSpeeds[i].y;
                pos[i*3] += snowSpeeds[i].x;
                if(pos[i*3 + 1] < 0) pos[i*3 + 1] = 55;
            }
            snowGeo.attributes.position.needsUpdate = true;

            if (gameRunning) {
                distance += 0.85; speed += 0.00008;
                document.getElementById('distance').innerText = Math.floor(distance / 10);
                document.getElementById('score').innerText = score;

                const targetX = lanes[currentLane];
                santaGroup.position.x += (targetX - santaGroup.position.x) * 0.2;
                santaGroup.rotation.z = (santaGroup.position.x - targetX) * 0.03;

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

                    if (Math.abs(dx) < 1.3 && Math.abs(dz) < 1.4 && santaGroup.position.y < 1.2) {
                        gameRunning = false;
                        audio.stopBGM();
                        audio.crashBoomCinematic();
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
