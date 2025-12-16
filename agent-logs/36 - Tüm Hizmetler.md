<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Living Cardiology Interface</title>
    <style>
        :root {
            /* Renk Paleti */
            --bg-color: #f0f7ff;
            --card-bg: rgba(255, 255, 255, 0.95);
            --text-main: #334155;
            --text-light: #64748b;
            --soft-red: #ff8fa3; 
            --vessel-red: #ff6b81;
            --soft-blue: #8ecae6;
            --vessel-blue: #4dabf7;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            overflow-x: hidden;
            background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
            background-size: 30px 30px;
        }

        /* --- ANA SAHNE --- */
        .anatomy-stage {
            position: relative;
            max-width: 1300px;
            min-height: 100vh; 
            margin: 0 auto;
            padding: 60px 20px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 60px;
        }

        /* --- SVG DAMAR KATMANI --- */
        #vascular-system {
            position: absolute;
            top: 0; left: 0;
            width: 100%; 
            height: 100%;
            pointer-events: none;
            z-index: 1; 
            overflow: visible;
        }

        .vessel-path {
            fill: none;
            stroke-width: 5;
            stroke-linecap: round;
            opacity: 0.6;
            transition: opacity 0.3s;
        }

        .artery {
            stroke: var(--vessel-red);
            stroke-dasharray: 15, 10;
            animation: pulseFlow 3s linear infinite;
        }

        .vein {
            stroke: var(--vessel-blue);
            stroke-dasharray: 15, 10;
            animation: pulseFlow 4s linear infinite reverse;
        }

        @keyframes pulseFlow {
            to { stroke-dashoffset: -300; }
        }

        .active-connection {
            stroke-width: 8;
            opacity: 1;
            filter: drop-shadow(0 0 8px currentColor);
        }

        /* --- MERKEZİ KALP (STICKY) --- */
        .heart-hub {
            position: sticky;
            top: 100px;
            width: 300px;
            z-index: 5;
            flex-shrink: 0;
            display: flex;
            justify-content: center;
            height: fit-content;
        }

        .anatomical-heart {
            width: 100%;
            filter: sepia(0.2) hue-rotate(-10deg) saturate(1.1) drop-shadow(0 20px 40px rgba(255, 100, 100, 0.15));
            animation: heartbeat 6s infinite ease-in-out;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .anatomical-heart:hover { transform: scale(1.05); }

        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            5% { transform: scale(1.03); }
            10% { transform: scale(1); }
            15% { transform: scale(1.05); }
            50% { transform: scale(1); }
        }

        /* Ankrajlar */
        .anchor { position: absolute; width: 1px; height: 1px; visibility: hidden; }
        #anc-clinical { top: 65%; left: 30%; }
        #anc-rhythm { top: 25%; left: 35%; }
        #anc-structural { top: 20%; left: 55%; }
        /* Valve ankrajı kaldırıldı */
        #anc-coronary { top: 40%; left: 70%; }
        #anc-peripheral { top: 10%; left: 50%; }
        #anc-diagnostic { top: 85%; left: 50%; }

        /* --- SÜTUNLAR --- */
        .column {
            display: flex;
            flex-direction: column;
            gap: 25px;
            width: 340px;
            z-index: 10;
        }

        /* --- KART TASARIMI --- */
        .bio-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid #fff;
            border-radius: 18px;
            width: 100%;
            box-shadow: 0 5px 20px rgba(0,0,0,0.04);
            transition: box-shadow 0.3s, transform 0.3s, background 0.3s, border-color 0.3s;
            cursor: pointer;
            overflow: hidden;
            position: relative;
        }

        .bio-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.08);
            background: #fff;
        }

        .card-header {
            padding: 18px;
            display: flex;
            align-items: center;
            gap: 15px;
            position: relative;
            z-index: 2;
            background: rgba(255,255,255,0.4);
        }

        .icon-box {
            width: 44px; height: 44px;
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px;
            background: #f8fafc;
            transition: 0.3s;
        }

        .card-info h3 { margin: 0; font-size: 17px; color: var(--text-main); font-weight: 700; }
        .card-info p { margin: 3px 0 0; font-size: 12px; color: var(--text-light); }

        .toggle-icon { margin-left: auto; color: #cbd5e1; transition: transform 0.4s; }

        .card-body {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.6s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.4s;
            opacity: 0;
            background: #fff;
            border-top: 1px solid rgba(0,0,0,0.03);
        }

        .bio-card.active { border-color: currentColor; background: #fff; }
        .bio-card.active .card-body { max-height: 2000px; opacity: 1; }
        .bio-card.active .toggle-icon { transform: rotate(180deg); color: var(--text-main); }

        .theme-red { color: var(--vessel-red); }
        .theme-red .icon-box { color: var(--soft-red); background: #fff5f7; }
        .theme-blue { color: var(--vessel-blue); }
        .theme-blue .icon-box { color: var(--soft-blue); background: #f0fbff; }

        .sub-service-list {
            list-style: none;
            padding: 10px 15px 20px 15px;
            margin: 0;
        }
        .sub-service-item {
            display: flex; align-items: center; padding: 10px 12px;
            margin-bottom: 4px; border-radius: 8px;
            color: var(--text-main); text-decoration: none; font-size: 14px;
            transition: 0.2s; border-left: 3px solid transparent;
        }
        .sub-service-item:hover { background: #f1f5f9; transform: translateX(5px); }
        .item-icon { margin-right: 10px; font-size: 16px; min-width: 20px; text-align: center; }
        
        .theme-red .sub-service-item:hover { border-left-color: var(--vessel-red); color: var(--vessel-red); }
        .theme-blue .sub-service-item:hover { border-left-color: var(--vessel-blue); color: var(--vessel-blue); }

        .connection-point {
            position: absolute;
            top: 40px; 
            width: 8px; height: 8px;
            background: #fff;
            border: 2px solid #ccc;
            border-radius: 50%;
            z-index: 5;
            transition: background 0.3s;
        }
        .bio-card.active .connection-point { background: currentColor; border-color: currentColor; }

        .column-left .connection-point { right: -5px; border-color: var(--vessel-red); }
        .column-right .connection-point { left: -5px; border-color: var(--vessel-blue); }

        @media (max-width: 1024px) {
            .anatomy-stage { flex-direction: column; align-items: center; gap: 30px; padding: 30px 15px;}
            .heart-hub { position: relative; top: 0; width: 140px; margin-bottom: 10px; order: 1;}
            .column { width: 100%; gap: 15px; order: 2; }
            #vascular-system { display: none; }
            .connection-point { display: none; }
        }
    </style>
</head>
<body>

<div class="anatomy-stage">

    <svg id="vascular-system"></svg>

    <div class="column column-left">
        
        <div class="bio-card theme-red" id="card-clinical">
            <div class="connection-point"></div>
            <div class="card-header">
                <div class="icon-box">🫀</div>
                <div class="card-info"><h3>Klinik Kardiyoloji</h3><p>Tanı, Takip ve Korunma</p></div>
                <div class="toggle-icon">▼</div>
            </div>
            <div class="card-body">
                <ul class="sub-service-list">
                    <li><a href="/tr/hizmetler/hipertansiyon/" class="sub-service-item"><span class="item-icon">📈</span>Hipertansiyon</a></li>
                    <li><a href="/tr/hizmetler/hiperlipidemi-tedavisi/" class="sub-service-item"><span class="item-icon">🩸</span>Hiperlipidemi Tedavisi</a></li>
                    <li><a href="/tr/hizmetler/kardiyovaskuler-korunma/" class="sub-service-item"><span class="item-icon">🛡️</span>Kardiyovasküler Korunma</a></li>
                    <li><a href="/tr/hizmetler/kalp-yetmezligi/" class="sub-service-item"><span class="item-icon">💗</span>Kalp Yetersizliği</a></li>
                </ul>
            </div>
        </div>

        <div class="bio-card theme-red" id="card-rhythm">
            <div class="connection-point"></div>
            <div class="card-header">
                <div class="icon-box">⚡</div>
                <div class="card-info"><h3>Kalp Pili & Elektrofizyoloji</h3><p>Elektrofizyoloji & Ablasyon</p></div>
                <div class="toggle-icon">▼</div>
            </div>
            <div class="card-body">
                <ul class="sub-service-list">
                    <li><a href="/tr/hizmetler/uc-odacikli-kalp-pili/" class="sub-service-item"><span class="item-icon">🔋</span>Üç Odacıklı Kalp Pili</a></li>
                    <li><a href="/tr/hizmetler/kalici-kalp-pili/" class="sub-service-item"><span class="item-icon">⚡</span>Kalıcı Kalp Pili</a></li>
                    <li><a href="/tr/hizmetler/gecici-kalp-pili/" class="sub-service-item"><span class="item-icon">🔌</span>Geçici Kalp Pili</a></li>
                    <li><a href="/tr/hizmetler/biventrikuler-pacemaker/" class="sub-service-item"><span class="item-icon">💫</span>Biventriküler Pacemaker</a></li>
                    <li><a href="/tr/hizmetler/icd/" class="sub-service-item"><span class="item-icon">🛡️</span>ICD (Şok Pili)</a></li>
                    <li><a href="/tr/hizmetler/ablasyon/" class="sub-service-item"><span class="item-icon">⚡</span>Ablasyon</a></li>
                    <li><a href="/tr/hizmetler/elektrofizyolojik-test/" class="sub-service-item"><span class="item-icon">🔬</span>Elektrofizyolojik Test</a></li>
                    <li><a href="/tr/hizmetler/kardiyoversiyon/" class="sub-service-item"><span class="item-icon">💥</span>Kardiyoversiyon</a></li>
                </ul>
            </div>
        </div>

        <div class="bio-card theme-red" id="card-structural">
            <div class="connection-point"></div>
            <div class="card-header">
                <div class="icon-box">🔄</div>
                <div class="card-info"><h3>Yapısal Girişimler</h3><p>Kapak Tamiri & Delik Kapatma</p></div>
                <div class="toggle-icon">▼</div>
            </div>
            <div class="card-body">
                <ul class="sub-service-list">
                    <li><a href="/tr/hizmetler/tavi/" class="sub-service-item"><span class="item-icon">🔄</span>TAVI (Aort Kapak)</a></li>
                    <li><a href="/tr/hizmetler/mitraclip/" class="sub-service-item"><span class="item-icon">📎</span>MitraClip</a></li>
                    <li><a href="/tr/hizmetler/mitral-kapak/" class="sub-service-item"><span class="item-icon">🎈</span>Mitral Balon Valvüloplasti</a></li>
                    <li><a href="/tr/hizmetler/trikuspid-kapak-yerlestirilmesi/" class="sub-service-item"><span class="item-icon">💚</span>Triküspid Kapak Yerleştirilmesi</a></li>
                    <li><a href="/tr/hizmetler/pulmoner-kapak-yerlestirilmesi/" class="sub-service-item"><span class="item-icon">🔧</span>Pulmoner Kapak Yerleştirilmesi</a></li>
                    <li><a href="/tr/hizmetler/alkol-septal-ablasyon/" class="sub-service-item"><span class="item-icon">🧪</span>Alkol Septal Ablasyon</a></li>
                    <li><a href="/tr/hizmetler/kalp-deligi-kapatma/" class="sub-service-item"><span class="item-icon">🧱</span>Kalp Deliği Kapatma (ASD/PFO)</a></li>
                </ul>
            </div>
        </div>

    </div>

    <div class="heart-hub">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/cc/Diagram_of_the_human_heart_%28no_labels%29.svg" 
             class="anatomical-heart" alt="Anatomical Heart">
        <div class="anchor" id="anc-clinical"></div>
        <div class="anchor" id="anc-rhythm"></div>
        <div class="anchor" id="anc-structural"></div>
        <div class="anchor" id="anc-coronary"></div>
        <div class="anchor" id="anc-peripheral"></div>
        <div class="anchor" id="anc-diagnostic"></div>
    </div>

    <div class="column column-right">
        
        <div class="bio-card theme-blue" id="card-coronary">
            <div class="connection-point"></div>
            <div class="card-header">
                <div class="icon-box">🔧</div>
                <div class="card-info"><h3>Koroner Girişimler</h3><p>Stent, CTO & Anjiyoplasti</p></div>
                <div class="toggle-icon">▼</div>
            </div>
            <div class="card-body">
                <ul class="sub-service-list">
                    <li><a href="/tr/hizmetler/sol-ana-koroner-stent/" class="sub-service-item"><span class="item-icon">⭐</span>Sol Ana Koroner Girişim</a></li>
                    <li><a href="/tr/hizmetler/bifurkasyon-girisimi/" class="sub-service-item"><span class="item-icon">🔀</span>Bifurkasyon Girişimleri</a></li>
                    <li><a href="/tr/hizmetler/cto-girisimi/" class="sub-service-item"><span class="item-icon">🎯</span>Kronik Total Oklüzyon</a></li>
                    <li><a href="/tr/hizmetler/koroner-fistul-tedavisi/" class="sub-service-item"><span class="item-icon">🔗</span>Koroner Fistül Tedavisi</a></li>
                    <li><a href="/tr/hizmetler/ivus/" class="sub-service-item"><span class="item-icon">🔬</span>IVUS Görüntüleme</a></li>
                    <li><a href="/tr/hizmetler/ffr/" class="sub-service-item"><span class="item-icon">📊</span>FFR Ölçümü</a></li>
                    <li><a href="/tr/hizmetler/koroner-anjiyoplasti/" class="sub-service-item"><span class="item-icon">💉</span>Koroner Anjiyoplasti ve Stentleme</a></li>
                    <li><a href="/tr/hizmetler/miyokard-enfarktusu/" class="sub-service-item"><span class="item-icon">💔</span>Miyokard Enfarktüsü Tedavisi</a></li>
                </ul>
            </div>
        </div>

        <div class="bio-card theme-blue" id="card-peripheral">
            <div class="connection-point"></div>
            <div class="card-header">
                <div class="icon-box">🦵</div>
                <div class="card-info"><h3>Periferik Girişimler</h3><p>Şahdamarı, Bacak & Varis</p></div>
                <div class="toggle-icon">▼</div>
            </div>
            <div class="card-body">
                <ul class="sub-service-list">
                    <li><a href="/tr/hizmetler/karotis-stenozu/" class="sub-service-item"><span class="item-icon">🧠</span>Karotis Stentleme</a></li>
                    <li><a href="/tr/hizmetler/renal-arter-stenozu/" class="sub-service-item"><span class="item-icon">🫘</span>Renal Arter Darlığı</a></li>
                    <li><a href="/tr/hizmetler/periferik-damar/" class="sub-service-item"><span class="item-icon">🦵</span>Periferik Damar Girişimi</a></li>
                    <li><a href="/tr/hizmetler/dizustu-damar-tikanikligi/" class="sub-service-item"><span class="item-icon">🦵</span>Dizüstü Damar Tıkanıklığı</a></li>
                    <li><a href="/tr/hizmetler/dizalti-damar-tikanikligi/" class="sub-service-item"><span class="item-icon">🦶</span>Dizaltı Damar Tıkanıklığı</a></li>
                    <li><a href="/tr/hizmetler/iliak-arter-tedavisi/" class="sub-service-item"><span class="item-icon">🛣️</span>İliak Arter Tedavisi</a></li>
                    <li><a href="/tr/hizmetler/evar-tevar/" class="sub-service-item"><span class="item-icon">🔧</span>EVAR - TEVAR</a></li>
                    <li><a href="/tr/hizmetler/aterektomi/" class="sub-service-item"><span class="item-icon">🎯</span>Periferik ve Koroner Aterektomi</a></li>
                    <li><a href="/tr/hizmetler/diyaliz-fistul-tedavisi/" class="sub-service-item"><span class="item-icon">💉</span>Diyaliz Fistül Tedavisi</a></li>
                    <li><a href="/tr/hizmetler/akut-dvt-tedavisi/" class="sub-service-item"><span class="item-icon">🛑</span>Akut DVT Tedavisi</a></li>
                    <li><a href="/tr/hizmetler/kronik-dvt-tedavisi/" class="sub-service-item"><span class="item-icon">🕰️</span>Kronik DVT Tedavisi</a></li>
                    <li><a href="/tr/hizmetler/may-thurner/" class="sub-service-item"><span class="item-icon">🩺</span>May-Thurner Sendromu</a></li>
                    <li><a href="/tr/hizmetler/varikosel-pelvik-konjesyon/" class="sub-service-item"><span class="item-icon">🚺</span>Varikosel ve Pelvik Konjesyon</a></li>
                </ul>
            </div>
        </div>

        <div class="bio-card theme-blue" id="card-diagnostic">
            <div class="connection-point"></div>
            <div class="card-header">
                <div class="icon-box">🩺</div>
                <div class="card-info"><h3>Tanısal İşlemler</h3><p>Anjiyo, Eko & Testler</p></div>
                <div class="toggle-icon">▼</div>
            </div>
            <div class="card-body">
                <ul class="sub-service-list">
                    <li><a href="/tr/hizmetler/kardiyak-anjiyografi/" class="sub-service-item"><span class="item-icon">❤️</span>Kardiyak Anjiyografi</a></li>
                    <li><a href="/tr/hizmetler/periferik-anjiyografi/" class="sub-service-item"><span class="item-icon">🦵</span>Periferik Anjiyografi</a></li>
                    <li><a href="/tr/hizmetler/ekokardiyografi/" class="sub-service-item"><span class="item-icon">🔊</span>Ekokardiyografi</a></li>
                    <li><a href="/tr/hizmetler/efor-testi/" class="sub-service-item"><span class="item-icon">🏃</span>Efor Testi</a></li>
                    <li><a href="/tr/hizmetler/ekg/" class="sub-service-item"><span class="item-icon">📉</span>EKG</a></li>
                    <li><a href="/tr/hizmetler/transtorasik-ekokardiyografi/" class="sub-service-item"><span class="item-icon">🖥️</span>Transtorasik Ekokardiyografi (TTE)</a></li>
                    <li><a href="/tr/hizmetler/transozofageal-ekokardiyografi/" class="sub-service-item"><span class="item-icon">🩺</span>Transözofageal Ekokardiyografi (TÖE)</a></li>
                    <li><a href="/tr/hizmetler/holter/" class="sub-service-item"><span class="item-icon">📡</span>Ritm Holter</a></li>
                    <li><a href="/tr/hizmetler/tansiyon-holter/" class="sub-service-item"><span class="item-icon">📏</span>Tansiyon Holter</a></li>
                    <li><a href="/tr/hizmetler/stres-ekokardiyografi/" class="sub-service-item"><span class="item-icon">💓</span>Stres Ekokardiyografi</a></li>
                    <li><a href="/tr/hizmetler/miyokard-perfuzyon/" class="sub-service-item"><span class="item-icon">🧲</span>Miyokard Perfüzyon</a></li>
                    <li><a href="/tr/hizmetler/radyal-anjiyografi/" class="sub-service-item"><span class="item-icon">🔎</span>Radyal Anjiyografi</a></li>
                    <li><a href="/tr/hizmetler/kardiyak-bt/" class="sub-service-item"><span class="item-icon">💻</span>Koroner BT Anjiyografi</a></li>
                    <li><a href="/tr/hizmetler/tilt-testi/" class="sub-service-item"><span class="item-icon">🧬</span>Tilt Testi</a></li>
                </ul>
            </div>
        </div>

    </div>

</div>

<script>
    // 1. DAMAR ÇİZME VE HESAPLAMA
    function drawVessel(svgId, anchorId, cardId, type) {
        const svg = document.getElementById(svgId);
        const anchor = document.getElementById(anchorId);
        const card = document.getElementById(cardId);
        
        if (!anchor || !card) return;

        const connectPoint = card.querySelector('.connection-point');
        if (!connectPoint) return;

        // Koordinatları Al (Sayfaya göre değil, SVG konteynerine göre)
        const svgRect = svg.getBoundingClientRect();
        const anchorRect = anchor.getBoundingClientRect();
        const pointRect = connectPoint.getBoundingClientRect();

        // SVG sol üst köşesine göre göreceli pozisyonlar
        const x1 = anchorRect.left - svgRect.left;
        const y1 = anchorRect.top - svgRect.top;
        const x2 = pointRect.left + pointRect.width/2 - svgRect.left;
        const y2 = pointRect.top + pointRect.height/2 - svgRect.top;

        // Kontrol Noktaları (Organik Kavis)
        const cp1x = x1 + (x2 - x1) * 0.5;
        const cp1y = y1;
        const cp2x = x2 - (x2 - x1) * 0.2;
        const cp2y = y2;

        const d = `M ${x1} ${y1} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${x2} ${y2}`;

        // Path Oluştur/Güncelle
        let path = document.getElementById(`path-${cardId}`);
        if (!path) {
            path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.id = `path-${cardId}`;
            path.classList.add('vessel-path', type);
            svg.appendChild(path);
        }
        path.setAttribute("d", d);

        // Aktiflik Durumu
        if(card.classList.contains('active')) {
            path.classList.add('active-connection');
        } else {
            path.classList.remove('active-connection');
        }
    }

    // 2. TÜM BAĞLANTILARI GÜNCELLE
    function updateAllConnections() {
        if (window.innerWidth <= 1024) return; // Mobilde çizme

        // Sol Sütun
        drawVessel('vascular-system', 'anc-clinical', 'card-clinical', 'artery');
        drawVessel('vascular-system', 'anc-rhythm', 'card-rhythm', 'artery');
        drawVessel('vascular-system', 'anc-structural', 'card-structural', 'artery');

        // Sağ Sütun
        drawVessel('vascular-system', 'anc-coronary', 'card-coronary', 'vein');
        drawVessel('vascular-system', 'anc-peripheral', 'card-peripheral', 'vein');
        drawVessel('vascular-system', 'anc-diagnostic', 'card-diagnostic', 'vein');
    }

    // 3. TIKLAMA VE ANIMASYON SENKRONİZASYONU
    document.querySelectorAll('.bio-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Linke tıklandıysa kartı kapatma
            if(e.target.closest('a')) return;

            // Kartı aç/kapat
            this.classList.toggle('active');

            // CSS transition (0.6s) boyunca her karede (frame) çizgiyi yeniden çiz.
            let startTime = performance.now();
            const duration = 700; 

            function animate(currentTime) {
                const elapsed = currentTime - startTime;
                updateAllConnections();

                if (elapsed < duration) {
                    requestAnimationFrame(animate);
                }
            }
            requestAnimationFrame(animate);
        });
    });

    // 4. BAŞLATMA
    window.addEventListener('load', updateAllConnections);
    window.addEventListener('resize', updateAllConnections);
    window.addEventListener('scroll', updateAllConnections); 
    
    setTimeout(updateAllConnections, 100);

</script>

</body>
</html>