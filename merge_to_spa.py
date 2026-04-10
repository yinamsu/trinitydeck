import os
import re

def extract_content(html):
    # 1. Identify start of slide-container
    start_match = re.search(r'<div class="slide-container".*?>', html, re.DOTALL)
    if not start_match: return ""
    start_idx = start_match.start()
    
    # 2. Identify the block where slide content ends (before buttons/style/script)
    # Search for <style, <script, <div id="prev-btn", or <div id="next-btn"
    end_block_match = re.search(r'<(style|script|div id="[pn])', html[start_idx:], re.IGNORECASE)
    if not end_block_match:
        # If no style/script found, look for /body
        end_block_match = re.search(r'</body', html[start_idx:], re.IGNORECASE)
        
    if not end_block_match:
        search_limit = len(html)
    else:
        search_limit = start_idx + end_block_match.start()
    
    # 3. From start_idx to search_limit, find the LAST </div>
    # This ensures we get the closing tag of slide-container but nothing after it
    chunk = html[start_idx:search_limit]
    last_div_idx = chunk.rfind('</div>')
    
    if last_div_idx == -1:
        return ""
    
    return chunk[:last_div_idx + 6].strip()

all_slides = []
for i in range(1, 11):
    fname = f"{i}.html"
    if not os.path.exists(fname): continue
    with open(fname, "r", encoding="utf-8") as f:
        html = f.read()
        extracted = extract_content(html)
        if extracted:
            all_slides.append(extracted)
            print(f"Extracted slide {i}")

# Premium SPA Template
master_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trinity Labs Pitch Deck</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;800&family=Gothic+A1:wght@300;400;500;700;800&display=swap" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css" rel="stylesheet" />
    <style>
        * { box-sizing: border-box; }
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            background-color: #050810; color: #FFFFFF;
            font-family: 'Noto Sans KR', sans-serif; overflow: hidden;
        }

        #deck-viewport {
            width: 100%; height: 100vh;
            overflow-y: scroll; scroll-snap-type: y mandatory; scroll-behavior: smooth;
            -ms-overflow-style: none; scrollbar-width: none;
        }
        #deck-viewport::-webkit-scrollbar { display: none; }

        .slide-section {
            width: 100%; height: 100vh; scroll-snap-align: start;
            display: flex; justify-content: center; align-items: center;
            position: relative; overflow: hidden;
        }

        .slide-container {
            width: 1280px; height: 720px;
            position: relative; flex-shrink: 0;
            transform-origin: center;
            background-color: #050810;
        }

        /* Side Navigation Dots */
        #side-nav {
            position: fixed; right: 40px; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 16px; z-index: 10000;
        }
        .nav-dot {
            width: 12px; height: 12px; border-radius: 50%;
            background: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .nav-dot:hover { background: rgba(255, 255, 255, 0.4); transform: scale(1.2); }
        .nav-dot.active {
            background: #3B82F6; transform: scale(1.5);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.6); border-color: #60A5FA;
        }

        /* Nav Arrows */
        .page-arrow {
            position: fixed; left: 50%; transform: translateX(-50%);
            z-index: 10000; color: rgba(255, 255, 255, 0.2);
            font-size: 28px; cursor: pointer; transition: all 0.3s ease; padding: 10px;
        }
        .page-arrow:hover { color: #3B82F6; transform: translateX(-50%) scale(1.2); }
        .up-arrow { top: 20px; }
        .down-arrow { bottom: 20px; }
        .page-arrow.hidden { opacity: 0; pointer-events: none; }

        @media (max-width: 768px) {
            #side-nav { right: 20px; }
        }
    </style>
</head>
<body>
    <div id="side-nav"></div>
    <div id="up-nav" class="page-arrow up-arrow hidden"><i class="fas fa-chevron-up"></i></div>
    <div id="down-nav" class="page-arrow down-arrow"><i class="fas fa-chevron-down"></i></div>

    <div id="deck-viewport">
[PLACEHOLDER]
    </div>

    <script>
        (function() {
            const viewport = document.getElementById('deck-viewport');
            const sections = document.querySelectorAll('.slide-section');
            const sideNav = document.getElementById('side-nav');
            const upNav = document.getElementById('up-nav');
            const downNav = document.getElementById('down-nav');
            
            let currentIdx = 0;

            // Generate Nav Dots
            sections.forEach((_, i) => {
                const dot = document.createElement('div');
                dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
                dot.onclick = () => {
                    viewport.scrollTo({ top: sections[i].offsetTop, behavior: 'smooth' });
                };
                sideNav.appendChild(dot);
            });

            // Update UI on scroll
            viewport.addEventListener('scroll', () => {
                const scrollPos = viewport.scrollTop;
                const winHeight = window.innerHeight;
                currentIdx = Math.round(scrollPos / winHeight);
                
                document.querySelectorAll('.nav-dot').forEach((dot, i) => {
                    dot.classList.toggle('active', i === currentIdx);
                });

                upNav.classList.toggle('hidden', currentIdx === 0);
                downNav.classList.toggle('hidden', currentIdx === sections.length - 1);
            });

            // Click Handlers
            upNav.onclick = () => {
                if (currentIdx > 0) viewport.scrollTo({ top: sections[currentIdx - 1].offsetTop, behavior: 'smooth' });
            };
            downNav.onclick = () => {
                if (currentIdx < sections.length - 1) viewport.scrollTo({ top: sections[currentIdx + 1].offsetTop, behavior: 'smooth' });
            };

            // Keyboard / Space support
            document.addEventListener('keydown', (e) => {
                const scrollKeys = ['ArrowDown', ' ', 'ArrowRight', 'PageDown'];
                const upKeys = ['ArrowUp', 'ArrowLeft', 'PageUp'];
                
                if (scrollKeys.includes(e.key) && currentIdx < sections.length - 1) {
                    e.preventDefault();
                    viewport.scrollTo({ top: sections[currentIdx + 1].offsetTop, behavior: 'smooth' });
                } else if (upKeys.includes(e.key) && currentIdx > 0) {
                    e.preventDefault();
                    viewport.scrollTo({ top: sections[currentIdx - 1].offsetTop, behavior: 'smooth' });
                }
            });

            // Robust Auto-Scaling
            function scaleDeck() {
                const containers = document.querySelectorAll('.slide-container');
                const winWidth = window.innerWidth;
                const winHeight = window.innerHeight;
                const scale = Math.min(winWidth / 1280, winHeight / 720) * 0.95;
                containers.forEach(el => {
                    el.style.transform = `scale(${scale})`;
                });
            }

            window.addEventListener('resize', scaleDeck);
            scaleDeck();
        })();
    </script>
</body>
</html>
"""

slides_block = ""
for i, content in enumerate(all_slides):
    slides_block += f'        <section class="slide-section" id="section-{i+1}">\\n'
    slides_block += f'            {content}\\n'
    slides_block += f'        </section>\\n'

# Handle the newline characters correctly during replacement
final_html = master_template.replace("[PLACEHOLDER]", slides_block).replace("\\\\n", "\\n").replace("\\n", "\\n")
# Actually, the string replacement above is tricky with f-strings.
# Let's just do it cleanly.

slides_block = ""
for i, content in enumerate(all_slides):
    slides_block += f'        <section class="slide-section" id="section-{i+1}">\\n'
    slides_block += f'            {content}\\n'
    slides_block += f'        </section>\\n'

# Correct way to handle literal backslashes if needed, but here we just want real newlines.
final_html = master_template.replace("[PLACEHOLDER]", slides_block).replace("\\n", "\n")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("SUCCESS: index.html has been corrected and stabilized.")
