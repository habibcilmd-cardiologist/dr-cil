<svg viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#e3f2fd;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#bbdefb;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="skinGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ffd7ba;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#ffb88c;stop-opacity:0.9" />
    </linearGradient>
    
    <linearGradient id="arteryHealthy" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ff9a9e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ff6b9d;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="arteryInner" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ffe0e6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ffc4d0;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="plaqueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#d4a574;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#b8935f;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="catheterGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2196f3;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#03a9f4;stop-opacity:1" />
    </linearGradient>
    
    <linearGradient id="balloonGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ffd54f;stop-opacity:0.95" />
      <stop offset="100%" style="stop-color:#ffb300;stop-opacity:0.95" />
    </linearGradient>
    
    <radialGradient id="pulseGrad">
      <stop offset="0%" style="stop-color:#4caf50;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#81c784;stop-opacity:0" />
    </radialGradient>

    <!-- Filters -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <filter id="softShadow">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.2"/>
    </filter>

    <!-- Clip paths -->
    <clipPath id="arteryFlowClip">
      <rect x="300" y="280" width="350" height="80" rx="40"/>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect width="900" height="700" fill="url(#bgGrad)"/>
  
  <!-- Decorative medical elements -->
  <g opacity="0.15">
    <circle cx="100" cy="100" r="40" fill="none" stroke="#2196f3" stroke-width="2"/>
    <circle cx="800" cy="600" r="50" fill="none" stroke="#2196f3" stroke-width="2"/>
    <path d="M 750,100 L 770,120 L 750,140" fill="none" stroke="#4caf50" stroke-width="3" stroke-linecap="round"/>
  </g>

  <!-- LEG ANATOMY -->
  <!-- Upper leg (thigh) -->
  <ellipse cx="450" cy="250" rx="120" ry="180" fill="url(#skinGrad)" opacity="0.4" filter="url(#softShadow)"/>
  
  <!-- Lower leg (calf) -->
  <ellipse cx="450" cy="500" rx="90" ry="150" fill="url(#skinGrad)" opacity="0.4" filter="url(#softShadow)"/>
  
  <!-- Leg outline to show anatomy -->
  <path d="M 330,100 Q 320,250 360,400 Q 370,500 380,650" 
        fill="none" stroke="#ffb88c" stroke-width="3" opacity="0.6"/>
  <path d="M 570,100 Q 580,250 540,400 Q 530,500 520,650" 
        fill="none" stroke="#ffb88c" stroke-width="3" opacity="0.6"/>

  <!-- Knee indication -->
  <ellipse cx="450" cy="400" rx="95" ry="30" fill="#ffc4a3" opacity="0.3"/>
  
  <!-- ARTERY SYSTEM -->
  <!-- Main femoral artery - upper segment (healthy) -->
  <rect x="410" y="120" width="80" height="140" rx="40" fill="url(#arteryHealthy)" opacity="0.8"/>
  <rect x="420" y="130" width="60" height="120" rx="30" fill="url(#arteryInner)"/>
  
  <!-- Problem area - stenosis region -->
  <g id="stenosisRegion">
    <!-- Outer artery wall -->
    <rect x="300" y="270" width="350" height="100" rx="50" fill="url(#arteryHealthy)" opacity="0.8" filter="url(#softShadow)"/>
    
    <!-- Inner lumen - BEFORE treatment (narrow) -->
    <rect id="narrowLumen" x="310" y="280" width="330" height="80" rx="40" fill="url(#arteryInner)">
      <animate attributeName="height" values="80;80;80;80;80;80" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="y" values="280;280;280;280;280;280" dur="8s" repeatCount="indefinite"/>
    </rect>
    
    <!-- Plaque buildup - TOP -->
    <ellipse cx="470" cy="295" rx="90" ry="25" fill="url(#plaqueGrad)" opacity="1">
      <animate attributeName="ry" values="25;25;25;25;8;8" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="295;295;295;295;285;285" dur="8s" repeatCount="indefinite"/>
    </ellipse>
    
    <!-- Plaque buildup - BOTTOM -->
    <ellipse cx="470" cy="345" rx="90" ry="25" fill="url(#plaqueGrad)" opacity="1">
      <animate attributeName="ry" values="25;25;25;25;8;8" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="345;345;345;345;355;355" dur="8s" repeatCount="indefinite"/>
    </ellipse>
    
    <!-- Plaque texture details -->
    <g opacity="0.6">
      <circle cx="440" cy="298" r="4" fill="#a07850"/>
      <circle cx="480" cy="302" r="3" fill="#a07850"/>
      <circle cx="460" cy="342" r="3.5" fill="#a07850"/>
      <circle cx="490" cy="345" r="4" fill="#a07850"/>
    </g>
  </g>

  <!-- Lower segment (healthy) -->
  <rect x="410" y="380" width="80" height="270" rx="40" fill="url(#arteryHealthy)" opacity="0.8"/>
  <rect x="420" y="390" width="60" height="250" rx="30" fill="url(#arteryInner)"/>

  <!-- BLOOD FLOW - BEFORE (slow, restricted) -->
  <g clip-path="url(#arteryFlowClip)">
    <circle r="5" fill="#e53935">
      <animateMotion dur="5s" repeatCount="indefinite" 
                     path="M 310,310 Q 400,310 460,320"/>
      <animate attributeName="opacity" values="0.8;0.8;0.8;0.8;0;0" dur="8s" repeatCount="indefinite"/>
    </circle>
    <circle r="4" fill="#ef5350">
      <animateMotion dur="5.5s" repeatCount="indefinite" 
                     path="M 310,330 Q 400,328 460,330"/>
      <animate attributeName="opacity" values="0.8;0.8;0.8;0.8;0;0" dur="8s" repeatCount="indefinite"/>
    </circle>
    <circle r="4.5" fill="#e53935">
      <animateMotion dur="6s" repeatCount="indefinite" begin="0.5s"
                     path="M 310,320 Q 400,318 460,325"/>
      <animate attributeName="opacity" values="0.8;0.8;0.8;0.8;0;0" dur="8s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- CATHETER AND INTERVENTION -->
  <g id="catheterSystem">
    <!-- Guide wire -->
    <line x1="200" y1="320" x2="200" y2="320" stroke="#ffc107" stroke-width="2.5" opacity="0.9">
      <animate attributeName="x2" values="200;200;500;500;500;500" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="y2" values="320;320;320;320;320;320" dur="8s" repeatCount="indefinite"/>
    </line>
    
    <!-- Catheter body -->
    <rect x="200" y="312" width="0" height="16" rx="8" fill="url(#catheterGrad)" filter="url(#glow)">
      <animate attributeName="width" values="0;0;280;280;280;280" dur="8s" repeatCount="indefinite"/>
    </rect>
    
    <!-- Catheter tip -->
    <circle cx="200" cy="320" r="8" fill="#03a9f4" filter="url(#glow)">
      <animate attributeName="cx" values="200;200;480;480;480;480" dur="8s" repeatCount="indefinite"/>
    </circle>
    
    <!-- BALLOON -->
    <g id="balloon">
      <!-- Deflated state -->
      <ellipse cx="480" cy="320" rx="10" ry="10" fill="url(#balloonGrad)" opacity="0" filter="url(#glow)">
        <animate attributeName="opacity" values="0;0;0;1;1;0" dur="8s" repeatCount="indefinite"/>
      </ellipse>
      
      <!-- Inflating balloon - pushes plaque -->
      <ellipse cx="480" cy="320" rx="10" ry="10" fill="url(#balloonGrad)" opacity="0" filter="url(#glow)">
        <animate attributeName="rx" values="10;10;10;10;80;80" dur="8s" repeatCount="indefinite"/>
        <animate attributeName="ry" values="10;10;10;10;45;45" dur="8s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;0;0;0;0.95;0.95" dur="8s" repeatCount="indefinite"/>
      </ellipse>
      
      <!-- Balloon highlight -->
      <ellipse cx="470" cy="310" rx="6" ry="5" fill="white" opacity="0">
        <animate attributeName="rx" values="6;6;6;6;25;25" dur="8s" repeatCount="indefinite"/>
        <animate attributeName="ry" values="5;5;5;5;15;15" dur="8s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;0;0;0;0.7;0.7" dur="8s" repeatCount="indefinite"/>
      </ellipse>
      
      <!-- Radial expansion lines -->
      <g opacity="0">
        <line x1="480" y1="320" x2="480" y2="275" stroke="#ff9800" stroke-width="2">
          <animate attributeName="opacity" values="0;0;0;0;0.6;0" dur="8s" repeatCount="indefinite"/>
        </line>
        <line x1="480" y1="320" x2="480" y2="365" stroke="#ff9800" stroke-width="2">
          <animate attributeName="opacity" values="0;0;0;0;0.6;0" dur="8s" repeatCount="indefinite"/>
        </line>
        <line x1="480" y1="320" x2="420" y2="320" stroke="#ff9800" stroke-width="2">
          <animate attributeName="opacity" values="0;0;0;0;0.6;0" dur="8s" repeatCount="indefinite"/>
        </line>
        <line x1="480" y1="320" x2="540" y2="320" stroke="#ff9800" stroke-width="2">
          <animate attributeName="opacity" values="0;0;0;0;0.6;0" dur="8s" repeatCount="indefinite"/>
        </line>
      </g>
    </g>
  </g>

  <!-- BLOOD FLOW - AFTER (fast, improved) -->
  <g clip-path="url(#arteryFlowClip)">
    <circle r="5" fill="#4caf50" opacity="0">
      <animateMotion dur="2s" repeatCount="indefinite" path="M 310,305 L 640,305"/>
      <animate attributeName="opacity" values="0;0;0;0;0;1" dur="8s" repeatCount="indefinite"/>
    </circle>
    <circle r="4.5" fill="#66bb6a" opacity="0">
      <animateMotion dur="2s" repeatCount="indefinite" begin="0.2s" path="M 310,320 L 640,320"/>
      <animate attributeName="opacity" values="0;0;0;0;0;1" dur="8s" repeatCount="indefinite"/>
    </circle>
    <circle r="5" fill="#4caf50" opacity="0">
      <animateMotion dur="2s" repeatCount="indefinite" begin="0.4s" path="M 310,335 L 640,335"/>
      <animate attributeName="opacity" values="0;0;0;0;0;1" dur="8s" repeatCount="indefinite"/>
    </circle>
    <circle r="4" fill="#66bb6a" opacity="0">
      <animateMotion dur="2.2s" repeatCount="indefinite" begin="0.3s" path="M 310,312 L 640,312"/>
      <animate attributeName="opacity" values="0;0;0;0;0;0.9" dur="8s" repeatCount="indefinite"/>
    </circle>
    <circle r="4" fill="#81c784" opacity="0">
      <animateMotion dur="2.2s" repeatCount="indefinite" begin="0.5s" path="M 310,328 L 640,328"/>
      <animate attributeName="opacity" values="0;0;0;0;0;0.9" dur="8s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- SUCCESS INDICATORS -->
  <!-- Pulse waves after treatment -->
  <g opacity="0">
    <circle cx="480" cy="320" r="50" fill="none" stroke="#4caf50" stroke-width="3">
      <animate attributeName="r" values="50;100;150" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.8;0.4;0" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="stroke-width" values="3;2;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <animate attributeName="opacity" values="0;0;0;0;0;1" dur="8s" repeatCount="indefinite"/>
  </g>

  <!-- Checkmark -->
  <g opacity="0">
    <circle cx="620" cy="320" r="30" fill="#4caf50" filter="url(#softShadow)"/>
    <polyline points="605,320 615,330 635,310" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <animate attributeName="opacity" values="0;0;0;0;0;1" dur="8s" repeatCount="indefinite"/>
  </g>

  <!-- LABELS AND ANNOTATIONS -->
  <!-- Before label -->
  <g opacity="1">
    <rect x="250" y="230" width="100" height="30" rx="15" fill="white" filter="url(#softShadow)"/>
    <text x="300" y="251" text-anchor="middle" fill="#e53935" font-family="Arial, sans-serif" font-size="14" font-weight="bold">TIKALI</text>
    <animate attributeName="opacity" values="1;1;1;1;0;0" dur="8s" repeatCount="indefinite"/>
  </g>

  <!-- After label -->
  <g opacity="0">
    <rect x="250" y="230" width="100" height="30" rx="15" fill="white" filter="url(#softShadow)"/>
    <text x="300" y="251" text-anchor="middle" fill="#4caf50" font-family="Arial, sans-serif" font-size="14" font-weight="bold">AÇIK</text>
    <animate attributeName="opacity" values="0;0;0;0;1;1" dur="8s" repeatCount="indefinite"/>
  </g>

  <!-- Arrow showing blood flow improvement -->
  <g opacity="0">
    <path d="M 560,280 L 620,280" stroke="#4caf50" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
    <path d="M 560,320 L 620,320" stroke="#4caf50" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
    <path d="M 560,360 L 620,360" stroke="#4caf50" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
    <animate attributeName="opacity" values="0;0;0;0;0;0.7" dur="8s" repeatCount="indefinite"/>
  </g>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#4caf50"/>
    </marker>
  </defs>

  <!-- Glow effect around treated area -->
  <circle cx="480" cy="320" r="80" fill="url(#pulseGrad)" opacity="0">
    <animate attributeName="r" values="80;100;80" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0;0;0;0.4;0.4" dur="8s" repeatCount="indefinite"/>
  </g>
</svg>