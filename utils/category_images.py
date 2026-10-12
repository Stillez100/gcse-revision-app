"""
Category Illustration SVG generator for GCSE Revision App.
Generates rich, scientific and mathematical vector illustrations
for each GCSE Biology and GCSE Maths category.
"""

def _raw_svg(cat_name: str) -> str:
    cat_lower = cat_name.lower().replace(",", " &").strip()
    
    # ── Biology Categories ──
    if "cell" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_cell" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F2027"/>
      <stop offset="50%" stop-color="#203A43"/>
      <stop offset="100%" stop-color="#2C5364"/>
    </linearGradient>
    <radialGradient id="nuc_glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#A78BFA"/>
      <stop offset="70%" stop-color="#6D28D9"/>
      <stop offset="100%" stop-color="#4C1D95"/>
    </radialGradient>
    <linearGradient id="cyto" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#059669" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#10B981" stop-opacity="0.15"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_cell)"/>
  <!-- Cell Wall / Membrane -->
  <rect x="12" y="15" width="86" height="110" rx="28" fill="url(#cyto)" stroke="#34D399" stroke-width="2.2" stroke-dasharray="1 0"/>
  <rect x="16" y="19" width="78" height="102" rx="24" fill="none" stroke="#10B981" stroke-width="1.2" stroke-opacity="0.6"/>
  <!-- Nucleus & Nucleolus -->
  <circle cx="55" cy="62" r="22" fill="url(#nuc_glow)" stroke="#C4B5FD" stroke-width="1.5"/>
  <circle cx="55" cy="62" r="8" fill="#EDE9FE" opacity="0.9"/>
  <!-- Chromatin swirls -->
  <path d="M 45 57 Q 52 50 58 59 Q 65 67 52 70" fill="none" stroke="#DDD6FE" stroke-width="1.2" opacity="0.6"/>
  <!-- Mitochondria -->
  <g transform="translate(24, 92) rotate(-25)">
    <rect width="24" height="13" rx="6.5" fill="#F59E0B" stroke="#FBBF24" stroke-width="1"/>
    <path d="M 4 6.5 Q 8 2 12 6.5 T 20 6.5" fill="none" stroke="#FEF3C7" stroke-width="1.2"/>
  </g>
  <!-- Ribosomes / Endoplasmic Reticulum folds -->
  <path d="M 32 32 Q 55 24 78 32" fill="none" stroke="#60A5FA" stroke-width="1.8" opacity="0.7"/>
  <path d="M 36 38 Q 55 30 74 38" fill="none" stroke="#93C5FD" stroke-width="1.4" opacity="0.5"/>
  <circle cx="34" cy="48" r="2" fill="#60A5FA"/>
  <circle cx="76" cy="46" r="2" fill="#60A5FA"/>
  <circle cx="78" cy="85" r="2" fill="#34D399"/>
  <circle cx="72" cy="98" r="2.5" fill="#34D399"/>
  <!-- Microscope focal ring overlay -->
  <circle cx="55" cy="70" r="48" fill="none" stroke="#FFFFFF" stroke-width="0.8" opacity="0.25"/>
