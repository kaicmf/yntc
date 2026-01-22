#!/usr/bin/env python3
"""生成静态博客网站 - 无需Ruby依赖"""
import os
import shutil
from pathlib import Path
import markdown
import yaml
from datetime import datetime

def create_site():
    """生成_site目录"""
    # 清理并创建输出目录
    site_dir = Path("_site")
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir()
    
    # 复制assets
    if Path("assets").exists():
        shutil.copytree("assets", "_site/assets")
    
    # 生成首页
    generate_index()
    
    # 生成文章页面
    generate_posts()
    
    # 生成about页面
    generate_page("about.md", "_site/about/index.html")
    
    # 生成archive页面
    generate_archive()
    
    print("✅ 网站生成完成！")

def read_frontmatter(content):
    """解析YAML frontmatter"""
    lines = content.split('\n')
    if not lines[0].startswith('---'):
        return {}, content
    
    fm_lines = []
    content_start = 0
    for i, line in enumerate(lines[1:], 1):
        if line.startswith('---'):
            content_start = i + 1
            break
        fm_lines.append(line)
    
    try:
        frontmatter = yaml.safe_load('\n'.join(fm_lines))
        if frontmatter is None:
            frontmatter = {}
    except:
        frontmatter = {}
    
    body = '\n'.join(lines[content_start:])
    return frontmatter or {}, body

