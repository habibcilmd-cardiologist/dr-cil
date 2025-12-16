<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doç. Dr. Habib ÇİL - İletişim Portalı</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Inter', 'sans-serif'] },
                    colors: {
                        'ios-red': '#FF3B30',
                        'ios-blue': '#007AFF',
                        'ios-green': '#34C759',
                        'ios-purple': '#AF52DE',
                        'glass-border': 'rgba(255, 255, 255, 0.4)',
                        'glass-bg': 'rgba(255, 255, 255, 0.65)',
                    },
                    animation: {
                        'blob': 'blob 7s infinite',
                        'ecg': 'ecgMove 3s linear infinite',
                        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                    },
                    keyframes: {
                        blob: {
                            '0%': { transform: 'translate(0px, 0px) scale(1)' },
                            '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
                            '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
                            '100%': { transform: 'translate(0px, 0px) scale(1)' },
                        },
                        ecgMove: {
                            '0%': { strokeDashoffset: '1000' },
                            '100%': { strokeDashoffset: '0' }
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #f2f2f7; /* Apple System Gray 6 */
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        }

        .glass-button {
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .glass-button:hover {
            background: rgba(255, 255, 255, 0.85);
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05), 0 0 0 1px rgba(255,255,255,0.8) inset;
        }

        /* EKG Çizgisi */
        .ecg-line {
            fill: none;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-dasharray: 1000; 
            filter: drop-shadow(0 0 2px rgba(255, 59, 48, 0.4));
        }

    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4 overflow-hidden relative selection:bg-ios-red selection:text-white">

    <div class="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-red-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div class="absolute top-[-10%] right-[-10%] w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div class="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
    </div>

    <div class="w-full max-w-md glass-card rounded-[32px] p-6 sm:p-8 flex flex-col items-center relative z-10 animate-[fadeIn_0.5s_ease-out]">
        
        <div class="text-center mb-8 w-full relative">
            <div class="w-16 h-16 bg-white rounded-2xl shadow-lg mx-auto mb-4 flex items-center justify-center relative overflow-hidden group">
                <div class="absolute inset-0 bg-gradient-to-tr from-red-50 to-white opacity-50"></div>
                <svg class="w-8 h-8 text-ios-red animate-pulse-slow relative z-10" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
            </div>
            
            <h1 class="text-2xl font-bold text-gray-900 tracking-tight">Doç. Dr. Habib ÇİL</h1>
            <p class="text-gray-500 font-medium text-sm mt-1 tracking-wide uppercase">Girişimsel Kardiyoloji Uzmanı</p>
            
            <div class="w-full h-8 mt-4 overflow-hidden relative opacity-60">
                <svg class="w-full h-full" viewBox="0 0 300 50" preserveAspectRatio="none">
                    <path class="ecg-line stroke-gray-300 animate-ecg" d="M0,25 L20,25 L30,40 L40,10 L50,45 L60,25 L100,25 L110,40 L120,10 L130,45 L140,25 L250,25 L260,40 L270,10 L280,45 L290,25 L300,25" />
                </svg>
                <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/0 to-white/0"></div> 
            </div>
        </div>

        <div class="w-full grid grid-cols-1 gap-4">

            <a href="https://www.doktorsitesi.com/doc-dr-habib-cil/kardiyoloji/istanbul" target="_blank" 
               class="glass-button group flex items-center p-4 rounded-2xl text-gray-800 no-underline relative overflow-hidden">
                <div class="w-12 h-12 rounded-xl bg-red-50 flex items-center justify-center shrink-0 group-hover:bg-ios-red transition-colors duration-300">
                   <svg class="w-6 h-6 text-ios-red group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                   </svg>
                </div>
                <div class="ml-4 flex-1">
                    <span class="block text-xs font-semibold text-ios-red opacity-80 mb-0.5">RANDEVU</span>
                    <span class="block text-lg font-bold tracking-tight">Doktor Sitesi</span>
                </div>
                <div class="opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0 transform duration-300">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </div>
            </a>

            <a href="https://www.doktortakvimi.com/habib-cil/kardiyoloji/istanbul" target="_blank" 
               class="glass-button group flex items-center p-4 rounded-2xl text-gray-800 no-underline relative overflow-hidden">
                <div class="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center shrink-0 group-hover:bg-ios-purple transition-colors duration-300">
                    <svg class="w-6 h-6 text-ios-purple group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                </div>
                <div class="ml-4 flex-1">
                    <span class="block text-xs font-semibold text-ios-purple opacity-80 mb-0.5">RANDEVU</span>
                    <span class="block text-lg font-bold tracking-tight">Doktor Takvimi</span>
                </div>
                <div class="opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0 transform duration-300">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </div>
            </a>

            <a href="tel:+902126655050" 
               class="glass-button group flex items-center p-4 rounded-2xl text-gray-800 no-underline relative overflow-hidden">
                <div class="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center shrink-0 group-hover:bg-ios-blue transition-colors duration-300">
                    <svg class="w-6 h-6 text-ios-blue group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                </div>
                <div class="ml-4 flex-1">
                    <span class="block text-xs font-semibold text-ios-blue opacity-80 mb-0.5">0212 665 50 50</span>
                    <span class="block text-lg font-bold tracking-tight">Ara (Dahili : 4012)</span>
                </div>
                <div class="absolute right-4 w-3 h-3 bg-green-400 rounded-full animate-ping opacity-20 group-hover:opacity-0 transition-opacity"></div>
            </a>

            <a href="https://api.whatsapp.com/send/?phone=905339454639&text&type=phone_number&app_absent=0" target="_blank" 
               class="glass-button group flex items-center p-4 rounded-2xl text-gray-800 no-underline relative overflow-hidden">
                <div class="w-12 h-12 rounded-xl bg-green-50 flex items-center justify-center shrink-0 group-hover:bg-ios-green transition-colors duration-300">
                    <svg class="w-6 h-6 text-ios-green group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                    </svg>
                </div>
                <div class="ml-4 flex-1">
                    <span class="block text-xs font-semibold text-ios-green opacity-80 mb-0.5">MESAJ AT - SORU SOR </span>
                    <span class="block text-lg font-bold tracking-tight">WhatsApp</span>
                </div>
                 <div class="opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0 transform duration-300">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </div>
            </a>

        </div>

        <div class="mt-8 text-center opacity-40">
            <p class="text-[10px] text-gray-600 font-medium">© 2025 Doç. Dr. Habib ÇİL</p>
        </div>

    </div>

</body>
</html>