</svg>'''

    elif "infection" in cat_lower or "response" in cat_lower and "homeostasis" not in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_inf" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E1B4B"/>
      <stop offset="60%" stop-color="#311042"/>
      <stop offset="100%" stop-color="#4C0519"/>
    </linearGradient>
    <radialGradient id="virus_glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="70%" stop-color="#B91C1C"/>
      <stop offset="100%" stop-color="#7F1D1D"/>
    </radialGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_inf)"/>
  <!-- Defensive shield barrier -->
  <path d="M 55 18 C 76 18 90 28 90 52 C 90 85 55 118 55 118 C 55 118 20 85 20 52 C 20 28 34 18 55 18 Z" fill="none" stroke="#60A5FA" stroke-width="1.8" opacity="0.4" stroke-dasharray="3 2"/>
  <!-- Central Pathogen / Virus Core -->
  <circle cx="55" cy="65" r="20" fill="url(#virus_glow)" stroke="#FCA5A5" stroke-width="1.5"/>
  <!-- Virus Spike Glycoproteins -->
  <line x1="55" y1="45" x2="55" y2="35" stroke="#F87171" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="55" cy="34" r="3.2" fill="#FCA5A5"/>
  <line x1="55" y1="85" x2="55" y2="95" stroke="#F87171" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="55" cy="96" r="3.2" fill="#FCA5A5"/>
  <line x1="35" y1="65" x2="25" y2="65" stroke="#F87171" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="24" cy="65" r="3.2" fill="#FCA5A5"/>
  <line x1="75" y1="65" x2="85" y2="65" stroke="#F87171" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="86" cy="65" r="3.2" fill="#FCA5A5"/>
  <line x1="41" y1="51" x2="34" y2="44" stroke="#F87171" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="33" cy="43" r="3" fill="#FCA5A5"/>
  <line x1="69" y1="79" x2="76" y2="86" stroke="#F87171" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="77" cy="87" r="3" fill="#FCA5A5"/>
  <line x1="69" y1="51" x2="76" y2="44" stroke="#F87171" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="77" cy="43" r="3" fill="#FCA5A5"/>
  <line x1="41" y1="79" x2="34" y2="86" stroke="#F87171" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="33" cy="87" r="3" fill="#FCA5A5"/>
  <!-- Y-shaped Antibodies -->
  <g transform="translate(24, 28) scale(0.85)">
    <path d="M 10 18 L 10 10 M 10 10 L 5 4 M 10 10 L 15 4" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <g transform="translate(72, 92) scale(0.85)">
    <path d="M 10 18 L 10 10 M 10 10 L 5 4 M 10 10 L 15 4" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <!-- Virus capsid texture -->
  <circle cx="50" cy="62" r="3" fill="#FECACA" opacity="0.7"/>
  <circle cx="61" cy="68" r="2.5" fill="#FECACA" opacity="0.7"/>
</svg>'''

    elif "bioenergetic" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_bio" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#064E3B"/>
      <stop offset="50%" stop-color="#065F46"/>
      <stop offset="100%" stop-color="#022C22"/>
    </linearGradient>
    <radialGradient id="sun_glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FDE047"/>
      <stop offset="60%" stop-color="#EAB308"/>
      <stop offset="100%" stop-color="#CA8A04"/>
    </radialGradient>
    <linearGradient id="leaf_grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4ADE80"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_bio)"/>
  <!-- Sun / Light energy -->
  <circle cx="26" cy="28" r="14" fill="url(#sun_glow)"/>
  <line x1="26" y1="8" x2="26" y2="3" stroke="#FDE047" stroke-width="2" stroke-linecap="round"/>
  <line x1="46" y1="28" x2="51" y2="28" stroke="#FDE047" stroke-width="2" stroke-linecap="round"/>
  <line x1="40" y1="42" x2="44" y2="46" stroke="#FDE047" stroke-width="2" stroke-linecap="round"/>
  <!-- Energy ray lines radiating to leaf -->
  <path d="M 38 38 L 56 62" stroke="#FEF08A" stroke-width="1.4" stroke-dasharray="3 2" opacity="0.8"/>
  <path d="M 42 28 L 70 54" stroke="#FEF08A" stroke-width="1.4" stroke-dasharray="3 2" opacity="0.8"/>
  <!-- Chloroplast / Leaf blade -->
  <path d="M 30 115 C 30 75 60 52 92 50 C 92 86 78 115 30 115 Z" fill="url(#leaf_grad)" stroke="#86EFAC" stroke-width="1.6"/>
  <!-- Leaf veins (vascular bundle) -->
  <path d="M 30 115 Q 58 84 92 50" fill="none" stroke="#DCFCE7" stroke-width="2"/>
  <path d="M 52 92 Q 68 84 76 72" fill="none" stroke="#DCFCE7" stroke-width="1.2"/>
  <path d="M 42 102 Q 54 98 64 88" fill="none" stroke="#DCFCE7" stroke-width="1.2"/>
  <!-- Thylakoid grana stack (ATP synthesis) -->
  <g transform="translate(62, 88)">
    <rect x="0" y="0" width="22" height="5" rx="2.5" fill="#BBF7D0"/>
    <rect x="2" y="6" width="22" height="5" rx="2.5" fill="#86EFAC"/>
    <rect x="1" y="12" width="22" height="5" rx="2.5" fill="#4ADE80"/>
  </g>
  <!-- ATP burst indicator -->
  <text x="55" y="128" font-family="system-ui, sans-serif" font-size="11" font-weight="900" fill="#FDE047">ATP ⚡</text>
