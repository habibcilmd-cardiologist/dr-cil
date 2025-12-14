<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0px); }
        }
        
        @keyframes drift {
            0% { transform: translate(0, 0) rotate(0deg); opacity: 0.3; }
            50% { transform: translate(15px, -20px) rotate(5deg); opacity: 0.5; }
            100% { transform: translate(0, 0) rotate(0deg); opacity: 0.3; }
        }

        @keyframes drawLine {
            to { stroke-dashoffset: 0; }
        }

        .animate-float { animation: float 6s ease-in-out infinite; }
        .animate-drift { animation: drift 10s ease-in-out infinite; }
        
        .ecg-line {
            stroke-dasharray: 1000;
            stroke-dashoffset: 1000;
            animation: drawLine 4s linear infinite;
        }
        
        /* Glassmorphism */
        .glass-card {
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        }
        
        .glass-stat {
             background: rgba(255, 255, 255, 0.4);
             border: 1px solid rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 selection:bg-rose-100 selection:text-rose-600">

    <section class="relative w-full min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-blue-50 via-white to-red-50 pt-20 lg:pt-0">
        
        <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
            <svg class="absolute top-[20%] left-0 w-full h-40 opacity-10 text-rose-400" viewBox="0 0 1200 100" preserveAspectRatio="none">
                <path class="ecg-line" fill="none" stroke="currentColor" stroke-width="1.5" d="M0,50 L200,50 L220,20 L240,80 L260,50 L400,50 L420,10 L440,90 L460,50 L1200,50" />
            </svg>
            <div class="absolute top-10 right-10 w-64 h-64 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-drift"></div>
            <div class="absolute bottom-20 left-20 w-80 h-80 bg-rose-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-drift" style="animation-delay: 2s;"></div>
        </div>

        <div class="container mx-auto px-6 lg:px-12 relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            <div class="lg:col-span-7 flex flex-col justify-center text-center lg:text-left space-y-6">
                
                <div class="flex flex-wrap justify-center lg:justify-start gap-2">
                    <span class="px-3 py-1 rounded-full bg-blue-50 border border-blue-100 text-blue-700 text-xs font-semibold tracking-wide uppercase">
                        Girişimsel Kardiyoloji Uzmanı
                    </span>
                    <span class="px-3 py-1 rounded-full bg-rose-50 border border-rose-100 text-rose-700 text-xs font-semibold tracking-wide uppercase">
                        İstanbul
                    </span>
                </div>
                
                <h1 class="text-4xl lg:text-6xl font-bold leading-tight text-slate-900">
                    <span class="block text-2xl lg:text-3xl font-medium text-slate-500 mb-2">Doç. Dr.</span>
                    Habib ÇİL
                </h1>
                
                <h2 class="text-xl lg:text-2xl font-light text-slate-600">
                    Kalbinizin Ritmi <span class="text-blue-600 font-medium">Güvenli Ellerde</span>
                </h2>
                
                <p class="text-base text-slate-600 leading-relaxed max-w-2xl mx-auto lg:mx-0">
                    İstanbul Üniversitesi Cerrahpaşa Tıp Fakültesi mezunu, Akdeniz Üniversitesi Kardiyoloji ihtisası. 25 yılı aşkın klinik deneyim ve akademik kariyer ile hastalarına en güncel tanı ve tedavi yöntemlerini sunmaktadır.
                </p>

                <div class="grid grid-cols-3 gap-4 border-t border-b border-slate-200 py-6 my-4 glass-stat rounded-xl">
                    <div class="text-center lg:text-left px-4 border-r border-slate-200 last:border-0">
                        <span class="block text-2xl lg:text-3xl font-bold text-blue-600">25+</span>
                        <span class="text-xs text-slate-500 font-medium uppercase tracking-wider">Yıl Deneyim</span>
                    </div>
                    <div class="text-center lg:text-left px-4 border-r border-slate-200 last:border-0">
                        <span class="block text-2xl lg:text-3xl font-bold text-rose-500">20K+</span>
                        <span class="text-xs text-slate-500 font-medium uppercase tracking-wider">İnvaziv Girişim</span>
                    </div>
                    <div class="text-center lg:text-left px-4">
                        <span class="block text-2xl lg:text-3xl font-bold text-slate-700">100+</span>
                        <span class="text-xs text-slate-500 font-medium uppercase tracking-wider">Bilimsel Yayın</span>
                    </div>
                </div>

                <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start pt-2">
                    <a href="#" class="px-8 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg shadow-blue-500/20 transition-all transform hover:-translate-y-0.5">
                        Randevu Oluştur
                    </a>
                    <a href="#" class="px-8 py-3.5 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium rounded-lg shadow-sm transition-all flex items-center justify-center gap-2">
                        Tedavileri İncele
                    </a>
                </div>
            </div>

            <div class="lg:col-span-5 relative h-[500px] lg:h-[600px] flex items-end justify-center">
                
                <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[400px] bg-gradient-to-t from-blue-200 to-transparent rounded-full filter blur-[60px] opacity-40"></div>

                <img src="https://placehold.co/450x600/e2e8f0/475569?text=Doktor+PNG" alt="Doç. Dr. Habib ÇİL" class="relative z-10 w-auto h-full max-h-[550px] object-contain drop-shadow-2xl mask-image-bottom">

                <div class="absolute top-20 -left-6 lg:-left-12 z-20 glass-card p-4 rounded-xl animate-float shadow-lg max-w-[180px]">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-rose-100 flex items-center justify-center text-rose-600">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
                        </div>
                        <div>
                            <p class="text-[10px] text-slate-500 font-bold uppercase">Uzmanlık</p>
                            <p class="text-sm font-bold text-slate-800">Damar Açma</p>
                        </div>
                    </div>
                </div>

                <div class="absolute bottom-32 -right-4 lg:-right-8 z-20 glass-card p-4 rounded-xl animate-float shadow-lg max-w-[200px]" style="animation-delay: 2s;">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 14l9-5-9-5-9 5 9 5z" /><path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /></svg>
                        </div>
                        <div>
                            <p class="text-[10px] text-slate-500 font-bold uppercase">Kariyer</p>
                            <p class="text-sm font-bold text-slate-800">Akademik Yetkinlik</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

</body>
</html>