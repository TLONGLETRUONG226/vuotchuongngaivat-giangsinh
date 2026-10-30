import streamlit as st
import streamlit.components.v1 as components

# Cấu hình giao diện Streamlit rộng toàn màn hình
st.set_page_config(
    page_title="Santa's Christmas Dash 2.5D",
    page_icon="🎅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn header và footer mặc định của Streamlit để game hiển thị trọn vẹn
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

# Mã nguồn HTML / JS hoàn chỉnh của game 2.5D Noel
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Santa's Christmas Dash 2.5D</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #0b1d3a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
        }
        #canvas-container {
            width: 100vw;
            height: 100vh;
            display: block;
        }
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
            box-sizing: border-box;
        }
        .hud-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }
        .score-box {
            background: rgba(0, 0, 0, 0.4);
            padding: 10px 20px;
            border-radius: 12px;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        #start-screen, #gameover-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(11, 29, 58, 0.85);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            pointer-events: auto;
            color: white;
            text-align: center;
            transition: opacity 0.3s ease;
        }
        h1 {
            font-size: 48px;
            color: #ff4757;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(255, 71, 87, 0.6);
        }
        p {
            font-size: 18px;
            color: #dfe4ea;
            max-width: 500px;
            line-height: 1.5;
            margin-bottom: 30px; ông
        }
        .btn {
            background: linear-gradient(135deg, #ff4757, #ff6b81);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 22px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(255, 71, 87, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
            pointer-events: auto;
        }
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 25px rgba(255, 71, 87, 0.6);
        }
        .btn:active {
            transform: scale(0.95);
        }
        #mobile-controls {
            display: none;
            position: absolute;
            bottom: 30px;
            width: 100%;
            justify-content: space-around;
            pointer-events: auto;
        }
        .control-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid white;
            color: white;
            font-size: 30px;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            backdrop-filter: blur(5px);
        }
        @media (max-width: 768px) {
            #mobile-controls { display: flex; }
        }
    </style>
    <!-- Nhúng thư viện Three.js từ CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="canvas-container"></div>

    <div id="ui-layer">
        <div class="hud-panel">
            <div class="score-box">🎁 Quà: <span id="score">0</span></div>
            <div class="score-box">⭐ Điểm: <span id="distance">0</span></div>
        </div>
    </div>

    <!-- Màn hình bắt đầu -->
    <div id="start-screen">
        <h1>🎅 Santa's Christmas Dash</h1>
        <p>Giúp ông già Noel nhảy qua những cây thông và người tuyết để phát quà kịp đêm Giáng Sinh!<br><b>Cách chơi:</b> Dùng phím <b>Mũi tên Trái / Phải</b> (hoặc nút bấm trên màn hình) để đổi làn đường, <b>Phím Cách (Space) / Mũi tên Lên</b> để nhảy.</p>
        <button class="btn" onclick="startGame()">BẮT ĐẦU CHƠI</button>
    </div>

    <!-- Màn hình Game Over -->
    <div id="gameover-screen" style="display: none;">
        <h1>💥 ÔI KHÔNG! TÔNG TRÚNG RỒI!</h1>
        <p>Ông già Noel bị ngã cú đau quá, quà rơi tung tóe khắp nơi mất tiêu! 🦌<br>Tổng quà thu thập: <span id="final-score">0</span></p>
        <button class="btn" onclick="restartGame()">CHƠI LẠI NGAY</button>
    </div>

    <div id="mobile-controls">
        <div class="control-btn" ontouchstart="moveLane(-1)">⬅️</div>
        <div class="control-btn" ontouchstart="jump()">⬆️</div>
        <div class="control-btn" ontouchstart="moveLane(1)">➡️</div>
    </div>

    <script>
        // --- KHỞI TẠO GAME THREE.JS 2.5D ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0b1d3a);
        scene.fog = new THREE.FogExp2(0x0b1d3a, 0.015);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 7, 14);
        camera.lookAt(0, 1, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        // Ánh sáng môi trường
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(10, 20, 10);
        dirLight.castShadow = true;
        scene.add(dirLight);

        // Biến trạng thái game
        let gameRunning = false;
        let score = 0;
        let distance = 0;
        let gameSpeed = 0.25;
        let lanes = [-2.5, 0, 2.5];
        let currentLaneIndex = 1;

        // Tạo mặt đường tuyết chạy dài
        const roadGeometry = new THREE.PlaneGeometry(10, 200);
        const roadMaterial = new THREE.MeshStandardMaterial({ color: 0xe0f7fa, roughness: 0.9 });
        const road = new THREE.Mesh(roadGeometry, roadMaterial);
        road.rotation.x = -Math.PI / 2;
        road.receiveShadow = true;
        scene.add(road);

        // Tạo ông già Noel (Santa Character đơn giản bằng khối hình học 2.5D)
        const santaGroup = new THREE.Group();
        
        // Thân đỏ
        const bodyGeo = new THREE.BoxGeometry(0.8, 1, 0.6);
        const bodyMat = new THREE.MeshStandardMaterial({ color: 0xd63031 });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.position.y = 0.8;
        body.castShadow = true;
        santaGroup.add(body);

        // Đầu & Râu
        const headGeo = new THREE.SphereGeometry(0.4, 16, 16);
        const headMat = new THREE.MeshStandardMaterial({ color: 0xffdab9 });
        const head = new THREE.Mesh(headGeo, headMat);
        head.position.y = 1.5;
        santaGroup.add(head);

        const beardGeo = new THREE.BoxGeometry(0.5, 0.3, 0.4);
        const beardMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
        const beard = new THREE.Mesh(beardGeo, beardMat);
        beard.position.set(0, 1.35, 0.25);
        santaGroup.add(beard);

        scene.add(santaGroup);
        santaGroup.position.x = lanes[currentLaneIndex];

        // Biến vật lý nhảy
        let isJumping = false;
        let jumpVelocity = 0;
        const gravity = 0.015;

        // Quản lý vật cản và quà tặng
        let obstacles = [];
        let gifts = [];

        function spawnObstacleOrGift() {
            if (!gameRunning) return;
            
            const lane = lanes[Math.floor(Math.random() * lanes.length)];
            const zPos = -100;

            if (Math.random() > 0.4) {
                // Tạo cây thông Noel (Vật cản)
                const treeGroup = new THREE.Group();
                const trunkMat = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
                const leavesMat = new THREE.MeshStandardMaterial({ color: 0x27ae60 });

                const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.8), trunkMat);
                trunk.position.y = 0.4;
                treeGroup.add(trunk);

                const leaves = new THREE.Mesh(new THREE.ConeGeometry(1, 2, 6), leavesMat);
                leaves.position.y = 1.6;
                treeGroup.add(leaves);

                treeGroup.position.set(lane, 0, zPos);
                scene.add(treeGroup);
                obstacles.push(treeGroup);
            } else {
                // Tạo hộp quà
                const giftGeo = new THREE.BoxGeometry(0.6, 0.6, 0.6);
                const giftMat = new THREE.MeshStandardMaterial({ color: 0xf1c40f });
                const gift = new THREE.Mesh(giftGeo, giftMat);
                gift.position.set(lane, 0.5, zPos);
                scene.add(gift);
                gifts.push(gift);
            }
        }

        // Tạo hiệu ứng tuyết rơi
        const snowflakesCount = 300;
        const snowGeo = new THREE.BufferGeometry();
        const snowPositions = new Float32Array(snowflakesCount * 3);

        for(let i=0; i<snowflakesCount*3; i+=3) {
            snowPositions[i] = (Math.random() - 0.5) * 40;
            snowPositions[i+1] = Math.random() * 30;
            snowPositions[i+2] = (Math.random() - 0.5) * 100;
        }
        snowGeo.setAttribute('position', new THREE.BufferAttribute(snowPositions, 3));
        const snowMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.2, transparent: true, opacity: 0.8 });
        const snowSystem = new THREE.Points(snowGeo, snowMat);
        scene.add(snowSystem);

        // Điều khiển phím
        window.addEventListener('keydown', (e) => {
            if (!gameRunning) return;
            if (e.key === 'ArrowLeft' || e.key === 'a') moveLane(-1);
            if (e.key === 'ArrowRight' || e.key === 'd') moveLane(1);
            if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'w') jump();
        });

        function moveLane(direction) {
            currentLaneIndex += direction;
            if (currentLaneIndex < 0) currentLaneIndex = 0;
            if (currentLaneIndex > 2) currentLaneIndex = 2;
        }

        function jump() {
            if (!isJumping) {
                isJumping = true;
                jumpVelocity = 0.25;
            }
        }

        function startGame() {
            document.getElementById('start-screen').style.display = 'none';
            score = 0;
            distance = 0;
            gameSpeed = 0.25;
            currentLaneIndex = 1;
            obstacles.forEach(obs => scene.remove(obs));
            gifts.forEach(g => scene.remove(g));
            obstacles = [];
            gifts = [];
            gameRunning = true;
        }

        function restartGame() {
            document.getElementById('gameover-screen').style.display = 'none';
            startGame();
        }

        // Spawn định kỳ vật cản
        setInterval(() => {
            if (gameRunning) spawnObstacleOrGift();
        }, 1200);

        // Vòng lặp Animation chính
        function animate() {
            requestAnimationFrame(animate);

            if (gameRunning) {
                distance += 1;
                gameSpeed += 0.0001; // Tăng tốc dần theo thời gian
                document.getElementById('distance').innerText = Math.floor(distance / 10);
                document.getElementById('score').innerText = score;

                // Di chuyển vị trí Santa mượt mà sang làn đường
                let targetX = lanes[currentLaneIndex];
                santaGroup.position.x += (targetX - santaGroup.position.x) * 0.2;

                // Xử lý nhảy
                if (isJumping) {
                    santaGroup.position.y += jumpVelocity;
                    jumpVelocity -= gravity;
                    if (santaGroup.position.y <= 0) {
                        santaGroup.position.y = 0;
                        isJumping = false;
                    }
                }

                // Cập nhật tuyết rơi
                const positions = snowGeo.attributes.position.array;
                for(let i=1; i<positions.length; i+=3) {
                    positions[i] -= 0.1;
                    if (positions[i] < 0) positions[i] = 30;
                }
                snowGeo.attributes.position.needsUpdate = true;

                // Xử lý vật cản
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    obstacles[i].position.z += gameSpeed;

                    // Kiểm tra va chạm với Santa
                    let dx = santaGroup.position.x - obstacles[i].position.x;
                    let dz = santaGroup.position.z - obstacles[i].position.z;
                    if (Math.abs(dx) < 0.8 && Math.abs(dz) < 0.8 && santaGroup.position.y < 1.2) {
                        gameRunning = false;
                        document.getElementById('final-score').innerText = score;
                        document.getElementById('gameover-screen').style.display = 'flex';
                    }

                    if (obstacles[i].position.z > 10) {
                        scene.remove(obstacles[i]);
                        obstacles.splice(i, 1);
                    }
                }

                // Xử lý hộp quà
                for (let i = gifts.length - 1; i >= 0; i--) {
                    gifts[i].position.z += gameSpeed;
                    gifts[i].rotation.y += 0.05;

                    let dx = santaGroup.position.x - gifts[i].position.x;
                    let dz = santaGroup.position.z - gifts[i].position.z;
                    if (Math.abs(dx) < 0.8 && Math.abs(dz) < 1.0) {
                        score += 10;
                        scene.remove(gifts[i]);
                        gifts.splice(i, 1);
                    } else if (gifts[i].position.z > 10) {
                        scene.remove(gifts[i]);
                        gifts.splice(i, 1);
                    }
                }
            }

            renderer.render(scene, camera);
        }

        animate();

        // Xử lý thay đổi kích thước màn hình
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

# Hiển thị game trong Streamlit
components.html(game_html, height=750, scrolling=False)