</svg>'''

    elif "homeostasis" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_hom" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E1B4B"/>
      <stop offset="60%" stop-color="#312E81"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="brain_grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F472B6"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_hom)"/>
  <!-- Stylized Brain Profile & Nervous System -->
  <path d="M 32 60 C 24 50 32 30 52 28 C 72 26 86 36 84 54 C 88 64 80 80 66 82 C 60 84 56 94 56 100 L 50 100 C 50 92 42 84 38 80 C 28 76 26 66 32 60 Z" fill="url(#brain_grad)" stroke="#DDD6FE" stroke-width="1.8"/>
  <!-- Cerebral convolutions / sulci folds -->
  <path d="M 40 40 Q 52 48 64 38 Q 72 48 78 58" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.6"/>
  <path d="M 36 56 Q 48 60 58 54 Q 70 66 76 72" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.6"/>
  <path d="M 44 70 Q 52 74 60 68" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.6"/>
  <!-- Spinal cord nerve impulses -->
  <line x1="53" y1="100" x2="53" y2="132" stroke="#67E8F9" stroke-width="2.5" stroke-dasharray="4 2"/>
  <!-- Synaptic spark nodes -->
  <circle cx="53" cy="108" r="3" fill="#A5F3FC"/>
  <circle cx="53" cy="122" r="3" fill="#A5F3FC"/>
  <!-- Thermoregulation / Set Point Badge: 37°C -->
  <rect x="62" y="104" width="42" height="22" rx="6" fill="#1E293B" stroke="#EC4899" stroke-width="1.2"/>
  <text x="67" y="119" font-family="system-ui, sans-serif" font-size="10.5" font-weight="900" fill="#F472B6">37°C ⚖️</text>
</svg>'''

    elif "inheritance" in cat_lower or "evolution" in cat_lower or "genetic" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_gen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#180D2B"/>
      <stop offset="50%" stop-color="#2D124D"/>
      <stop offset="100%" stop-color="#0D0717"/>
    </linearGradient>
    <linearGradient id="helix1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EC4899"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>
    <linearGradient id="helix2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#06B6D4"/>
      <stop offset="100%" stop-color="#3B82F6"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_gen)"/>
  <!-- Double Helix Strands -->
  <path d="M 28 15 Q 55 42 82 42 T 28 95 T 82 135" fill="none" stroke="url(#helix1)" stroke-width="3" stroke-linecap="round"/>
  <path d="M 82 15 Q 55 42 28 42 T 82 95 T 28 135" fill="none" stroke="url(#helix2)" stroke-width="3" stroke-linecap="round"/>
  <!-- Base Pairs / Hydrogen Bonds -->
  <line x1="38" y1="24" x2="72" y2="24" stroke="#F43F5E" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="55" cy="24" r="2.2" fill="#FFFFFF"/>
  <line x1="42" y1="36" x2="68" y2="36" stroke="#10B981" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="55" cy="36" r="2.2" fill="#FFFFFF"/>
  <line x1="55" y1="42" x2="55" y2="42" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="42" y1="52" x2="68" y2="52" stroke="#F59E0B" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="55" cy="52" r="2.2" fill="#FFFFFF"/>
  <line x1="34" y1="68" x2="76" y2="68" stroke="#3B82F6" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="55" cy="68" r="2.2" fill="#FFFFFF"/>
  <line x1="38" y1="82" x2="72" y2="82" stroke="#F43F5E" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="55" cy="82" r="2.2" fill="#FFFFFF"/>
  <line x1="42" y1="108" x2="68" y2="108" stroke="#10B981" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="55" cy="108" r="2.2" fill="#FFFFFF"/>
  <line x1="34" y1="124" x2="76" y2="124" stroke="#3B82F6" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="55" cy="124" r="2.2" fill="#FFFFFF"/>
  <!-- Sparkles -->
  <circle cx="20" cy="40" r="1.5" fill="#F472B6"/>
  <circle cx="92" cy="75" r="1.5" fill="#38BDF8"/>
  <circle cx="18" cy="110" r="1.5" fill="#A78BFA"/>
