import os

# High-visibility styling
btn_style = """
    <style>
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
        /* Mobile adjustment */
        @media (max-width: 768px) {
            .nav-btn { width: 55px; height: 55px; font-size: 22px; }
            .prev-btn { left: 15px; }
            .next-btn { right: 15px; }
        }
    </style>
"""

# HTML and JS logic
new_component = btn_style + """
    <div id="prev-btn" class="nav-btn prev-btn"><i class="fas fa-chevron-left"></i></div>
    <div id="next-btn" class="nav-btn next-btn"><i class="fas fa-chevron-right"></i></div>

    <script>
        (function() {
            function navigate(direction) {
                const currentPath = window.location.pathname;
                let fileName = currentPath.split('/').pop() || 'index.html';
                
                // Handle index.html or empty path as page 1
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

            document.addEventListener('keydown', function (e) {
                if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
                    navigate('next');
                } else if (e.key === 'ArrowLeft') {
                    navigate('prev');
                }
            });

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
        })();
    </script>
"""

for file in os.listdir('.'):
    if file.endswith('.html'):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # SAFE replacement: Add component BEFORE </body>
            if 'nav-btn' not in content:
                # First, remove any existing scripts we might have added manually in the reset point
                # Since we reset to a state WITH the basic script, we should replace that script or just append before </body>
                # The reset point (08e3d85) had a <script> block with 'window.location.href'
                import re
                content = re.sub(r'<script>.*?</script>\s*</body>', new_component + '</body>', content, flags=re.DOTALL)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file}")
        except Exception as e:
            print(f"Failed to update {file}: {e}")
