import os

script = """    <script>
        document.addEventListener('keydown', function (e) {
            const currentPath = window.location.pathname;
            let fileName = currentPath.split('/').pop() || 'index.html';
            if (fileName === 'index.html') fileName = '1.html';
            let currentPage = parseInt(fileName.replace('.html', '')) || 1;

            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
                if (currentPage < 10) window.location.href = (currentPage + 1) + '.html';
            } else if (e.key === 'ArrowLeft') {
                if (currentPage > 1) window.location.href = (currentPage - 1) + '.html';
            }
        });
    </script>
</body>"""

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'window.location.href' not in content:
                    new_content = content.replace('</body>', script)
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file}")
            except Exception as e:
                print(f"Failed to update {file}: {e}")