</svg>'''

    elif "ecology" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_eco" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#022C22"/>
      <stop offset="60%" stop-color="#064E3B"/>
      <stop offset="100%" stop-color="#042F2E"/>
    </linearGradient>
    <radialGradient id="globe_glow" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="65%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0369A1"/>
    </radialGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_eco)"/>
  <!-- Planet Earth / Ecosystem Biosphere -->
  <circle cx="55" cy="62" r="32" fill="url(#globe_glow)" stroke="#67E8F9" stroke-width="1.8"/>
  <!-- Continents / Flora green patches -->
  <path d="M 42 42 Q 52 48 58 42 Q 68 50 62 62 Q 54 68 46 60 Z" fill="#22C55E" opacity="0.9"/>
  <path d="M 50 72 Q 62 76 72 68 Q 78 80 66 84 Q 56 86 50 72 Z" fill="#16A34A" opacity="0.9"/>
  <path d="M 32 60 Q 40 68 36 76 Q 28 72 32 60 Z" fill="#22C55E" opacity="0.85"/>
  <!-- Atmosphere ozone ring -->
  <circle cx="55" cy="62" r="36" fill="none" stroke="#BAE6FD" stroke-width="1.2" opacity="0.45"/>
  <!-- Foliage / Oak tree canopy crest -->
  <path d="M 36 122 L 74 122 L 62 98 L 70 98 L 55 80 L 40 98 L 48 98 Z" fill="#10B981" stroke="#34D399" stroke-width="1.2"/>
  <!-- Energy Cycle Arrows -->
  <path d="M 22 55 A 40 40 0 0 1 88 55" fill="none" stroke="#FDE047" stroke-width="1.5" stroke-dasharray="3 2"/>
  <polygon points="88,52 93,56 87,60" fill="#FDE047"/>
  <text x="32" y="134" font-family="system-ui, sans-serif" font-size="9.5" font-weight="900" fill="#A7F3D0">BIOSPHERE</text>
</svg>'''

    # ── Maths Categories ──
    elif "algebra" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_alg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="50%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#312E81"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_alg)"/>
  <!-- Cartesian Coordinate Grid -->
  <line x1="14" y1="75" x2="96" y2="75" stroke="#475569" stroke-width="1.2"/>
  <line x1="55" y1="18" x2="55" y2="122" stroke="#475569" stroke-width="1.2"/>
  <!-- Axis Arrows -->
  <polygon points="96,73 101,75 96,77" fill="#94A3B8"/>
  <polygon points="53,18 55,13 57,18" fill="#94A3B8"/>
  <!-- Quadratic Parabola Curve: y = ax^2 + c -->
  <path d="M 22 28 Q 55 110 88 28" fill="none" stroke="#818CF8" stroke-width="2.6" stroke-linecap="round"/>
  <!-- Linear Tangent: y = mx + c -->
  <line x1="20" y1="110" x2="90" y2="40" stroke="#F43F5E" stroke-width="1.8" stroke-dasharray="3 2"/>
  <!-- Vertex point -->
  <circle cx="55" cy="69" r="3.5" fill="#FDE047"/>
  <!-- Formula overlay badge -->
  <rect x="22" y="112" width="66" height="20" rx="6" fill="#0F172A" stroke="#6366F1" stroke-width="1.2"/>
  <text x="26" y="126" font-family="'Courier New', monospace" font-size="11" font-weight="900" fill="#A5B4FC">f(x)=ax²+c</text>