def generate_index():
    """生成首页"""
    posts = []
    posts_dir = Path("_posts")
    
    if posts_dir.exists():
        for post_file in sorted(posts_dir.glob("*.md"), reverse=True):
            with open(post_file, 'r', encoding='utf-8') as f:
                fm, body = read_frontmatter(f.read())
            
            posts.append({
                'title': fm.get('title', post_file.stem),
                'date': fm.get('date', 'Unknown'),
                'excerpt': markdown.markdown(body[:200]),
                'url': f"/{post_file.stem}/"
            })
    
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小凯的个人博客</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.9; }
        .container { max-width: 900px; margin: 30px auto; padding: 0 20px; }
        .posts { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .post { padding: 30px; border-bottom: 1px solid #eee; }
        .post:last-child { border-bottom: none; }
        .post h2 { margin-bottom: 10px; }
        .post h2 a { color: #667eea; text-decoration: none; }
        .post h2 a:hover { text-decoration: underline; }
        .post-date { color: #999; font-size: 0.9em; margin-bottom: 15px; }
        .post-excerpt { color: #555; line-height: 1.6; }
        .nav { background: white; padding: 20px; border-radius: 8px; margin-top: 30px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .nav a { margin: 0 15px; color: #667eea; text-decoration: none; }
        .nav a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 小凯的个人博客</h1>
        <p>学习、思考、分享</p>
    </div>
    
    <div class="container">
        <div class="posts">
"""
    
    for post in posts:
        html += f"""        <div class="post">
            <h2><a href="{post['url']}">{post['title']}</a></h2>
            <div class="post-date">{post['date']}</div>
            <div class="post-excerpt">{post['excerpt']}</div>
        </div>
"""
    
    html += """        </div>
        
        <div class="nav">
            <a href="/about/">关于</a>
            <a href="/archive/">文章存档</a>
            <a href="https://github.com/kaicmf/yntc" target="_blank">GitHub</a>
        </div>
    </div>
</body>
</html>"""
    
    Path("_site/index.html").write_text(html)

def generate_posts():
    """生成文章页面"""
    posts_dir = Path("_posts")
    if not posts_dir.exists():
        return
    
    for post_file in posts_dir.glob("*.md"):
        with open(post_file, 'r', encoding='utf-8') as f:
            fm, body = read_frontmatter(f.read())
        
        html_content = markdown.markdown(body)
        title = fm.get('title', post_file.stem)
        date = fm.get('date', 'Unknown')
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 小凯的博客</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header-info {{ opacity: 0.9; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        .post {{ background: white; border-radius: 8px; padding: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .post-content {{ color: #333; line-height: 1.8; font-size: 1.1em; }}
        .post-content h2 {{ margin: 30px 0 15px 0; color: #333; }}
        .post-content h3 {{ margin: 20px 0 10px 0; color: #555; }}
        .post-content p {{ margin-bottom: 15px; }}
        .post-content code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New'; }}
        .post-content pre {{ background: #2b2b2b; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 15px 0; }}
        .post-content ul, .post-content ol {{ margin: 15px 0 15px 20px; }}
        .post-content li {{ margin-bottom: 5px; }}
        .back-link {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }}
        .back-link a {{ color: #667eea; text-decoration: none; }}
        .back-link a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="header-info">📅 {date}</div>
    </div>
    
    <div class="container">
        <div class="post">
            <div class="post-content">
                {html_content}
            </div>
            <div class="back-link">
                <a href="/">← 返回首页</a>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        # 创建文章目录和index.html
        post_dir = Path(f"_site/{post_file.stem}")
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / "index.html").write_text(html)

def generate_page(md_file, output_path):
    """生成页面"""
    if not Path(md_file).exists():
        return
    
    with open(md_file, 'r', encoding='utf-8') as f:
        fm, body = read_frontmatter(f.read())
    
    html_content = markdown.markdown(body)
    title = fm.get('title', 'Page')
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        .content {{ background: white; border-radius: 8px; padding: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .content h2 {{ margin: 20px 0 10px 0; color: #333; }}
        .content p {{ margin-bottom: 15px; color: #555; line-height: 1.8; }}
        .back-link {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }}
        .back-link a {{ color: #667eea; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
    </div>
    
    <div class="container">
        <div class="content">
            {html_content}
            <div class="back-link">
                <a href="/">← 返回首页</a>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html)

def generate_archive():
    """生成文章存档页面"""
    posts = []
    posts_dir = Path("_posts")
    
    if posts_dir.exists():
        for post_file in sorted(posts_dir.glob("*.md"), reverse=True):
            with open(post_file, 'r', encoding='utf-8') as f:
                fm, body = read_frontmatter(f.read())
            
            posts.append({
                'title': fm.get('title', post_file.stem),
                'date': fm.get('date', 'Unknown'),
                'categories': fm.get('categories', []),
                'url': f"/{post_file.stem}/"
            })
    
    posts_by_year = {}
    for post in posts:
        year = str(post['date'])[:4]
        if year not in posts_by_year:
            posts_by_year[year] = []
        posts_by_year[year].append(post)
    
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章存档</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; }
        .header h1 { font-size: 2em; }
        .container { max-width: 900px; margin: 30px auto; padding: 0 20px; }
        .archive { background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .year { margin-bottom: 30px; }
        .year h2 { color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 15px; }
        .post-item { padding: 10px 0; border-bottom: 1px solid #eee; }
        .post-item:last-child { border-bottom: none; }
        .post-date { color: #999; font-size: 0.9em; margin-right: 15px; }
        .post-title a { color: #667eea; text-decoration: none; }
        .post-title a:hover { text-decoration: underline; }
        .post-category { color: #999; font-size: 0.85em; }
        .back-link { margin-top: 30px; text-align: center; }
        .back-link a { color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 文章存档</h1>
    </div>
    
    <div class="container">
        <div class="archive">
"""
    
    for year in sorted(posts_by_year.keys(), reverse=True):
        html += f"            <div class=\"year\">\n"
        html += f"                <h2>{year}</h2>\n"
        for post in posts_by_year[year]:
            categories = ", ".join(post['categories']) if post['categories'] else "未分类"
            html += f"""                <div class="post-item">
                    <span class="post-date">{post['date']}</span>
                    <span class="post-title"><a href="{post['url']}">{post['title']}</a></span>
                    <span class="post-category">({categories})</span>
                </div>
"""
        html += "            </div>\n"
    
    html += """        </div>
        
        <div class="back-link">
            <a href="/">← 返回首页</a>
        </div>
    </div>
</body>
</html>"""
    
    Path("_site/archive/index.html").parent.mkdir(parents=True, exist_ok=True)
    Path("_site/archive/index.html").write_text(html)

if __name__ == "__main__":
    try:
        create_site()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
