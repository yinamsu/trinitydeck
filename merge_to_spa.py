import os
import re

def extract_content(html):
    # Find the slide-container div
    start_match = re.search(r'<div class="slide-container".*?>', html, re.DOTALL)
    if not start_match:
        return ""
    start_idx = start_match.start()
    
    # Robustly find the matching closing </div>
    # Starting from start_idx, we track <div> and </div>
    count = 0
    pos = start_idx
    while pos < len(html):
        if html[pos:pos+4] == '<div':
            count += 1
            pos += 4
        elif html[pos:pos+6] == '</div>':
            count -= 1
            if count == 0:
                return html[start_idx:pos+6]
            pos += 6
        else:
            pos += 1
    return ""

all_slides_html = []
for i in range(1, 11):
    filename = f"{i}.html"
    if not os.path.exists(filename): continue
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()
        extracted = extract_content(html)
        if extracted:
            all_slides_html.append(extracted)
            print(f"Extracted: {filename}")

# Master Template
template = """<!DOCTYPE html>
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
            scrollbar-width: none; -ms-overflow-style: none;
        }
        #deck-viewport::-webkit-scrollbar { display: none; }
        .slide-section {
            width: 100%; height: 100vh; scroll-snap-align: start;
            display: flex; justify-content: center; align-items: center;
            position: relative; overflow: hidden;
        }
        .slide-container {
            width: 1280px; height: 720px; position: relative;
            flex-shrink: 0; transform-origin: center;
        }
        #side-nav {
            position: fixed; right: 40px; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 16px; z-index: 10000;
        }
        .nav-dot {
            width: 12px; height: 12px; border-radius: 50%;
            background: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .nav-dot.active {
            background: #3B82F6; transform: scale(1.5);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.6); border-color: #60A5FA;
        }
        .page-arrow {
            position: fixed; left: 50%; transform: translateX(-50%);
            z-index: 10000; color: rgba(255, 255, 255, 0.2);
            font-size: 28px; cursor: pointer; transition: all 0.3s ease; padding: 10px;
        }
        .page-arrow:hover { color: #3B82F6; transform: translateX(-50%) scale(1.2); }
        .up-arrow { top: 20px; }
        .down-arrow { bottom: 20px; }
        .page-arrow.hidden { opacity: 0; pointer-events: none; }
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
            sections.forEach((_, i) => {
                const dot = document.createElement('div');
                dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
                dot.onclick = () => viewport.scrollTo({ top: sections[i].offsetTop, behavior: 'smooth' });
                sideNav.appendChild(dot);
            });
            viewport.addEventListener('scroll', () => {
                const scrollPos = viewport.scrollTop;
                const winHeight = window.innerHeight;
                currentIdx = Math.round(scrollPos / winHeight);
                document.querySelectorAll('.nav-dot').forEach((dot, i) => dot.classList.toggle('active', i === currentIdx));
                upNav.classList.toggle('hidden', currentIdx === 0);
                downNav.classList.toggle('hidden', currentIdx === sections.length - 1);
            });
            upNav.onclick = () => { if (currentIdx > 0) viewport.scrollTo({ top: sections[currentIdx - 1].offsetTop, behavior: 'smooth' }); };
            downNav.onclick = () => { if (currentIdx < sections.length - 1) viewport.scrollTo({ top: sections[currentIdx + 1].offsetTop, behavior: 'smooth' }); };
            document.addEventListener('keydown', (e) => {
                const keys = ['ArrowDown', ' ', 'ArrowRight', 'PageDown'];
                const upKeys = ['ArrowUp', 'ArrowLeft', 'PageUp'];
                if (keys.includes(e.key) && currentIdx < sections.length - 1) {
                    e.preventDefault(); viewport.scrollTo({ top: sections[currentIdx + 1].offsetTop, behavior: 'smooth' });
                } else if (upKeys.includes(e.key) && currentIdx > 0) {
                    e.preventDefault(); viewport.scrollTo({ top: sections[currentIdx - 1].offsetTop, behavior: 'smooth' });
                }
            });
            function scaleDeck() {
                const containers = document.querySelectorAll('.slide-container');
                const winWidth = window.innerWidth, winHeight = window.innerHeight;
                const scale = Math.min(winWidth / 1280, winHeight / 720) * 0.95;
                containers.forEach(el => el.style.transform = `scale(${scale})`);
            }
            window.addEventListener('resize', scaleDeck);
            scaleDeck();
        })();
    </script>
</body>
</html>
"""

sections_html = ""
for i, inner_html in enumerate(all_slides_html):
    sections_html += f'        <section class="slide-section" id="section-{i+1}">\\n            {inner_html}\\n        </section>\\n'.replace("\\n", "\n")

final_html = template.replace("[PLACEHOLDER]", sections_html)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)
print("SUCCESS: index.html emergency fix applied.")