</svg>'''

    elif "geometry" in cat_lower or "measure" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_geom" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#082F49"/>
      <stop offset="50%" stop-color="#0C4A6E"/>
      <stop offset="100%" stop-color="#0369A1"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_geom)"/>
  <!-- 3D Isometric Cube / Prism Wireframe -->
  <polygon points="55,18 88,34 55,50 22,34" fill="#0284C7" stroke="#38BDF8" stroke-width="1.6" opacity="0.8"/>
  <polygon points="22,34 55,50 55,84 22,68" fill="#0369A1" stroke="#38BDF8" stroke-width="1.6" opacity="0.9"/>
  <polygon points="55,50 88,34 88,68 55,84" fill="#075985" stroke="#38BDF8" stroke-width="1.6" opacity="0.95"/>
  <!-- Right-Angled Triangle with Pythagorean arc -->
  <polygon points="24,124 88,124 88,88" fill="#0284C7" fill-opacity="0.25" stroke="#FDE047" stroke-width="2"/>
  <!-- Right-angle square -->
  <rect x="80" y="116" width="8" height="8" fill="none" stroke="#FDE047" stroke-width="1.4"/>
  <!-- Theta angle arc -->
  <path d="M 40 124 A 16 16 0 0 0 36 114" fill="none" stroke="#F43F5E" stroke-width="1.6"/>
  <text x="44" y="120" font-family="system-ui, sans-serif" font-size="9" font-weight="900" fill="#F43F5E">θ</text>
  <text x="48" y="134" font-family="'Courier New', monospace" font-size="10" font-weight="900" fill="#BAE6FD">a²+b²=c²</text>
</svg>'''

    elif "number" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_num" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1C1917"/>
      <stop offset="50%" stop-color="#292524"/>
      <stop offset="100%" stop-color="#44403C"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_num)"/>
  <!-- Golden Spiral (Fibonacci) curve -->
  <path d="M 24 95 A 18 18 0 0 1 42 77 A 28 28 0 0 1 70 105 A 44 44 0 0 1 26 130" fill="none" stroke="#F59E0B" stroke-width="2.2" stroke-linecap="round"/>
  <!-- Number and Math Symbols Grid -->
  <text x="24" y="42" font-family="'Courier New', monospace" font-size="24" font-weight="900" fill="#FBBF24">π</text>
  <text x="64" y="42" font-family="'Courier New', monospace" font-size="22" font-weight="900" fill="#38BDF8">√x</text>
  <text x="22" y="74" font-family="'Courier New', monospace" font-size="20" font-weight="900" fill="#A855F7">∑</text>
  <text x="64" y="74" font-family="'Courier New', monospace" font-size="20" font-weight="900" fill="#10B981">%</text>
  <text x="32" y="106" font-family="'Courier New', monospace" font-size="16" font-weight="900" fill="#F43F5E">xⁿ</text>
  <text x="68" y="106" font-family="'Courier New', monospace" font-size="16" font-weight="900" fill="#F59E0B">½</text>
</svg>'''

    elif "probability" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_prob" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2E1065"/>
      <stop offset="50%" stop-color="#3B0764"/>
      <stop offset="100%" stop-color="#4C1D95"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_prob)"/>
  <!-- 3D Isometric Dice -->
  <g transform="translate(18, 16)">
    <!-- Top Face -->
    <polygon points="36,6 64,18 36,30 8,18" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.4"/>
    <circle cx="36" cy="18" r="3.2" fill="#DC2626"/>
    <!-- Left Face -->
    <polygon points="8,18 36,30 36,60 8,48" fill="#E2E8F0" stroke="#CBD5E1" stroke-width="1.4"/>
    <circle cx="18" cy="30" r="2.4" fill="#0F172A"/>
    <circle cx="26" cy="49" r="2.4" fill="#0F172A"/>
    <!-- Right Face -->
    <polygon points="36,30 64,18 64,48 36,60" fill="#CBD5E1" stroke="#94A3B8" stroke-width="1.4"/>
    <circle cx="46" cy="40" r="2.2" fill="#0F172A"/>
    <circle cx="54" cy="32" r="2.2" fill="#0F172A"/>
    <circle cx="46" cy="52" r="2.2" fill="#0F172A"/>
    <circle cx="54" cy="44" r="2.2" fill="#0F172A"/>
  </g>
  <!-- Venn Diagram: Sets A and B -->
  <circle cx="42" cy="104" r="22" fill="#EC4899" fill-opacity="0.35" stroke="#F472B6" stroke-width="1.6"/>
  <circle cx="68" cy="104" r="22" fill="#3B82F6" fill-opacity="0.35" stroke="#60A5FA" stroke-width="1.6"/>
  <!-- Overlap text -->
  <text x="49" y="108" font-family="system-ui, sans-serif" font-size="9" font-weight="900" fill="#FDE047">A∩B</text>
  <text x="35" y="134" font-family="'Courier New', monospace" font-size="10" font-weight="900" fill="#DDD6FE">P(A)=n/N</text>
</svg>'''

    elif "ratio" in cat_lower or "proportion" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_rat" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#042F2E"/>
      <stop offset="50%" stop-color="#115E59"/>
      <stop offset="100%" stop-color="#134E4A"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_rat)"/>
  <!-- Classic Mechanical Balance Scales -->
  <!-- Fulcrum base -->
  <polygon points="55,60 46,92 64,92" fill="#14B8A6" stroke="#2DD4BF" stroke-width="1.4"/>
  <line x1="38" y1="92" x2="72" y2="92" stroke="#2DD4BF" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Balance beam -->
  <line x1="20" y1="48" x2="90" y2="48" stroke="#FBBF24" stroke-width="3" stroke-linecap="round"/>
  <circle cx="55" cy="48" r="4.5" fill="#F59E0B"/>
  <!-- Left Pan -->
  <line x1="24" y1="48" x2="16" y2="68" stroke="#FDE68A" stroke-width="1.2"/>
  <line x1="24" y1="48" x2="32" y2="68" stroke="#FDE68A" stroke-width="1.2"/>
  <path d="M 12 68 Q 24 78 36 68 Z" fill="#F59E0B" stroke="#FCD34D" stroke-width="1.2"/>
  <!-- Left weights: 1 block -->
  <rect x="20" y="60" width="8" height="8" rx="2" fill="#F43F5E"/>
  <!-- Right Pan -->
  <line x1="86" y1="48" x2="78" y2="68" stroke="#FDE68A" stroke-width="1.2"/>
  <line x1="86" y1="48" x2="94" y2="68" stroke="#FDE68A" stroke-width="1.2"/>
  <path d="M 74 68 Q 86 78 98 68 Z" fill="#F59E0B" stroke="#FCD34D" stroke-width="1.2"/>
  <!-- Right weights: 2 blocks (Ratio 1 : 2) -->
  <rect x="80" y="60" width="6" height="8" rx="1.5" fill="#3B82F6"/>
  <rect x="88" y="60" width="6" height="8" rx="1.5" fill="#3B82F6"/>
  <!-- Ratio badge -->
  <rect x="28" y="106" width="54" height="22" rx="6" fill="#0F172A" stroke="#2DD4BF" stroke-width="1.4"/>
  <text x="38" y="122" font-family="'Courier New', monospace" font-size="13" font-weight="900" fill="#5EEAD4">1 : 2</text>
