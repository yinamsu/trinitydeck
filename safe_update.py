import os
import re

# Body Centering CSS
body_centering_style = """
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #050810;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .slide-container {
            flex-shrink: 0;
            transform-origin: center;
        }
"""

# High-visibility styling (updated)
btn_style = """
        .nav-btn {
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            width: 70px;
            height: 70px;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(12px);
            border: 2px solid #3B82F6;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            font-size: 28px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 9999;
            text-decoration: none;
            opacity: 1;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
        }
        .nav-btn:hover {
            background: rgba(59, 130, 246, 0.3);
            border-color: #60A5FA;
            transform: translateY(-50%) scale(1.1);
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.5);
        }
        .prev-btn { left: 40px; }
        .next-btn { right: 40px; }
        .nav-btn.disabled {
            display: none !important;
        }
        @media (max-width: 768px) {
            .nav-btn { width: 55px; height: 55px; font-size: 22px; }
            .prev-btn { left: 15px; }
            .next-btn { right: 15px; }
        }
    </style>
"""

# HTML and JS logic (with Auto-Scaling)
new_component = body_centering_style + btn_style + """
    <div id="prev-btn" class="nav-btn prev-btn"><i class="fas fa-chevron-left"></i></div>
    <div id="next-btn" class="nav-btn next-btn"><i class="fas fa-chevron-right"></i></div>

    <script>
        (function() {
            // Navigation Logic
            function navigate(direction) {
                const currentPath = window.location.pathname;
                let fileName = currentPath.split('/').pop() || 'index.html';
                let currentPage = 1;
                if (fileName.includes('.html') && fileName !== 'index.html') {
                    currentPage = parseInt(fileName.replace('.html', '')) || 1;
                }

                if (direction === 'next' && currentPage < 10) {
                    window.location.href = (currentPage + 1) + '.html';
                } else if (direction === 'prev' && currentPage > 1) {
                    if (currentPage === 2) {
                        window.location.href = 'index.html';
                    } else {
                        window.location.href = (currentPage - 1) + '.html';
                    }
                }
            }

            // Keyboard Support
            document.addEventListener('keydown', function (e) {
                if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
                    navigate('next');
                } else if (e.key === 'ArrowLeft') {
                    navigate('prev');
                }
            });

            // Button Support
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');

            const currentPath = window.location.pathname;
            let fileName = currentPath.split('/').pop() || 'index.html';
            let currentPage = 1;
            if (fileName.includes('.html') && fileName !== 'index.html') {
                currentPage = parseInt(fileName.replace('.html', '')) || 1;
            }

            if (currentPage === 1) prevBtn.classList.add('disabled');
            if (currentPage === 10) nextBtn.classList.add('disabled');

            prevBtn.addEventListener('click', () => navigate('prev'));
            nextBtn.addEventListener('click', () => navigate('next'));

            // AUTO-SCALING LOGIC
            function scaleSlider() {
                const container = document.querySelector('.slide-container');
                if (!container) return;
                const winWidth = window.innerWidth;
                const winHeight = window.innerHeight;
                // Leave a small margin (0.95) for professional look
                const scale = Math.min(winWidth / 1280, winHeight / 720) * 0.95;
                container.style.transform = `scale(${scale})`;
            }

            window.addEventListener('resize', scaleSlider);
            scaleSlider();
        })();
    </script>
"""

for file in os.listdir('.'):
    if file.endswith('.html'):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # This time we need to replace the original body style AND the existing button script
            # 1. Strip the static <style> in <head> if it's there
            content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL, count=1)
            
            # 2. Replace the footer component (Style + HTML + Script)
            if '<div id="prev-btn"' in content:
                content = re.sub(r'<style>.*?\.nav-btn.*?</script>', '', content, flags=re.DOTALL)
            
            # 3. Insert the new component before </body>
            if '</body>' in content:
                 content = re.sub(r'</body>', new_component + '</body>', content)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file}")
        except Exception as e:
            print(f"Failed to update {file}: {e}")
