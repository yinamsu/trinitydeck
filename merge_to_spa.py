import os
import re

def extract_content(html):
    # Find the slide-container div carefully
    start_tag = '<div class="slide-container"'
    start_idx = html.find(start_tag)
    if start_idx == -1:
        return ""
    
    # Use balanced div counting to extract the full container
    content_from_start = html[start_idx:]
    depth = 0
    end_idx = 0
    
    # We look for <div and </div
    tags = re.finditer(r'<(/?div)', content_from_start)
    for tag in tags:
        if tag.group(1) == 'div':
            depth += 1
        elif tag.group(1) == '/div':
            depth -= 1
        
        if depth == 0:
            end_idx = tag.end()
            break
    
    if end_idx == 0: return ""
    return content_from_start[:end_idx]

all_slides_html = []
for i in range(1, 11):
    filename = f"{i}.html"
    try:
        if not os.path.exists(filename):
            print(f"Skipping missing: {filename}")
            continue
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
            extracted = extract_content(html)
            if extracted:
                all_slides_html.append(extracted)
                print(f"Extracted: {filename}")
            else:
                print(f"Failed: {filename}")
    except Exception as e:
        print(f"Error handling {filename}: {e}")

# The Master Template
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
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #050810;
            color: #FFFFFF;
            font-family: 'Noto Sans KR', sans-serif;
            overflow: hidden;
        }

        #deck-viewport {
            width: 100%;
            height: 100vh;
            overflow-y: scroll;
            scroll-snap-type: y mandatory;
            scroll-behavior: smooth;
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        #deck-viewport::-webkit-scrollbar { display: none; }

        .slide-section {
            width: 100%;
            height: 100vh;
            scroll-snap-align: start;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        .slide-container {
            width: 1280px;
            height: 720px;
            position: relative;
            flex-shrink: 0;
            transform-origin: center;
        }

        /* Side Navigation Dots */
        #side-nav {
            position: fixed;
            right: 40px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 16px;
            z-index: 10000;
        }
        .nav-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .nav-dot:hover { background: rgba(255, 255, 255, 0.4); transform: scale(1.2); }
        .nav-dot.active {
            background: #3B82F6;
            transform: scale(1.5);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
            border-color: #60A5FA;
        }

        /* Nav Arrows */
        .page-arrow {
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10000;
            color: rgba(255, 255, 255, 0.2);
            font-size: 28px;
            cursor: pointer;
            transition: all 0.3s ease;
            padding: 10px;
        }
        .page-arrow:hover { color: #3B82F6; transform: translateX(-50%) scale(1.2); }
        .up-arrow { top: 20px; }
        .down-arrow { bottom: 20px; }
        .page-arrow.hidden { opacity: 0; pointer-events: none; }

        @media (max-width: 768px) {
            #side-nav { right: 20px; }
            .nav-dot { width: 10px; height: 10px; }
            .page-arrow { font-size: 20px; }
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

            // Generate dots
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

            // Click handlers
            upNav.onclick = () => {
                if (currentIdx > 0) viewport.scrollTo({ top: sections[currentIdx - 1].offsetTop, behavior: 'smooth' });
            };
            downNav.onclick = () => {
                if (currentIdx < sections.length - 1) viewport.scrollTo({ top: sections[currentIdx + 1].offsetTop, behavior: 'smooth' });
            };

            // Keyboard/Space
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowDown' || e.key === ' ' || e.key === 'ArrowRight' || e.key === 'PageDown') {
                    if (currentIdx < sections.length - 1) {
                        e.preventDefault();
                        viewport.scrollTo({ top: sections[currentIdx + 1].offsetTop, behavior: 'smooth' });
                    }
                } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') {
                    if (currentIdx > 0) {
                        e.preventDefault();
                        viewport.scrollTo({ top: sections[currentIdx - 1].offsetTop, behavior: 'smooth' });
                    }
                }
            });

            // Responsive Scaling
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
for i, inner_html in enumerate(all_slides_html):
    slides_block += f'<section class="slide-section" id="section-{i+1}">{inner_html}</section>\\n'

final_html = template.replace("[PLACEHOLDER]", slides_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("SUCCESS: index.html consolidated.")