</svg>'''

    elif "statistic" in cat_lower:
        return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <defs>
    <linearGradient id="bg_stat" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#18181B"/>
      <stop offset="50%" stop-color="#27272A"/>
      <stop offset="100%" stop-color="#3F3F46"/>
    </linearGradient>
    <linearGradient id="bar1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <linearGradient id="bar2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#A855F7"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
    <linearGradient id="bar3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#22C55E"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <rect width="110" height="140" fill="url(#bg_stat)"/>
  <!-- Grid Axis -->
  <line x1="16" y1="105" x2="98" y2="105" stroke="#52525B" stroke-width="1.4"/>
  <line x1="16" y1="20" x2="16" y2="105" stroke="#52525B" stroke-width="1.4"/>
  <!-- Multi-bar Histogram -->
  <rect x="24" y="65" width="14" height="40" rx="3" fill="url(#bar1)"/>
  <rect x="44" y="42" width="14" height="63" rx="3" fill="url(#bar2)"/>
  <rect x="64" y="28" width="14" height="77" rx="3" fill="url(#bar3)"/>
  <rect x="84" y="55" width="14" height="50" rx="3" fill="#F59E0B"/>
  <!-- Trendline / Regression line -->
  <path d="M 22 75 Q 52 46 95 24" fill="none" stroke="#F43F5E" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="31" cy="65" r="3" fill="#FDE047"/>
  <circle cx="51" cy="42" r="3" fill="#FDE047"/>
  <circle cx="71" cy="28" r="3" fill="#FDE047"/>
  <circle cx="91" cy="55" r="3" fill="#FDE047"/>
  <!-- Stats Badge -->
  <text x="24" y="126" font-family="'Courier New', monospace" font-size="11" font-weight="900" fill="#E4E4E7">x̄=μ • σ²</text>
</svg>'''

    # Generic Fallback
    return '''<svg viewBox="0 0 110 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="border-radius:10px 0 0 10px; display:block;">
  <rect width="110" height="140" fill="#1E293B"/>
  <circle cx="55" cy="70" r="30" fill="#6366F1" opacity="0.3"/>
  <text x="35" y="78" font-size="32">📚</text>
</svg>'''

def get_category_svg(cat_name: str) -> str:
    raw = _raw_svg(cat_name)
    return " ".join(line.strip() for line in raw.splitlines())
