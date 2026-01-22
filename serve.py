#!/usr/bin/env python3
"""
简单的本地博客预览服务器
用法: python serve.py
访问: http://localhost:8000
"""

import http.server
import socketserver
import os
import markdown
from pathlib import Path

PORT = 8000

class BlogHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 如果请求的是markdown文件，转换为HTML
        if self.path.endswith('.md'):
            filepath = self.path[1:]  # 去掉前面的/
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                # 简单的markdown到HTML转换
                html = generate_post_html(filepath, md_content)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
                return
        
        # 默认处理
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def generate_post_html(filepath, md_content):
    """生成博客文章的HTML"""
    # 提取YAML front matter
    lines = md_content.split('\n')
    front_matter = {}
    content_start = 0
    
    if lines[0] == '---':
        for i, line in enumerate(lines[1:], 1):
            if line == '---':
                content_start = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip()
    
    # 获取内容部分
    post_content = '\n'.join(lines[content_start:])
    
    # 转换markdown为HTML（简单版本）
    try:
        html_content = markdown.markdown(post_content)
    except:
        html_content = f'<pre>{post_content}</pre>'
    
    # 构建完整HTML
    title = front_matter.get('title', '未标题')
    date = front_matter.get('date', '')
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 小凯的博客</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        .post-header {{ border-bottom: 2px solid #667eea; padding-bottom: 20px; margin-bottom: 30px; }}
        .post-title {{ font-size: 2.2em; margin: 0 0 10px 0; color: #333; }}
        .post-meta {{ color: #666; font-size: 0.95em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="post-header">
            <h1 class="post-title">{title}</h1>
            <p class="post-meta">发布于: {date}</p>
        </div>
        <div class="post-content">
            {html_content}
        </div>
    </div>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    handler = BlogHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"📝 博客服务器已启动!")
        print(f"🌐 访问地址: http://localhost:{PORT}")
        print(f"📁 服务目录: {os.getcwd()}")
        print(f"⏹️  按 Ctrl+C 停止服务")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 服务已停止")
