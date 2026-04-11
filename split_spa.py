import os
import re

# Template for individual slide files
FILE_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trinity Labs Pitch Deck - Slide {page_num}</title>
    <link rel="icon" type="image/png" href="favicon.png">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;800&family=Gothic+A1:wght@300;400;500;700;800&display=swap" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css" rel="stylesheet" />
    <style>
        * {{ box-sizing: border-box; }}
        body, html {{
            margin: 0; padding: 0; width: 100%; height: 100dvh;
            background-color: #050810; color: #FFFFFF;
            font-family: 'Noto Sans KR', sans-serif; overflow: hidden;
            display: flex; justify-content: center; align-items: center;
        }}
        .slide-container {{
            width: 1280px; height: 720px;
            position: relative; flex-shrink: 0;
            transform-origin: center;
            background-color: #050810;
        }}
        .nav-btn {{
            position: fixed; top: 50%; transform: translateY(-50%);
            width: 60px; height: 60px; background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: #FFFFFF; font-size: 24px; cursor: pointer; z-index: 10000;
            text-decoration: none; transition: all 0.3s ease;
        }}
        .nav-btn:hover {{ background: rgba(59, 130, 246, 0.2); border-color: #3B82F6; }}
        .prev-btn {{ left: 30px; }}
        .next-btn {{ right: 30px; }}
        .nav-btn.hidden {{ display: none; }}
    </style>
</head>
<body>
    {prev_btn}
    {next_btn}
    
    {content}

    <script>
        (function() {{
            function scaleDeck() {{
                const container = document.querySelector('.slide-container');
                const winWidth = window.innerWidth;
                const winHeight = window.innerHeight;
                const isPortrait = winHeight > winWidth;
                let scale;
                
                if (isPortrait && winWidth < 768) {{
                    scale = (winWidth / 1280) * 0.92;
                }} else if (winHeight < 500) {{
                    scale = Math.min(winWidth / 1280, winHeight / 720) * 0.88; 
                }} else {{
                    scale = Math.min(winWidth / 1280, winHeight / 720) * 0.95;
                }}
                if (container) container.style.transform = `scale(${{scale}})`;
            }}
            window.addEventListener('resize', scaleDeck);
            scaleDeck();
        }})();
    </script>
</body>
</html>
"""

def split_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all sections
    sections = re.findall(r'<section class="slide-section" id="section-(\d+)">\s*(.*?)\s*</section>', content, re.DOTALL)
    
    for i, (num_str, section_content) in enumerate(sections):
        page_num = int(num_str)
        
        prev_btn = f'<a href="{page_num-1}.html" class="nav-btn prev-btn"><i class="fas fa-chevron-left"></i></a>' if page_num > 1 else ""
        # 1.html is the second page in logic if index is first, but here we keep 1.html for slide 1.
        if page_num == 1:
            # Special case for 1.html prev -> index.html? Maybe not if standalone.
            prev_btn = ""
        elif page_num == 2:
            prev_btn = f'<a href="index.html" class="nav-btn prev-btn"><i class="fas fa-chevron-left"></i></a>'

        next_btn = f'<a href="{page_num+1}.html" class="nav-btn next-btn"><i class="fas fa-chevron-right"></i></a>' if page_num < 10 else ""

        # Clean up section content - remove any extra wrappers if present
        # Most likely it's just the slide-container
        
        output = FILE_TEMPLATE.format(
            page_num=page_num,
            prev_btn=prev_btn,
            next_btn=next_btn,
            content=section_content.strip()
        )
        
        filename = f'{page_num}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Generated {filename}")

if __name__ == "__main__":
    split_index()
